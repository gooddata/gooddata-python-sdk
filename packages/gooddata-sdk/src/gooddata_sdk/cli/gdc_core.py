# (C) 2024 GoodData Corporation
import argparse
import sys
from pathlib import Path

from gooddata_sdk.cli.clone import clone_all, clone_granular
from gooddata_sdk.cli.constants import CONFIG_FILE, DEFAULT_SOURCE_DIR
from gooddata_sdk.cli.deploy import deploy_all, deploy_granular
from gooddata_sdk.cli.utils import _SUPPORTED, Bcolors
from gooddata_sdk.config import AacConfig
from gooddata_sdk.utils import read_layout_from_file


def _find_config_file() -> Path:
    """Find the gooddata.yaml config file in the current directory or parents."""
    current = Path.cwd()
    for directory in [current, *current.parents]:
        config_path = directory / CONFIG_FILE
        if config_path.exists():
            return config_path
    print(f"{Bcolors.FAIL}Config file {CONFIG_FILE} was not found.{Bcolors.ENDC}")
    sys.exit(1)


def _get_source_dir(config_path: Path) -> str:
    """Get source_dir from config file, falling back to default."""
    content = read_layout_from_file(config_path)
    if isinstance(content, dict) and AacConfig.can_structure(content):
        config = AacConfig.from_dict(content)
        if config.source_dir is not None:
            return config.source_dir
    return DEFAULT_SOURCE_DIR


def _deploy(path: Path, source_dir: str, args: argparse.Namespace) -> None:
    if not path.is_dir():
        raise ValueError(f"Path {path} is not a directory.")
    if args.only is None:
        deploy_all(path, source_dir)
    else:
        deploy_granular(path, source_dir, args)


def _clone(path: Path, source_dir: str, args: argparse.Namespace) -> None:
    if args.only is None:
        clone_all(path, source_dir)
    else:
        clone_granular(path, source_dir, args)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gdc",
        description="GoodData CLI for deploying and cloning analytics-as-code projects.",
    )
    parser.add_argument("action", help="Specify if you want to deploy or clone project.", choices=("deploy", "clone"))
    parser.add_argument("--only", help="Specify available granularity for action.", nargs="+", choices=_SUPPORTED)

    args = parser.parse_args()
    config_path = _find_config_file()
    manifest_directory = config_path.parent
    source_dir = _get_source_dir(config_path)

    if args.action == "clone":
        _clone(manifest_directory, source_dir, args)
    elif args.action == "deploy":
        _deploy(manifest_directory, source_dir, args)


if __name__ == "__main__":
    main()
