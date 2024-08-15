# (C) 2023 GoodData Corporation
import argparse
import json
import os
from pathlib import Path
from typing import TextIO

import attr
import toml
from attr import define

MODULE_TEMPLATE_STRING = Path("module_template.md").read_text()
CLASS_TEMPLATE_STRING = Path("class_template.md").read_text()
FUNCTION_TEMPLATE_STRING = Path("function_template.md").read_text()


@attr.s(auto_attribs=True)
class RefHolder:
    """ """

    url: str
    packages: []
    directory: str


@define
class TemplateReplacementSpec:
    """
    Specification for replacing tokens in a template. Tokens currently in use are:
        PARENT - name of the parent object
        NAME - name of the object
        LINK - link title of the object
    """

    parent: None | str = None
    name: None | str = None
    link: None | str = None
    path: None | str = None

    def render_template_to_str(self, template: str) -> str:
        """
        Replace the variables in markdown templates and return the new content string.
        """
        for token, replacement in [
            ("PARENT", self.parent),
            ("NAME", self.name),
            ("LINK", self.link),
            ("PATH", self.path),
        ]:
            if replacement is not None:
                template = template.replace(token, replacement)
        return template

    def render_template_to_file(self, template: str, file: TextIO):
        rendered_string = self.render_template_to_str(template)
        file.write(rendered_string)


def read_json_file(file_path: str) -> dict:
    """Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path) as json_file:
        return json.load(json_file)


def create_file_structure(data: dict, root: Path, url_root: str):
    """Recursively create file structure based on JSON data.

    Args:
        data (dict): JSON data representing the object.
        root (Path): Path to the root directory.
        url_root (str): URL root path for the API reference.
    """
    links = {}

    def _recursive_create(data_root: dict, dir_root: Path, api_ref_root: str, module_import_path: str):
        """Recursively create files and directories.

        Args:
            data_root (dict): Sub-dictionary of the JSON representing the object.
            dir_root (Path): Path to the directory root.
            api_ref_root (str): URL root path for the API reference.
            module_import_path (str): Import path to the object.
        """
        dir_root.mkdir(exist_ok=True)
        for name, obj in data_root.items():
            # There are entries in the json, that are not dicts (ex: the field `kind`)
            if not isinstance(obj, dict):
                continue

            # If an object already has a page, skip it
            if name in links:
                continue

            kind = obj.get("kind", None)

            obj_module_import_path = module_import_path + f".{name}" if module_import_path != "" else name

            # Remove ".functions" from the path, to correspond to the import path
            if ".functions" in obj_module_import_path:
                obj_module_import_path = obj_module_import_path.replace(".functions", "")

            # Create files based on the kind of the data: module/class/function
            if kind == "module":
                template_spec = TemplateReplacementSpec(name=name, link=name, path=obj_module_import_path)
                (dir_root / name).mkdir(exist_ok=True)
                with (dir_root / name / "_index.md").open("w") as f:
                    template_spec.render_template_to_file(MODULE_TEMPLATE_STRING, f)

                # Add entry for url linking
                links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "function"}  # Lowercase for Hugo

            elif kind == "class":
                (dir_root / name).mkdir(exist_ok=True)
                template_spec = TemplateReplacementSpec(
                    name=name, link=name, parent=module_import_path.split(".")[-1], path=obj_module_import_path
                )
                with (dir_root / name / "_index.md").open("w") as f:
                    template_spec.render_template_to_file(CLASS_TEMPLATE_STRING, f)

                # Add entry for url linking
                links[name] = {"path": f"{api_ref_root}/{name}".lower(), "kind": "class"}  # Lowercase for Hugo

            elif name == "functions":
                for func_name in obj:
                    if func_name.startswith("_"):
                        continue  # Skip magic and private methods

                    with (dir_root / f"{func_name}.md").open("w") as f:
                        template_spec = TemplateReplacementSpec(
                            name=func_name,
                            link=func_name,
                            parent=module_import_path.split(".")[-1],
                            path=obj_module_import_path + f".{func_name}",
                        )
                        template_spec.render_template_to_file(FUNCTION_TEMPLATE_STRING, f)

                    # Add entry for url linking
                    links[func_name] = {
                        "path": f"{api_ref_root}/{func_name}".lower(),  # Lowercase for Hugo
                        "kind": "function",
                    }
                continue  # No need to recurse deeper, functions are the last level

            else:
                continue  # Not a class nor a module

            _recursive_create(obj, dir_root / name, f"{api_ref_root}/{name}", obj_module_import_path)

    _recursive_create(data, root, url_root, "")

    return links


def change_json_root(data: dict, json_start_paths: list[str] | None) -> dict:
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


def parse_toml(toml_path: str, version: str, root_directory: str) -> [RefHolder]:
    references = []
    # In case of missing toml_file, we need a default for the api-references
    if not os.path.exists(toml_path):
        return [
            RefHolder(
                url=f"/{version}/api-reference",
                packages=["sdk", "catalog"],
                directory=f"{root_directory}/{version}/api-reference",
            )
        ]
    parsed_toml = toml.load(toml_path)
    for name in parsed_toml:
        packages = parsed_toml[name]["packages"]
        directory = f"{root_directory}/{version}/{parsed_toml[name]['directory']}"
        url = f"/{version}/{parsed_toml[name]['directory']}"
        references.append(RefHolder(url, packages, directory))
    return references


def main():
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument("toml_file", metavar="FILE", help="Paths to toml config file", default="api_spec.toml")
    parser.add_argument("json_file", metavar="FILE", help="Paths to json data file", default="data.json")
    parser.add_argument("version", metavar="str", help="Current Version", default="latest")
    parser.add_argument("root_directory", metavar="str", help="Current Version", default="versioned_docs")

    args = parser.parse_args()

    references = parse_toml(args.toml_file, args.version, args.root_directory)
    links = {}
    for ref in references:
        print(f"Parsing: {ref.url}")
        data = read_json_file(args.json_file)
        data = change_json_root(data, ref.packages)
        links.update(create_file_structure(data, Path(ref.directory), url_root=ref.url))
    with open(f"{args.root_directory}/{args.version}/links.json", "w") as f:
        json.dump(links, f, indent=4)
    print("Dumping the links.json")


if __name__ == "__main__":
    main()
