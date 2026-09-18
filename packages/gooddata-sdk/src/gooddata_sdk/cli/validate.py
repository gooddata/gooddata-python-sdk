# (C) 2026 GoodData Corporation
"""``gdc validate`` -- check a layout before deploying it.

Deploying the analytics model is a PUT of the whole thing, so the cheapest moment to find
a broken visualization is before that call, not after a dashboard fails to draw. This runs
the same checks the library exposes, over a layout directory, and exits non-zero when
something is provably wrong so it can gate a pipeline.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from gooddata_sdk import GoodDataSdk
from gooddata_sdk.catalog.validation.service import ValidationService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    LAYOUT_VISUALIZATION_OBJECTS_DIR,
    CatalogDeclarativeAnalytics,
    CatalogDeclarativeVisualizationObject,
)
from gooddata_sdk.cli.constants import CONFIG_FILE
from gooddata_sdk.cli.utils import Bcolors


def _load_single_file(path: Path) -> CatalogDeclarativeAnalytics:
    """Wrap one visualization YAML as a model, so both inputs take the same path afterwards.

    The layout writes one file per object named by its id, so a single file is already a
    whole object -- which is what makes validating exactly the thing you edited possible
    without a workspace or the rest of the layout.

    Only visualizations are validated, and every other kind of object is stored in exactly
    the same shape, so a metric file loads as a visualization without complaint and then
    reports every structural key as missing. The directory the layout put it in is what
    distinguishes them, so it is checked before anything is read.
    """
    if path.parent.name != LAYOUT_VISUALIZATION_OBJECTS_DIR:
        raise ValueError(
            f"{path} is not a visualization object: only files under "
            f"'{LAYOUT_VISUALIZATION_OBJECTS_DIR}/' are validated. Point --path at a layout "
            f"directory to check a whole model."
        )
    visualization = CatalogDeclarativeVisualizationObject.load_from_disk(path)
    return CatalogDeclarativeAnalytics.from_dict(
        {"analytics": {"visualizationObjects": [visualization.to_dict(camel_case=True)]}},
        camel_case=True,
    )


def _load(path: Path) -> CatalogDeclarativeAnalytics:
    if path.is_file():
        return _load_single_file(path)
    return CatalogDeclarativeAnalytics.load_from_disk(path)


def _connect(path: Path) -> GoodDataSdk:
    """Connect for the reference checks, preferring a project profile over the environment.

    Environment variables are the fallback rather than an afterthought: validating a single
    file that was checked out on its own is the case this has to serve, and there is no
    project config beside it. ``GOODDATA_HOST``/``GOODDATA_TOKEN`` are the names the rest of
    the monorepo already uses.
    """
    config_path = path if path.is_file() else path / CONFIG_FILE
    if config_path.exists() and config_path.name == CONFIG_FILE:
        return GoodDataSdk.create_from_profile(profiles_path=config_path)

    host, token = os.environ.get("GOODDATA_HOST"), os.environ.get("GOODDATA_TOKEN")
    if host and token:
        return GoodDataSdk.create(host, token)

    try:
        return GoodDataSdk.create_from_profile()
    except (ValueError, FileNotFoundError) as exc:
        raise ValueError(
            "Cannot connect for --workspace checks: no gooddata.yaml beside the layout, no "
            "GOODDATA_HOST/GOODDATA_TOKEN in the environment, and no default profile. Drop "
            "--workspace to run the structural checks, which need no credentials."
        ) from exc


def _print(report_text: str, ok: bool) -> None:
    colour = Bcolors.OKGREEN if ok else Bcolors.FAIL
    print(f"{colour}{report_text}{Bcolors.ENDC}")


def validate(path: Path, args: argparse.Namespace) -> int:
    """Validate a layout directory or a single object file. Returns the process exit code.

    Without ``--workspace`` only the offline checks run: structure and the references
    sorts and filters make inside an object. That is deliberate -- it needs no credentials,
    so it can run on a pull request. Naming a workspace adds the checks that need to know
    where the objects are going, resolving what they reference against everything that
    workspace can see, inherited objects included.
    """
    try:
        model = _load(path)
    except ValueError as exc:
        # A bad --path is the user's mistake, not a crash: exit 2 the way argparse does for
        # a usage error, so a pipeline can tell it apart from content that failed validation.
        print(f"{Bcolors.FAIL}{exc}{Bcolors.ENDC}")
        return 2

    if args.workspace is None:
        report = model.validate()
        _print(report.format(), report.ok)
        if report.ok:
            print(
                f"{Bcolors.WARNING}Structure only. Pass --workspace to also check that the "
                f"metrics, labels and datasets these objects reference exist.{Bcolors.ENDC}"
            )
        return 0 if report.ok else 1

    try:
        sdk = _connect(path)
    except ValueError as exc:
        print(f"{Bcolors.FAIL}{exc}{Bcolors.ENDC}")
        return 2

    result = ValidationService(sdk).validate_analytics_model(args.workspace, model)
    _print(result.format(), result.ok)
    return 0 if result.ok else 1
