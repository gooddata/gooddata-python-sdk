# (C) 2023 GoodData Corporation
import importlib
import inspect
import json
import os
import pkgutil
import re
import sys
from types import FunctionType, ModuleType
from typing import Any

import cattrs
import docstring_parser
from attr import define
from docstring_parser import parse
from docstring_parser.common import Docstring, DocstringStyle


# Object definitions
@define
class ParamsData:
    arg_name: str
    default: str | None
    is_optional: bool | None
    type_name: str | None
    description: str | None

    @classmethod
    def from_docstr_parameter(cls, docstr_parameter):
        return cls(
            arg_name=docstr_parameter.arg_name,
            default=docstr_parameter.default,
            is_optional=docstr_parameter.is_optional,
            type_name=docstr_parameter.type_name,
            description=docstr_parameter.description,
        )


@define
class ReturnData:
    type_name: str | None
    description: str | None
    return_name: str | None

    @classmethod
    def from_parsed_docstr(cls, parsed_docstr: Docstring):
        return cls(
            type_name=parsed_docstr.returns.type_name,
            description=parsed_docstr.returns.description,
            return_name=parsed_docstr.returns.return_name,
        )


@define
class DocstringData:
    params: list[ParamsData]
    long_description: str | None
    short_description: str | None
    examples: str
    returns: ReturnData | None = None

    @classmethod
    def from_parsed_docstr(cls, parsed_docstr: Docstring):
        docstr_data = cls(
            params=[ParamsData.from_docstr_parameter(param) for param in parsed_docstr.params],
            long_description=parsed_docstr.long_description,
            short_description=parsed_docstr.short_description,
            examples=str(parsed_docstr.examples),
        )
        if parsed_docstr.returns:
            docstr_data.returns = ReturnData.from_parsed_docstr(parsed_docstr)
        return docstr_data


@define
class SignatureData:
    params: list[tuple[str, str]]
    return_annotation: str


@define
class FunctionData:
    docstring: str | None
    signature: SignatureData
    is_property: bool = False
    docstring_parsed: DocstringData | None = None
    kind: str = "function"


@define
class ClassData:
    docstring: str | None
    functions: dict[str, FunctionData]
    docstring_parsed: DocstringData | None = None
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


def docstring_data(docstr: str | None) -> DocstringData | None:
    """
    Parse the docstring and return the parser data in a dict

    Args:
        docstr (str | None): docstring to parse

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

    return DocstringData.from_parsed_docstr(parsed_docstr)


def signature_data(sig: inspect.Signature) -> SignatureData:
    """
    Parse the signature object and return the contained data in a formatted dict

    Args:
        sig: Signature object to be analysed

    Returns:
        SignatureData: parsed signature data
    """
    sig_params_data = []

    for param in sig.parameters.values():
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

    return ret


def module_data(module: ModuleType, module_name: str) -> dict:
    """
    Parse a module object and return formatted docstring data about its contents
    Args:
        module (ModuleType): module object to be analysed
    Returns:
        dict: parsed module data
    """
    data: dict[str, Any] = {"kind": "module"}
    objects = vars(module) if hasattr(module, "__dict__") else {}

    for name, obj in objects.items():
        obj_module = inspect.getmodule(obj)
        if obj_module is None:
            continue

        if isinstance(obj, type):
            # Filter out non-gooddata libraries
            if module_name in obj_module.__name__:
                data[name] = class_data(obj)
        elif isinstance(obj, ModuleType) and module_name in obj_module.__name__:
            data[name] = module_data(obj)
    return data


def parse_package(obj: ModuleType, module_name: str = None) -> dict:
    """
    Parse the package and its submodules into a dict object, that
    can be converted into a json

    Args:
        obj (ModuleType): package object
        module_name: name of the module
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
    data = {"kind": "module"}

    if not isinstance(obj, ModuleType):
        return data

    iterator = pkgutil.iter_modules(obj.__path__)
    for item in iterator:
        if item.name not in data:
            data[item.name] = {}

        if item.ispkg and item.name in vars(obj):
            data[item.name].update(parse_package(vars(obj)[item.name], module_name))
        else:
            if item.name in vars(obj):
                module = vars(obj)[item.name]
                data[item.name].update(module_data(module, module_name))
    return data


def import_submodules(pkg_name: str) -> dict[str, ModuleType]:
    """
    Import all submodules of a package, enabling their parsing

    Args:
        pkg_name (str): package name
    """
    package = sys.modules[pkg_name]
    dictionary = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        if importlib.util.find_spec(f"{pkg_name}.{name}") is not None:
            dictionary[name] = importlib.import_module(f"{pkg_name}.{name}")


if __name__ == "__main__":
    import gooddata_pandas
    import gooddata_sdk

    import_submodules("gooddata_sdk")
    import_submodules("gooddata_pandas")
    output_json: dict = {
        **cattrs.unstructure(parse_package(gooddata_pandas, "gooddata_pandas")),
        **cattrs.unstructure(parse_package(gooddata_sdk, "gooddata_sdk")),
    }
    with open("data.json", "w") as f:
        f.write(json.dumps(output_json))

    print(f"Saved the .json file: `data.json` to {os.getcwd()}")
