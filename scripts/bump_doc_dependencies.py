# (C) 2023 GoodData Corporation
import argparse
from pathlib import Path

import tomlkit

_CURRENT_DIR = Path.cwd()

_TOML_FILE = _CURRENT_DIR / "docs/config/production/params.toml"
_REDIR_FILE = _CURRENT_DIR / "docs/layouts/index.redir"


def bump_toml(file_path: Path, version: list[int]):
    if version[2] != 0:
        print("params.toml not updated for hotfixes.")
        return

    short_version = f"{version[0]}.{version[1]}"

    # Load the TOML file
    with open(file_path, "r") as file:
        content = file.read()
    data = tomlkit.parse(content)

    versions = data.get("versions", [])

    # Remove the old version
    if versions:
        versions.pop()

    # Add the new version
    new_version_data = tomlkit.table()
    new_version_data["version"] = short_version
    new_version_data["dirpath"] = short_version
    new_version_data["url"] = f"/{short_version}/"
    versions.insert(1, new_version_data)

    with open(file_path, "w") as file:
        file.write(tomlkit.dumps(data))


def bump_redir(file_path: Path, version: list[int]):
    long_version = f"{version[0]}.{version[1]}.{version[2]}"
    short_version = f"{version[0]}.{version[1]}"

    new_redirect_rule = f"/{long_version}/ {{{{ .Site.BaseURL }}}}/{short_version} 301!\n"

    with open(file_path, "r") as file:
        content = file.readlines()

    content.insert(4, new_redirect_rule)

    if version[2] == 0:
        indices_to_replace = [1, 2, 3]
        new_lines = [
            f"/ {{{{ .Site.BaseURL }}}}/{short_version}/ 301!",
            f"/latest/ {{{{ .Site.BaseURL }}}}/{short_version}/ 301",
            f"/docs/ {{{{ .Site.BaseURL }}}}/{short_version}/ 301!",
        ]

        for i, new_line in zip(indices_to_replace, new_lines):
            content[i] = new_line + "\n"

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
