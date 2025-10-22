# (C) 2024 GoodData Corporation
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from gooddata_sdk.cli.clone import clone_all, clone_granular
from gooddata_sdk.cli.constants import GD_COMMAND, GD_PACKAGE_JSON, GD_ROOT
from gooddata_sdk.cli.deploy import deploy_all, deploy_granular
from gooddata_sdk.cli.utils import _SUPPORTED, Bcolors
from gooddata_sdk.utils import read_json

_CURRENT_DIR = Path(__file__).parent


def get_manifest_directory() -> Path:
    """
    Get the directory where the manifest file (gooddata.yaml) is located
    using the gd stream-manifest-path command.
    """
    p = subprocess.Popen(
        [GD_COMMAND, "stream-manifest-path"],
        cwd=Path().resolve(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, err = p.communicate()
    if err:
        print(f"{Bcolors.FAIL}Manifest gooddata.yaml was not found.{Bcolors.ENDC}")
        sys.exit(1)
    return Path(output.decode()).parent


def _deploy(path: Path, args: argparse.Namespace) -> None:
    """
    Handles deploy command use cases.
    """
    if not path.is_dir():
        raise ValueError(f"Path {path} is not a directory.")

    if args.only is None:
        deploy_all(path)
    else:
        deploy_granular(path, args)


def _clone(path: Path, args: argparse.Namespace) -> None:
    """
    Handles clone command use cases.
    """
    if args.only is None:
        clone_all(path)
    else:
        clone_granular(path, args)


def _manage_node_cli() -> None:
    """
    First, it checks if Node CLI is installed and if it is the correct version.
    If not, it installs the correct version. If it is not installed at all then it's installed
    locally in ~/.gooddata directory.
    """
    requested_version = read_json(_CURRENT_DIR / "package.json")["dependencies"]["@gooddata/code-cli"]
    if GD_PACKAGE_JSON.exists():
        current_version = read_json(GD_PACKAGE_JSON)["version"]
        if current_version == requested_version:
            return
        else:
            print(
                f"Node.js @gooddata/code-cli version '{requested_version}' is required,"
                f" but version '{current_version}' is installed."
            )
    if not GD_ROOT.exists():
        GD_ROOT.mkdir()
    shutil.copyfile(_CURRENT_DIR / "package.json", GD_ROOT / "package.json")
    print(f"Installing @gooddata/code-cli version '{requested_version}' in {GD_ROOT}...")
    p = subprocess.Popen(
        ["npm", "i"],
        cwd=GD_ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _, err = p.communicate()
    if err:
        print(f"{Bcolors.FAIL}An error has occurred during installation: {err.decode()}.{Bcolors.ENDC}")
        sys.exit(1)


def main(cli_args: list[str]) -> None:
    """
    The entrypoint for gdc cli.
    """
    parser = argparse.ArgumentParser(
        prog="gdc",
        description="Process GoodData as code file structure. Utilize @gooddata/code-cli for workspaces. "
        "Note that this is an EXPERIMENTAL feature.",
    )
    parser.add_argument("action", help="Specify if you want to deploy or clone project.", choices=("deploy", "clone"))
    parser.add_argument("--only", help="Specify available granularity for action.", nargs="+", choices=_SUPPORTED)

    _manage_node_cli()
    args = parser.parse_args(cli_args)
    manifest_directory = get_manifest_directory()
    if args.action == "clone":
        _clone(manifest_directory, args)
    elif args.action == "deploy":
        _deploy(manifest_directory, args)


if __name__ == "__main__":
    main(sys.argv[1:])
