# (C) 2023 GoodData Corporation
import argparse
import json
import os
from enum import Enum
from pathlib import Path
from typing import List, TextIO, TypeVar

import attr
import toml

_API_SPEC_LINKS = {}
_ROOT_DIR = ""

MODULE_TEMPLATE_STRING = Path("module_template.md").read_text()
CLASS_TEMPLATE_STRING = Path("class_template.md").read_text()
METHOD_TEMPLATE_STRING = Path("method_template.md").read_text()

# TABLES
_TABLE_BASE = "\n\n| Name | Description |\n|--|--|\n"
_CLASS_TABLE = "## Classes"
_MODULE_TABLE = "## Modules"
_PARAMETERS_TABLE = "## Parameters"
_METHOD_TABLE = "## Methods"
_PROPERTIES_TABLE = "## Properties"
_RETURN_TABLE = "## Returns"
_TABLE_NONE = "\n\n _None_ \n"
_METHOD_TABLE_BASE = "\n\n| Name | Type | Description |\n|--|--|--|\n"

SpecModule = TypeVar("SpecModule", bound="TemplateReplacementSpecModule")
SpecTemplate = TypeVar("SpecTemplate", bound="TemplateReplacementSpec")


class RefType(Enum):
    METHOD = 1
    CLASS = 2
    MODULE = 3


@attr.s(auto_attribs=True)
class RefHolder:
    """ """
    name: str
    url: str
    packages: []
    directory: str


@attr.s(auto_attribs=True)
class CodeBlockParameter:
    """ """

    type: str
    name: str
    description: str


@attr.s(auto_attribs=True)
class TemplateReplacementSpec:
    """
    Specification holder to be rendered into documentation.
        name - name of the object
    """

    name: str = attr.ib(default=None)
    path: str = attr.ib(default=None)
    _import_path: str = attr.ib(default=None)

    def render(self, file: TextIO):
        raise "Called render from interface class!"

    @staticmethod
    def create_table(template: str, spec_list: List[SpecTemplate] | None = None, delete: bool = False) -> str:

        if spec_list and len(spec_list) != 0:
            table = template + _TABLE_BASE
            for item in spec_list:
                table += f"| [{item.name}](./{item.name.lower()}/) | {item.description} |\n"
        else:
            if delete:
                return ""
            table = template + _TABLE_NONE
        return table

    @staticmethod
    def create_methods_table(template: str, spec_list: List[SpecTemplate] | None = None) -> str:
        if spec_list and len(spec_list) != 0:
            table = template + _METHOD_TABLE_BASE
            for item in spec_list:
                table += f"| {item.name} | {item.type} |{item.description} |\n"
        else:
            table = template + _TABLE_NONE
        return table


@attr.s(auto_attribs=True)
class TemplateReplacementSpecMethod(TemplateReplacementSpec):
    """
    Module specification holder.
        _parameters - list of method parameters
        _returns - return value
        description - description of the method
        description_long - long description
    """

    _parameters: [CodeBlockParameter] = attr.ib(default=None)
    return_type: str = attr.ib(default=None)
    return_desc: str = attr.ib(default=None)
    description: str = attr.ib(default=None)
    description_long: str = attr.ib(default=None)
    usage: str = attr.ib(default="")
    parent: str = attr.ib(default="")

    def render(self, file: TextIO):
        spec = METHOD_TEMPLATE_STRING

        parameter_str = self.create_methods_table(_PARAMETERS_TABLE, self._parameters)

        returns_str = (
            f"{_RETURN_TABLE}\n\n | Type | Description|\n|--|--|\n |{self.return_type} | {self.return_desc}|\n\n"
            if self.return_type != "" else f"{_RETURN_TABLE}\n\n_None_\n\n"
        )

        spec = spec.replace("METHOD_NAME", self.name)
        spec = spec.replace("METHOD_USAGE", self.usage)
        spec = spec.replace("METHOD_DESCRIPTION", self.description_long)
        spec = spec.replace("PARAMETERS", parameter_str)
        spec = spec.replace("RETURNS", returns_str)
        spec = spec.replace("PARENT_NAME", self.parent)
        file.write(spec)


