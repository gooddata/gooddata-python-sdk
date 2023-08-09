import argparse
import json
from pathlib import Path
from typing import List, Optional

MODULE_TEMPLATE_STRING = Path("module_template.md").read_text()
CLASS_TEMPLATE_STRING = Path("class_template.md").read_text()
FUNCTION_TEMPLATE_STRING = Path("function_template.md").read_text()


def shorten_name(name: str, max_len: int = 30) -> str:
    """Shorten the name of the object, if it is too long.

    Args:
        name (str): The name to be shortened.
        max_len (int, optional): Maximum length of the name. Defaults to 30.

    Returns:
        str: The shortened name.
    """
    if len(name) > max_len:
        return name[: max_len - 3] + "..."
    return name


def process_json_file(file_path: str) -> dict:
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
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    MODULE_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                    .replace("NAME", name)
                    .replace("LINK", shorten_name(name))
                )
                links[name] = {"path": f"{url_root}/{name}".lower(), "kind": "function"}  # Lowercase for Hugo
            elif kind == "class":
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    CLASS_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                    .replace("NAME", name)
                    .replace("LINK", shorten_name(name))
                    .replace("PARENT", module_import_path.split(".")[-1])
                )
                links[name] = {"path": f"{url_root}/{name}".lower(), "kind": "class"}  # Lowercase for Hugo
            elif name == "functions":
                for func_name, func in obj.items():
                    if func_name.startswith("_"):
                        continue  # Skip magic and private methods

                    (dir_root / f"{func_name}.md").open("w+").write(
                        FUNCTION_TEMPLATE_STRING.replace("PATH", obj_module_import_path + f".{func_name}")
                        .replace("NAME", func_name)
                        .replace("LINK", shorten_name(func_name))
                        .replace("PARENT", module_import_path.split(".")[-1])
                    )
                    links[func_name] = {
                        "path": f"{url_root}/{func_name}".lower(),  # Lowercase for Hugo
                        "kind": "function",
                    }
                continue  # No need to recurse deeper

            else:
                continue  # Not a class nor a module

            _recursive_create(obj, dir_root / name, f"{url_root}/{name}", obj_module_import_path)

    _recursive_create(data, root, url_root, "")

    return links


def change_json_root(data: dict, json_start_paths: Optional[List[str]]) -> dict:
    """Change the root of the JSON data to the specified path.

    Args:
        data (dict): Dict with the module data.
        json_start_paths (Optional[List[str]]): Paths to the object in the JSON data.

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
    data = process_json_file(file_path)
    data = change_json_root(data, args.json_start_path)
    links = create_file_structure(data, Path(args.output), url_root=args.url_root)
    json.dump(links, open("links.json", "w+"), indent=4)


main()
