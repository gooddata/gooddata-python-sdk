# (C) 2023 GoodData Corporation
import sys
import tomllib
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parent.parent


def get_version(content: dict) -> list[int]:
    current_version = content.get("tool", {}).get("tbump", {}).get("version", {}).get("current")
    if current_version is None:
        raise ValueError("No current version found while reading from pyproject.toml")
    return list(map(int, current_version.split(".")))


if __name__ == "__main__":
    bump_type = sys.argv[1]
    with open(_ROOT_DIR / "pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    version = get_version(data)
    match bump_type:
        case "patch":
            version[2] += 1
        case "minor":
            version[1] += 1
            version[2] = 0
        case "major":
            version[0] += 1
            version[1] = 0
            version[2] = 0
        case _:
            raise ValueError("Invalid bump type")
    print(".".join(list(map(str, version))))