@attr.s(auto_attribs=True)
class TemplateReplacementSpecClass(TemplateReplacementSpec):
    """
    Module specification holder.
        _methods - list of methods in the class
        _properties - list of properties
        description - description of the class
    """
    _methods: [TemplateReplacementSpecMethod] = attr.ib(default=None)
    _properties: [CodeBlockParameter] = attr.ib(default=None)
    description: str = attr.ib(default=None)
    description_long: str = attr.ib(default=None)


    def render(self, file: TextIO):
        properties_str = self.create_table(_PROPERTIES_TABLE, self._properties)

        methods_str = self.create_table(_METHOD_TABLE, self._methods)

        spec = CLASS_TEMPLATE_STRING
        spec = spec.replace("METHODS", methods_str)
        spec = spec.replace("PROPERTIES", properties_str)
        spec = spec.replace("CLASS_NAME", self.name)
        spec = spec.replace("CLASS_DESCRIPTION", self.description_long)
        for method in self._methods:
            fl = Path(method.path + "/_index.md")
            fl.parent.mkdir(parents=True, exist_ok=True)
            with open(fl, "w") as f:
                method.render(f)
        file.write(spec)


@attr.s(auto_attribs=True)
class TemplateReplacementSpecModule(TemplateReplacementSpec):
    """
    Module specification holder.
        _classes - list of classes in the module
        _modules - list of modules in the module
        _description - description of the module
    """

    _classes: [TemplateReplacementSpecClass] = attr.ib(default=None)
    _modules: [SpecModule] = attr.ib(default=None)
    description: str = attr.ib(default=None)
    description_long: str = attr.ib(default=None)

    def render(self, file: TextIO):
        classes_str = self.create_table(_CLASS_TABLE, self._classes, delete=True)

        module_str = self.create_table(_MODULE_TABLE, self._modules, delete=True)

        spec = MODULE_TEMPLATE_STRING
        spec = spec.replace("MODULE_NAME", self.name)
        spec = spec.replace("MODULE_DESCRIPTION", self.description_long)
        spec = spec.replace("CLASSES", classes_str)
        spec = spec.replace("MODULES", module_str)
        for clss in self._classes:
            fl = Path(clss.path + "/_index.md")
            fl.parent.mkdir(parents=True, exist_ok=True)
            with open(fl, "w") as f:
                clss.render(f)
        for mod in self._modules:
            fl = Path(mod.path + "/_index.md")
            fl.parent.mkdir(parents=True, exist_ok=True)
            with open(fl, "w") as f:
                mod.render(f)
        if self.name != "url_root":
            file.write(spec)


def parse_usage(name: str, data: dict):
    result = f"{name}("
    for param in data["params"]:
        if param[0] != "self":
            result += str(param[0])
    result += ")"
    if "return_annotation" in data:
        result += f" -> {data['return_annotation']}"
    return result


