import json
import os

import pkgutil
import importlib
import sys
from importlib.machinery import ModuleSpec
from types import ModuleType, FunctionType
import inspect
from typing import Dict
import re

import docstring_parser
from docstring_parser import parse
from docstring_parser.common import DocstringStyle

LOG = open("log.txt", "w+")


def docstring_fixes(docstr: str) -> str:
    docstr = re.sub(r"Args:[\n ]*None", "", docstr)  # Fix for Args: None in docstrings, which is not valid
    return docstr


def docstring_data(docstr: str):
    if docstr is None:
        return {}
    docstr = docstring_fixes(docstr)
    try:
        parsed_docstr = parse(docstr, style=DocstringStyle.GOOGLE)
    except docstring_parser.common.ParseError:
        raise ValueError("Invalid docstring: " + docstr)
    if ":param" in docstr:
        raise ValueError("Invalid docstring (numpy): " + docstr)

    params_data = []
    for doc_param in parsed_docstr.params:
        params_data.append({
            'arg_name': doc_param.arg_name,
            'default': doc_param.default,
            'is_optional': doc_param.is_optional,
            'type_name': doc_param.type_name,
            "description": doc_param.description,
        })

    data = {
        "params": params_data,
        "long_description": parsed_docstr.long_description,
        "short_description": parsed_docstr.short_description,
        "examples": str(parsed_docstr.examples)
    }
    if parsed_docstr.returns:
        data["returns"] = {
            "type_name": parsed_docstr.returns.type_name,
            "description": parsed_docstr.returns.description,
            "return_name": parsed_docstr.returns.return_name
        }
    return data


def signature_data(sig: inspect.Signature) -> dict:
    params_data = []

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            annotation = None
        params_data.append([str(param), str(annotation)])

    return_annotation = sig.return_annotation
    if return_annotation == inspect.Parameter.empty:
        return_annotation = None

    return {
        "params": params_data,
        "return_type": str(return_annotation)
    }


def function_data(func: FunctionType) -> dict:
    try:
        docstr_data = docstring_data(inspect.getdoc(func))
    except ValueError:
        LOG.write(str(inspect.getmodule(func)) + ":" + str(func))  # logging invalid docstrings
        LOG.write("\n")
        docstr_data = {}
    return {
        "kind": "function",
        "docstring": inspect.getdoc(func),
        "docstring_parsed": docstr_data,
        "signature": signature_data(inspect.signature(func))
    }


def object_data(obj: type) -> dict:
    data = {key: value for key, value in inspect.getmembers(obj)}
    ret = {
        "kind": "class",
        "docstring": inspect.getdoc(object),
        "docstring_parsed": docstring_data(inspect.getdoc(object)),
        "functions": {}
    }
    for key, value in data.items():
        if isinstance(value, FunctionType):
            ret["functions"][key] = function_data(value)
        # if inspect.isclass(value) and key != "__class__":
        #     ret["classes"][key] = object_data(value)

    return ret


def file_data(module: ModuleType) -> dict:
    data = {"kind": "module"}
    objects = vars(module)
    for name, obj in objects.items():
        if isinstance(obj, type):
            # Filter out non-gooddata libraries
            if MODULE_NAME in inspect.getmodule(obj).__name__:
                data[name] = object_data(obj)
        elif isinstance(obj, ModuleType):
            try:
                if MODULE_NAME in inspect.getmodule(obj).__name__:
                    data[name] = file_data(obj)
            except AttributeError:
                pass
    return data


def parse_package(obj, data=None):
    """
    Parse the package and it's submodules into a dict object, that
    can be converted into a json

    example return:
        {
        "submodule1": {
            "file1": {
                "class_name" : class_data (see `object_data`)
                }
            }
        }

    :param obj: package object
    :param data: optional parameter for recursive calling
    :return: data of package
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
                data[item.name].update(file_data(module))

    return data


def import_submodules(pkg_name):
    """
    Import all submodules of a package, enabling their parsing
    :param pkg_name:
    :return:
    """
    package = sys.modules[pkg_name]

    return {
        name: importlib.import_module(pkg_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }


def generate_links(module_data: dict) -> Dict[str, str]:
    """
    Generate links for the objects for the json data:
        Example:
        {
            "AFM" : {"path": "compute.model.attribute.afm_models.AFM", "kind": "class"},
            "Class2" : {"path": "path.in.json.Class2", "kind": "class"},
            "func1" : {"path": "path.in.json.func1", "kind": "function"}
        }
    :param data: dict with the module data
    :return:
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
                    _recursive_find_classes(val, path + "." + key)
                else:
                    _recursive_find_classes(val, key)

    _recursive_find_classes(module_data, "")

    sorted_keys = sorted(links, key=lambda key: links[key]["path"], reverse=True)
    links = {key: links[key] for key in sorted_keys}
    return links


if __name__ == '__main__':
    import gooddata_sdk

    MODULE_NAME = "gooddata_sdk"  # This global variable is needed in further parsing
    import_submodules(MODULE_NAME)
    res = parse_package(gooddata_sdk)
    open("data.json", "w+").write(json.dumps(res))
    open("links_data.json", "w+").write(json.dumps(generate_links(res)))

    print(f"Saved data.json and links_data.json to {os.getcwd()}")
