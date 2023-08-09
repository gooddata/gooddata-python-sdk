import importlib
import inspect
import json
import os
import pkgutil
import re
import sys
from types import FunctionType, ModuleType
from typing import Any, Dict, Optional

import cattrs
import docstring_parser
from attr import define
from docstring_parser import parse
from docstring_parser.common import DocstringStyle


# Object definitions
@define
class ParamsData:
    arg_name: str
    default: str | None
    is_optional: bool | None
    type_name: str | None
    description: str | None


@define
class ReturnData:
    type_name: str | None
    description: str | None
    return_name: str | None


@define
class DocstringData:
    params: list[ParamsData]
    long_description: str | None
    short_description: str | None
    examples: str
    returns: Optional[ReturnData] = None


@define
class SignatureData:
    params: list[tuple[str, str]]
    return_annotation: str


@define
class FunctionData:
    docstring: str | None
    signature: SignatureData
    is_property: bool = False
    docstring_parsed: Optional[DocstringData] = None
    kind: str = "function"


@define
class ClassData:
    docstring: str | None
    functions: dict[str, FunctionData]
    docstring_parsed: Optional[DocstringData] = None
    kind: str = "class"


# regex patterns for `docstring_fixes` function
docstr_fix_none_pattern = re.compile(r"Args:[\n ]*None")


def docstring_fixes(docstr: str) -> str:
    """
    Sometimes GD docstrings use invalid formatting, which the parser is unable to parse
    This function fixes those issues

    Args:
        docstr: docstring to fix
    Returns:
        str: fixed docstring
    """
    # Fix for Args: None in docstrings, which is not valid
    docstr = docstr_fix_none_pattern.sub("", docstr)
    return docstr


def docstring_data(docstr: Optional[str]) -> Optional[DocstringData]:
    """
    Parse the docstring and return the parser data in a dict

    Args:
        docstr (Optional[str]): docstring to parse

    Returns:
        DocstringData: parsed docstring data

    Raises:
        ValueError: if the docstring is invalid (= not Google style)
    """
    if docstr is None:
        return None
    docstr = docstring_fixes(docstr)
    try:
        parsed_docstr = parse(docstr, style=DocstringStyle.GOOGLE)
    except docstring_parser.common.ParseError:
        raise ValueError(f"Invalid docstring: {docstr}")
    if ":param" in docstr:
        # Some numpy style docstrings are parsed without throwing an error
        # but the parsed data is invalid, this is a quick way to detect those
        raise ValueError(f"Invalid docstring (numpy): {docstr}")

    params_data: list[ParamsData] = []
    for doc_param in parsed_docstr.params:
        params_data.append(
            ParamsData(
                arg_name=doc_param.arg_name,
                default=doc_param.default,
                is_optional=doc_param.is_optional,
                type_name=doc_param.type_name,
                description=doc_param.description,
            )
        )
    data = DocstringData(
        params=params_data,
        long_description=parsed_docstr.long_description,
        short_description=parsed_docstr.short_description,
        examples=str(parsed_docstr.examples),
    )
    if parsed_docstr.returns:
        data.returns = ReturnData(
            type_name=parsed_docstr.returns.type_name,
            description=parsed_docstr.returns.description,
            return_name=parsed_docstr.returns.return_name,
        )
    return data


def signature_data(sig: inspect.Signature) -> SignatureData:
    """
    Parse the signature object and return the contained data in a formatted dict

    Args:
        sig: Signature object to be analysed

    Returns:
        SignatureData: parsed signature data
    """
    sig_params_data = []

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            annotation = None
        sig_params_data.append((str(param), str(annotation)))

    return_annotation = sig.return_annotation
    if return_annotation == inspect.Parameter.empty:
        return_annotation = None

    return SignatureData(params=sig_params_data, return_annotation=str(return_annotation))


def function_data(func: FunctionType, is_property: bool = False) -> FunctionData:
    """
    Parse the function object and return information about the function in a formatted dict

    Args:
        func: Function object to be analysed
        is_property: Whether the function is a property

    Returns:
        FunctionData: parsed function data
    """
    try:
        docstr_data = docstring_data(inspect.getdoc(func))
    except ValueError:
        print(f"WARN: Invalid docstring in func {inspect.getmodule(func)}: {str(func)}")
        docstr_data = None
    return FunctionData(
        docstring=inspect.getdoc(func),
        docstring_parsed=docstr_data,
        signature=signature_data(inspect.signature(func)),
        is_property=is_property,
    )


