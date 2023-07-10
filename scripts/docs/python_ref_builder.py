import argparse
import json
from pathlib import Path

# Template variables:
#   PATH: replace with path to object
#   NAME: replace with name of the object
#   PARENT: replace with parent name (only for functions)
MODULE_TEMPLATE_STRING = open("module_template.md").read()
CLASS_TEMPLATE_STRING = open("class_template.md").read()
FUNCTION_TEMPLATE_STRING = open("function_template.md").read()


def process_json_file(file_path) -> dict:
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def create_file_structure(data: dict, root: Path, url_root: str):
    links = {}

    def _recursive_create(data_root: dict, dir_root: Path, url_root: str, module_import_path: str):
        """
        :param data_root: Sub-dictionary of the original json representing the object
        :param dir_root: Path to the corresponding directory root Ex.: Path("./sdk/compute")
        :param module_import_path: Import path to the object Ex.: "sdk.compute"
        :return:
        """
        dir_root.mkdir(exist_ok=True)
        for name, obj in data_root.items():
            if not isinstance(obj, dict):
                continue
            kind = obj.get("kind", None)

            obj_module_import_path = module_import_path + f".{name}" if module_import_path != "" else name

            # Remove ".functions" from the path, to correspond to the import path
            if ".functions" in obj_module_import_path:
                obj_module_import_path = obj_module_import_path.replace(".functions", "")

            if kind == "module":
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    MODULE_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                    .replace("NAME", name)
                )
                links[name] = {
                    "path": f"{url_root}/{name}".lower(),  # Lowercase for Hugo
                    "kind": "function"
                }
            elif kind == "class":
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    CLASS_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                    .replace("NAME", name)
                )
                links[name] = {
                    "path": f"{url_root}/{name}".lower(),  # Lowercase for Hugo
                    "kind": "class"
                }
            elif name == "functions":
                for func_name, func in obj.items():
                    (dir_root / f"{func_name}.md").open("w+").write(
                        FUNCTION_TEMPLATE_STRING
                            .replace("PATH", obj_module_import_path + f".{func_name}")
                            .replace("NAME", func_name)
                            .replace("PARENT", module_import_path.split(".")[-1])
                    )
                    links[func_name] = {
                        "path": f"{url_root}/{func_name}".lower(),  # Lowercase for Hugo
                        "kind": "function"
                    }
                continue  # No need to recurse deeper

            else:
                continue  # Not a class nor a module

            _recursive_create(obj, dir_root / name, f"{url_root}/{name}", obj_module_import_path)

    _recursive_create(data, root, url_root, "")

    return links


def change_json_root(data: dict, json_start_path: str) -> dict:
    """
    Change the root of the json data to the specified path

    Example
    input:
        data:
        "root": {
            "sdk": {sdk-data}
            "other": {...}
            }
        json_start_path: "root.sdk"
    output:
        "sdk": sdk-data

    :param data: dict with the module data
    :param json_start_path: path to the object in the json data
    :return:
    """
    if json_start_path:
        for part in json_start_path.split("."):
            data = data[part]
        return {json_start_path.split(".")[-1]: data}
    return data


def main():
    parser = argparse.ArgumentParser(description='Process a JSON file')
    parser.add_argument('file', metavar='FILE', help='path to the JSON file', default="data.json")
    parser.add_argument('output', metavar='FILE', help='root directory of the output', default="apiref")
    parser.add_argument('--json_start_path', default="", required=False,
                        help="Example: sdk.CatalogUserService, "
                             "would only generate markdown tree for that object")
    parser.add_argument('--url_root', default="", required=False,
                        help="url root path for the apiref")
    args = parser.parse_args()

    file_path = args.file
    data = process_json_file(file_path)
    data = change_json_root(data, args.json_start_path)
    links = create_file_structure(data, Path(args.output), url_root=args.url_root)
    json.dump(links, open("links.json", "w+"), indent=4)


main()
