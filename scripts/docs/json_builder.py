import json
import os

import pkgutil
import importlib
import sys
from importlib.machinery import ModuleSpec
from types import ModuleType, FunctionType
import inspect
from typing import Dict

from docstring_parser import parse


def docstring_data(docstr: str):
    parsed_docstr = parse(docstr)
    params_data = []
    for doc_param in parsed_docstr.params:
        params_data.append({
            'arg_name': doc_param.arg_name,
            'default': doc_param.default,
            'is_optional': doc_param.is_optional,
            'type_name': doc_param.type_name
        })

    data = {
        "params": params_data,
        "long_description": parsed_docstr.long_description,
        "short_description": parsed_docstr.short_description,
        "examples": str(parsed_docstr.examples)
    }
    if parsed_docstr.returns:
        data["returns"]: parsed_docstr.returns.type_name

    return data


def signature_data(sig: inspect.Signature) -> dict:
    params_data = []

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            annotation = None
        params_data.append([str(param), str(annotation)])

    return {
        "params": params_data,
        "return_type": str(sig.return_annotation)
    }


def function_data(func: FunctionType) -> dict:
    return {
        "kind": "function",
        "docstring": inspect.getdoc(func),
        "docstring_parsed": docstring_data(inspect.getdoc(func)),
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
            "AFM" : compute.model.attribute.afm_models.AFM,
            "Class2" : path.in.json.Class2
        }
    :param data: dict with the module data
    :return:
    """
    links = {}

    def _recursive_find_classes(data: dict, path: str):
        if data.get("kind", None) in ["class", "function"]:
            # Last item in path corresponds to the class name
            links[path.split(".")[-1]] = path

        for key, val in data.items():
            if isinstance(val, dict):
                _recursive_find_classes(val, path + "." + key)

    _recursive_find_classes(module_data, "")

    #  The dict has to be sorted in order of longest keys to shortest
    #  to properly generate links. Example:
    #      GoodApi : link1, GoodApiClient : link2
    #  then if GoodApiClient was a match in text it would be matched first
    #  and ruin the link for GoodApiClient
    #
    #  Note: This requires Python 3.7+ to work (ordered dict as a default),
    #  but that's standard by now
    sorted_keys = sorted(links, key=lambda key: len(key), reverse=True)
    links = {key: links[key] for key in sorted_keys}
    return links


if __name__ == '__main__':
    import gooddata_sdk

    MODULE_NAME = "gooddata_sdk"  # This global variable is needed in further parsing
    import_submodules(MODULE_NAME)
    res = parse_package(gooddata_sdk)
    open("data.json", "w+").write(json.dumps(res))
    open("links.json", "w+").write(json.dumps(generate_links(res)))

    print(f"Saved json and links to {os.getcwd()}")