def class_data(obj: type) -> ClassData:
    """
    Parse the class object and return information about the class in a formatted dict

    Args:
        obj(type): class object to be analysed
    Returns:
        ClassData: parsed class data
    """
    data = {key: value for key, value in inspect.getmembers(obj)}
    ret = ClassData(
        docstring=inspect.getdoc(obj),
        docstring_parsed=docstring_data(inspect.getdoc(obj)),
        functions={},
    )
    for key, value in data.items():
        if isinstance(value, FunctionType):
            ret.functions[key] = function_data(value)
        elif isinstance(value, property):
            for attr in ("fget", "fset", "fdel"):
                if hasattr(value, attr) and getattr(value, attr) is not None:
                    ret.functions[key] = function_data(getattr(value, attr), is_property=True)

        # As of now, there are no subclasses in the gooddata package,
        # and the data would not be handled correctly
        # if inspect.isclass(value) and key != "__class__":
        #     ret["classes"][key] = object_data(value)

    return ret


def module_data(module: ModuleType) -> dict:
    """
    Parse a module object and return formatted docstring data about its contents
    Args:
        module (ModuleType): module object to be analysed
    Returns:
        dict: parsed module data
    """
    data: dict[str, Any] = {"kind": "module"}
    objects = vars(module)
    for name, obj in objects.items():
        obj_module = inspect.getmodule(obj)
        if obj_module is None:
            continue

        if isinstance(obj, type):
            # Filter out non-gooddata libraries
            if MODULE_NAME in obj_module.__name__:
                data[name] = class_data(obj)
        elif isinstance(obj, ModuleType):
            if MODULE_NAME in obj_module.__name__:
                data[name] = module_data(obj)
    return data


def parse_package(obj: ModuleType, data=None):
    """
    Parse the package and its submodules into a dict object, that
    can be converted into a json

    Args:
        obj (ModuleType): package object
        data (dict): optional parameter for recursive calling
    Returns:
        dict: data of package


    Example:
        {
        "submodule1": {
            "file1": {
                "class_name" : class_data (see `object_data`)
                }
            }
        }
    """
    if not data:
        data = {}
    data["kind"] = "module"
    if isinstance(obj, ModuleType):
        iterator = pkgutil.iter_modules(obj.__path__)
        for item in iterator:
            if item.name not in data:
                data[item.name] = {}

            if item.ispkg:
                data[item.name].update(parse_package(vars(obj)[item.name]))
            else:
                module = vars(obj)[item.name]
                data[item.name].update(module_data(module))

    return data


def import_submodules(pkg_name):
    """
    Import all submodules of a package, enabling their parsing

    Args:
        pkg_name (str): package name
    """
    package = sys.modules[pkg_name]

    return {
        name: importlib.import_module(f"{pkg_name}.{name}")
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }


def generate_links(module_data: dict) -> Dict[str, dict[str, str]]:
    """
    Generate links for the objects for the json data:

    Args:
        module_data(dict): dict with the module data
    Returns:
        dict: dict with the links
    Example:
    {
        "AFM" : {"path": "compute.model.attribute.afm_models.AFM", "kind": "class"},
        "Class2" : {"path": "path.in.json.Class2", "kind": "class"},
        "func1" : {"path": "path.in.json.func1", "kind": "function"}
    }
    """
    links = {}

    def _recursive_find_classes(data: dict, path: str):
        if data.get("kind", None) in ["class", "function"]:
            # Last item in path corresponds to the class name
            links[path.split(".")[-1]] = {"path": path, "kind": data["kind"]}

        for key, val in data.items():
            if isinstance(val, dict):
                if key == "functions":
                    _recursive_find_classes(val, path)
                elif path != "":
                    _recursive_find_classes(val, f"{path}.{key}")
                else:
                    _recursive_find_classes(val, key)

    _recursive_find_classes(module_data, "")

    sorted_keys = sorted(links, key=lambda key: links[key]["path"], reverse=True)
    links = {key: links[key] for key in sorted_keys}
    return links


if __name__ == "__main__":
    import gooddata_sdk

    MODULE_NAME = "gooddata_sdk"  # This global variable is needed in further parsing
    import_submodules(MODULE_NAME)
    res = parse_package(gooddata_sdk)
    output_json: dict = cattrs.unstructure(res)
    open("data.json", "w+").write(json.dumps(output_json))
    open("links_data.json", "w+").write(json.dumps(generate_links(output_json)))

    print(f"Saved data.json and links_data.json to {os.getcwd()}")
