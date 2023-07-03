import argparse
import json
from pathlib import Path

# Template variables:
#   PATH: replace with path to object
MODULE_TEMPLATE_STRING = open("module_template.md").read()
CLASS_TEMPLATE_STRING = open("class_template.md").read()


def process_json_file(file_path) -> dict:
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def create_file_structure(data: dict, root: Path):
    def _recursive_create(data_root: dict, dir_root: Path, module_import_path: str):
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

            if kind == "module":
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    MODULE_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                )
            elif kind == "class":
                (dir_root / name).mkdir(exist_ok=True)
                (dir_root / name / "_index.md").open("w+").write(
                    CLASS_TEMPLATE_STRING.replace("PATH", obj_module_import_path)
                )
            else:
                continue  # Not a class nor a module

            _recursive_create(obj, dir_root / name, obj_module_import_path)

    _recursive_create(data, root, "")

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file')
    parser.add_argument('file', metavar='FILE', help='path to the JSON file', default="data.json")
    parser.add_argument('output', metavar='FILE', help='root directory of the output', default="apiref")
    args = parser.parse_args()

    file_path = args.file
    data = process_json_file(file_path)
    create_file_structure(data, Path(args.output))

main()
