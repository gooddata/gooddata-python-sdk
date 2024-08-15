# (C) 2023 GoodData Corporation
import argparse
from pathlib import Path

import tomlkit

_ROOT_DIR = Path(__file__).resolve().parent.parent

_TOML_FILE = _ROOT_DIR / "docs/config/production/params.toml"
_REDIR_FILE = _ROOT_DIR / "docs/layouts/index.redir"


def bump_toml(file_path: Path, version: list[int]):
    if version[2] != 0:
        print("params.toml not updated for hotfixes.")
        return

    short_version = f"{version[0]}.{version[1]}"

    # Load the TOML file
    with open(file_path) as file:
        content = file.read()
    data = tomlkit.parse(content)

    versions = data.get("versions", [])

    old_version = versions[1]["version"]
    versions[1]["dirpath"] = old_version
    versions[1]["url"] = f"/{old_version}/"

    # Add the new version
    new_version_data = tomlkit.table()
    new_version_data["version"] = short_version
    new_version_data["dirpath"] = "latest"
    new_version_data["url"] = "/latest/"
    versions.insert(1, new_version_data)

    # Pop the last version
    versions.pop()

    with open(file_path, "w") as file:
        file.write(tomlkit.dumps(data))


def bump_redir(file_path: Path, version: list[int]):
    long_version = f"{version[0]}.{version[1]}.{version[2]}"
    short_version = f"{version[0]}.{version[1]}"
    with open(file_path) as file:
        content = file.readlines()

    if version[2] == 0:
        line_to_delete = -1
        for i, line in enumerate(content):
            if line.endswith("/latest 301!\n"):
                parts = line.split(" ")
                if len(parts[0].split(".")) == 2:
                    line_to_delete = i
                else:
                    old_short_version = f"{parts[0][:-3]}"
                    content[i] = content[i].replace("/latest", old_short_version)

        if line_to_delete != -1:
            content.remove(content[line_to_delete])

        content.insert(3, f"/{long_version}/ {{{{ .Site.BaseURL }}}}/latest 301!\n")

        content.insert(3, f"/{short_version}/ {{{{ .Site.BaseURL }}}}/latest 301!\n")

    else:
        content.insert(4, f"/{long_version}/ {{{{ .Site.BaseURL }}}}/latest 301!\n")
    with open(file_path, "w") as file:
        file.writelines(content)


def main():
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument("version", help="root directory of the output")
    args = parser.parse_args()
    x, y, z = map(int, args.version.split("."))
    bump_toml(file_path=_TOML_FILE, version=[x, y, z])
    bump_redir(file_path=_REDIR_FILE, version=[x, y, z])


if __name__ == "__main__":
    main()
