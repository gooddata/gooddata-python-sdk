# (C) 2026 GoodData Corporation
"""``gdc validate`` -- check a layout before deploying it.

Deploying the analytics model is a PUT of the whole thing, so the cheapest moment to find
a broken visualization is before that call, not after a dashboard fails to draw. This runs
the same checks the library exposes, over a layout directory, and exits non-zero when
something is provably wrong so it can gate a pipeline.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from gooddata_sdk import GoodDataSdk
from gooddata_sdk.catalog.validation.catalog_from_layout import catalog_ids_from_layout
from gooddata_sdk.catalog.validation.files import check_layout_files
from gooddata_sdk.catalog.validation.layout import LAYOUT_REFERENCE_TYPES, object_references
from gooddata_sdk.catalog.validation.ldm import validate_ldm
from gooddata_sdk.catalog.validation.model import ValidationReport
from gooddata_sdk.catalog.validation.plan import plan_deploy
from gooddata_sdk.catalog.validation.references import ReferenceResolution, resolve_references
from gooddata_sdk.catalog.validation.service import ValidationService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    LAYOUT_ANALYTICS_MODEL_DIR,
    LAYOUT_VISUALIZATION_OBJECTS_DIR,
    CatalogDeclarativeAnalytics,
    CatalogDeclarativeVisualizationObject,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    LAYOUT_LDM_DIR,
    CatalogDeclarativeModel,
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
    """Load a layout directory or a single object file, refusing anything that is neither.

    The guards matter more than they look. ``load_from_disk`` creates the layout's
    directories as it walks, so pointing it at a path that is not a layout silently *makes*
    one, finds nothing in it, and reports a clean bill of health -- a validator's worst
    failure mode, since it looks exactly like success. A read-only command has no business
    writing anything, so the shape of the path is checked before it is read.
    """
    if not path.exists():
        raise ValueError(f"{path} does not exist.")
    if path.is_file():
        return _load_single_file(path)
    if not (path / LAYOUT_ANALYTICS_MODEL_DIR).is_dir():
        raise ValueError(
            f"{path} is not a layout directory: expected a '{LAYOUT_ANALYTICS_MODEL_DIR}/' "
            f"folder inside it. Point --path at the workspace folder a layout was stored "
            f"into, or at a single visualization YAML."
        )
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


def _emit_json(
    report: ValidationReport,
    *,
    path: Path,
    objects_checked: int,
    workspace_id: str | None,
    resolution: ReferenceResolution | None = None,
) -> None:
    """Print the whole run as one JSON object on stdout.

    Exit codes say whether a run passed; they cannot say what failed. Anything that wants
    to annotate a pull request, count findings by code over time, or fail only on a
    particular check needs the findings themselves, and parsing the human output would make
    its wording an API.

    Colour is deliberately not applied: this goes through a pipe.
    """
    payload: dict[str, Any] = {
        "path": str(path),
        "workspace": workspace_id,
        "objectsChecked": objects_checked,
        **report.to_dict(),
    }
    if resolution is not None:
        payload["references"] = {
            "resolved": resolution.resolved_count,
            "unresolved": [
                {"objectId": reference.obj_id, "location": reference.location} for reference in resolution.unresolved
            ],
        }
    print(json.dumps(payload, indent=2))


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

    # File-level and logical-model checks run on a directory only: both answer questions
    # about the layout as a whole, which a single object file cannot raise.
    file_findings = check_layout_files(path / LAYOUT_ANALYTICS_MODEL_DIR) if path.is_dir() else []

    # The logical model is validated alongside the analytics model, not instead of it:
    # every metric and visualization stands on the joins declared there, so a layout whose
    # analytics model is spotless is still broken if its LDM is not.
    ldm_findings = []
    ldm_datasets = 0
    ldm_model = None
    if path.is_dir() and (path / LAYOUT_LDM_DIR).is_dir():
        ldm_model = CatalogDeclarativeModel.load_from_disk(path)
        ldm_findings = validate_ldm(ldm_model)
        ldm_datasets = len(ldm_model.ldm.datasets) if ldm_model.ldm is not None else 0

    # Counted across every kind the checks actually look at, not visualizations alone:
    # reporting 1302 when 4757 objects were read understates the work and makes a clean
    # result look narrower than it is.
    checked = (
        sum(
            len(getattr(model.analytics, name, []) or [])
            for name in ("visualization_objects", "analytical_dashboards", "metrics", "filter_contexts")
        )
        if model.analytics is not None
        else 0
    )
    checked += ldm_datasets
    as_json = getattr(args, "json", False)

    if checked == 0:
        # Distinguished from success on purpose: "nothing was wrong" and "nothing was looked
        # at" print the same way otherwise, and the second is usually a wrong --path.
        if as_json:
            _emit_json(ValidationReport(), path=path, objects_checked=0, workspace_id=args.workspace)
        else:
            print(f"{Bcolors.WARNING}No objects found under {path}. Nothing to validate.{Bcolors.ENDC}")
        return 0

    if args.workspace is None:
        report = model.validate().extend(file_findings).extend(ldm_findings)
        # A layout carrying its own logical model can answer whether the metrics, labels
        # and datasets it names exist, without a server: the LDM is where those objects are
        # declared. Skipped when the layout has no LDM, because then the absence of an
        # object says only that this layout does not define it.
        offline_resolution = None
        if ldm_model is not None:
            available = catalog_ids_from_layout(model, ldm_model)
            for object_id, reference in object_references(model):
                if reference.type in LAYOUT_REFERENCE_TYPES:
                    continue
                findings, resolution = resolve_references(
                    [reference],
                    effective_ids=available,
                    object_id=object_id,
                    scope="this layout's logical model",
                )
                report.extend(findings)
                if offline_resolution is None:
                    offline_resolution = ReferenceResolution()
                offline_resolution.resolved_count += resolution.resolved_count
                offline_resolution.unresolved.extend(resolution.unresolved)
        if as_json:
            _emit_json(
                report,
                path=path,
                objects_checked=checked,
                workspace_id=None,
                resolution=offline_resolution,
            )
            return 0 if report.ok else 1

        headline = f"{checked} object(s) checked."
        if offline_resolution is not None:
            headline += f" {offline_resolution.summary()} against the layout's own logical model."
        _print(f"{headline}\n{report.format()}", report.ok)
        if report.ok and offline_resolution is None:
            print(
                f"{Bcolors.WARNING}Structure only -- this layout carries no logical model, so "
                f"whether the metrics, labels and datasets it references exist could not be "
                f"checked. Pass --workspace for that.{Bcolors.ENDC}"
            )
        return 0 if report.ok else 1

    try:
        sdk = _connect(path)
    except ValueError as exc:
        print(f"{Bcolors.FAIL}{exc}{Bcolors.ENDC}")
        return 2

    result = ValidationService(sdk).validate_analytics_model(args.workspace, model)
    result.report.extend(file_findings).extend(ldm_findings)

    if as_json:
        _emit_json(
            result.report,
            path=path,
            objects_checked=result.objects_checked + ldm_datasets,
            workspace_id=args.workspace,
            resolution=result.resolution,
        )
        return 0 if result.ok else 1

    _print(result.format(), result.ok)

    if getattr(args, "plan", False):
        print()
        print(plan_deploy(sdk, args.workspace, model).format())

    return 0 if result.ok else 1
