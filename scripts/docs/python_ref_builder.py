# (C) 2023 GoodData Corporation
import argparse
import json
from pathlib import Path
from typing import List, TextIO

from attr import define

MODULE_TEMPLATE_STRING = Path("module_template.md").read_text()
CLASS_TEMPLATE_STRING = Path("class_template.md").read_text()
FUNCTION_TEMPLATE_STRING = Path("function_template.md").read_text()


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

    def _recursive_create(data_root: dict, dir_root: Path, url_root: str, module_import_path: str):
        """Recursively create files and directories.

        Args:
            data_root (dict): Sub-dictionary of the JSON representing the object.
            dir_root (Path): Path to the directory root.
            url_root (str): URL root path for the API reference.
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
                links[name] = {"path": f"{url_root}/{name}".lower(), "kind": "function"}  # Lowercase for Hugo

            elif kind == "class":
                (dir_root / name).mkdir(exist_ok=True)
                template_spec = TemplateReplacementSpec(
                    name=name, link=name, parent=module_import_path.split(".")[-1], path=obj_module_import_path
                )
                with (dir_root / name / "_index.md").open("w") as f:
                    template_spec.render_template_to_file(CLASS_TEMPLATE_STRING, f)

                # Add entry for url linking
                links[name] = {"path": f"{url_root}/{name}".lower(), "kind": "class"}  # Lowercase for Hugo

            elif name == "functions":
                for func_name, func in obj.items():
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
                        "path": f"{url_root}/{func_name}".lower(),  # Lowercase for Hugo
                        "kind": "function",
                    }
                continue  # No need to recurse deeper, functions are the last level

            else:
                continue  # Not a class nor a module

            _recursive_create(obj, dir_root / name, f"{url_root}/{name}", obj_module_import_path)

    _recursive_create(data, root, url_root, "")

    return links


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


def main():
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument("file", metavar="FILE", help="path to the JSON file", default="data.json")
    parser.add_argument("output", metavar="FILE", help="root directory of the output", default="apiref")
    parser.add_argument(
        "--json_start_path",
        default="",
        required=False,
        nargs="*",
        help="Example: sdk.CatalogUserService, "
        "would only generate markdown tree for that object,"
        "can use multiple start paths, by including the argument multiple times",
    )
    parser.add_argument("--url_root", default="", required=False, help="url root path for the apiref")
    args = parser.parse_args()
    print(f"Json start path is f{args.json_start_path}")

    file_path = args.file
    data = read_json_file(file_path)
    data = change_json_root(data, args.json_start_path)
    links = create_file_structure(data, Path(args.output), url_root=args.url_root)
    json.dump(links, open("links.json", "w"), indent=4)
    print("Dumping the links.json")


if __name__ == "__main__":
    main()