def read_json_file(file_path: str) -> dict:
    """Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path) as json_file:
        return json.load(json_file)


def parse_method(
        data_root: dict, api_path: str, module_import_path: str, name: str, parent: str
) -> TemplateReplacementSpecMethod:

    long_description = str(data_root["docstring"]) if data_root["docstring"] is not None else ""
    short_description = ""
    params = []
    return_type = data_root["signature"]["return_annotation"]
    return_description = ""

    if "docstring_parsed" in data_root and data_root["docstring_parsed"] is not None:

        if (
            "params" in data_root["docstring_parsed"]
            and data_root["docstring_parsed"]["params"] is not None
        ):
            params = [
                CodeBlockParameter(
                    obj["type_name"],
                    obj["arg_name"],
                    str(obj["description"]).replace("\n", "")
                ) for obj in data_root["docstring_parsed"]["params"]
            ]

        if (
            "short_description" in data_root["docstring_parsed"]
            and data_root["docstring_parsed"]["short_description"] is not None
        ):
            short_description = str(data_root["docstring_parsed"]["short_description"])

        if (
            "returns" in data_root["docstring_parsed"]
            and data_root["docstring_parsed"]["returns"] is not None
        ):
            return_description = data_root["docstring_parsed"]["returns"]["description"]

    return TemplateReplacementSpecMethod(
        parameters=params,
        return_type=return_type,
        return_desc=return_description,
        name=name,
        path=api_path,
        import_path=module_import_path,
        description=short_description,
        description_long=long_description,
        usage=parse_usage(name, data_root["signature"]),
        parent=parent
    )


def parse_class(json_root: dict, api_path: str, module_import_path: str, name: str) -> TemplateReplacementSpecClass:
    class_methods = []
    short_description = ""

    for fname, obj in json_root.items():
        # There are entries in the json, that are not dicts (e.g.: the field `kind`)
        if not isinstance(obj, dict):
            continue
        # If an object already has a page, skip it
        if fname in _API_SPEC_LINKS:
            continue

        obj_module_import_path = module_import_path + f".{fname}" if module_import_path != "" else name

        # Remove ".functions" from the path, to correspond to the import path
        if ".functions" in obj_module_import_path:
            obj_module_import_path = obj_module_import_path.replace(".functions", "")

        if fname == "functions":
            for func_name, func_obj in obj.items():
                if func_name.startswith("_"):
                    continue  # Skip magic and private methods

                class_methods.append(
                    parse_method(
                        data_root=func_obj,
                        api_path=f"{api_path}/{func_name}",
                        module_import_path=obj_module_import_path,
                        name=func_name,
                        parent=name
                    )
                )
                # Add entry for url linking
                _API_SPEC_LINKS[func_name] = {
                    "path": f"{api_path}/{func_name}".lower(),  # Lowercase for Hugo
                    "kind": "function",
                }
            continue  # No need to recurse deeper, functions are the last level

        if "docstring_parsed" in json_root and json_root["docstring_parsed"] is not None:
            if (
                    "short_description" in json_root["docstring_parsed"]
                    and json_root["docstring_parsed"]["short_description"] is not None
            ):
                short_description = str(json_root["docstring_parsed"]["short_description"])

    return TemplateReplacementSpecClass(
        methods=class_methods,
        description_long=str(json_root["docstring"]),
        name=name,
        path=api_path,
        description=short_description
    )


def parse_module(json_root: dict, api_path: str, module_import_path: str, name: str) -> TemplateReplacementSpecModule:
    module_classes = []
    module_modules = []
    short_description = ""
    description = json_root["docstring"] if "docstring" in json_root else ""
    for fname, obj in json_root.items():
        # There are entries in the json, that are not dicts (e.g.: the field `kind`)
        if not isinstance(obj, dict):
            continue
        # If an object already has a page, skip it
        if fname in _API_SPEC_LINKS:
            continue

        kind = obj.get("kind", None)

        obj_module_import_path = module_import_path + f".{fname}" if module_import_path != "" else name

        # Remove ".functions" from the path, to correspond to the import path
        if ".functions" in obj_module_import_path:
            obj_module_import_path = obj_module_import_path.replace(".functions", "")

        # Create files based on the kind of the data: module/class/function
        if kind == "module":

            _API_SPEC_LINKS[fname] = {"path": f"{api_path}/{fname}".lower(), "kind": "module"}  # Lowercase for Hugo
            module_modules.append(
                parse_module(
                    json_root=obj, api_path=f"{api_path}/{fname}", module_import_path=obj_module_import_path, name=fname
                )
            )

            # Add entry for url linking

        elif kind == "class":
            _API_SPEC_LINKS[fname] = {"path": f"{api_path}/{fname}".lower(), "kind": "class"}  # Lowercase for Hugo
            module_classes.append(
                parse_class(
                    json_root=obj,
                    api_path=f"{api_path}/{fname}",
                    module_import_path=module_import_path,
                    name=fname
                )
            )

        else:
            continue  # Not a class nor a module


    if "docstring_parsed" in json_root and json_root["docstring_parsed"] is not None:
        if (
                "short_description" in json_root["docstring_parsed"]
                and json_root["docstring_parsed"]["short_description"] is not None
        ):
            short_description = str(json_root["docstring_parsed"]["short_description"])

    return TemplateReplacementSpecModule(
        classes=module_classes,
        modules=module_modules,
        description=short_description,
        name=name,
        path=api_path,
        description_long=description
    )


def create_file_structure(data: dict, root_path: Path, url_root: str, packages: []):
    """Recursively create file structure based on JSON data.

    Args:
        data (dict): JSON data representing the object.
        root_path (Path): Path to the root directory.
        url_root (str): URL root path for the API reference.
        packages (list): list of packages to use
    """

    file = Path(_ROOT_DIR / root_path / ".")
    file.parent.mkdir(parents=True, exist_ok=True)
    file = Path(_ROOT_DIR / root_path / ".")
    for package in packages:
        if not data[package]:
            continue
        new_data = data[package]
        root = parse_module(
            json_root=new_data,
            api_path=root_path.__str__()+"/"+package,
            module_import_path="",
            name=package
        )
        file = Path(root_path.__str__() + "/" + package + "/_index.md")
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w") as f:
            root.render(f)


def change_json_root(data: dict, json_start_paths: List[str] | None) -> dict:
    """Change the root of the JSON data to the specified path.

    Args:
        data (dict): Dict with the module data.
        json_start_paths (List[str] | None): Paths to the object in the JSON data.

    Returns:
        dict: Modified JSON data.
    """
    if json_start_paths is None:
        return data

    new_json = {}
    for json_start_path in json_start_paths:
        new_root_data = data
        for part in json_start_path.split("."):
            new_root_data = new_root_data[part]
        new_json[json_start_path.split(".")[-1]] = new_root_data
    return new_json


def parse_toml(toml_path: str, version: str) -> [RefHolder]:
    references = []
    # In case of missing toml_file, we need a default for the api-references
    if not os.path.exists(toml_path):
        return [
            RefHolder(
                name="sdk",
                url=f"/{version}/api-reference",
                packages=["sdk", "catalog"],
                directory=f"{_ROOT_DIR}/{version}/api-reference"
            )
        ]
    parsed_toml = toml.load(toml_path)
    for name in parsed_toml:
        packages = parsed_toml[name]["packages"]
        directory = f"{_ROOT_DIR}/{version}/{parsed_toml[name]['directory']}"
        url = f"{version}/{parsed_toml[name]['directory']}"
        references.append(RefHolder(name, url, packages, directory))
    return references


def main():
    parser = argparse.ArgumentParser(
        description="Process a JSON file"
    )
    parser.add_argument(
        "toml_file", metavar="FILE", help="Path to toml config file", default="api_spec.toml"
    )
    parser.add_argument(
        "json_file", metavar="FILE", help="Path to json data file", default="data.json"
    )
    parser.add_argument(
        "version", metavar="str", help="Current Version", default="latest"
    )
    parser.add_argument(
        "root_directory", metavar="str", help="Current Version", default="versioned_docs"
    )

    args = parser.parse_args()
    references = parse_toml(args.toml_file, args.version)
    for ref in references:
        print({args.root_directory + ref.directory})
        data = read_json_file(args.json_file)
        data = change_json_root(data, ref.packages)
        create_file_structure(data, Path(args.root_directory + ref.directory), url_root=ref.url, packages=ref.packages)
        _API_SPEC_LINKS.clear()
    print("Dumping the links.json")

    # print(_API_SPEC_LINKS)


if __name__ == "__main__":
    main()
