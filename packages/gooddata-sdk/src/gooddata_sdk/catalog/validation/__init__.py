# (C) 2026 GoodData Corporation
"""Validation of declarative analytics objects before they are deployed.

The metadata API stores a visualization's ``content`` as a free-form JSON object: it is
checked for being an object and for its length, and nothing else. The structure the
renderer actually requires -- buckets, their local identifiers, the references between
sorts/filters and bucket items -- is not part of that contract, so an object that no
frontend can draw is stored without complaint and fails later, one insight at a time.

This package closes that gap on the client side, for the paths that go through the SDK.
It reports rather than enforces: see :class:`Severity` for what separates the two levels
and why the distinction matters when the format gains a chart type the SDK has not heard
of yet.
"""

from gooddata_sdk.catalog.validation.buckets import (
    BUCKET_NAMES,
    BUCKETS_BY_VISUALIZATION,
    VISUALIZATION_NAMES,
    VISUALIZATION_URLS,
    check_buckets_for_visualization_type,
)
from gooddata_sdk.catalog.validation.catalog_from_layout import catalog_ids_from_layout, catalog_ids_from_ldm
from gooddata_sdk.catalog.validation.files import check_layout_files
from gooddata_sdk.catalog.validation.layout import validate_layout
from gooddata_sdk.catalog.validation.ldm import validate_ldm
from gooddata_sdk.catalog.validation.maql import extract_maql_references
from gooddata_sdk.catalog.validation.model import Finding, Severity, ValidationError, ValidationReport
from gooddata_sdk.catalog.validation.plan import DeployPlan, build_deploy_plan, plan_deploy
from gooddata_sdk.catalog.validation.properties import check_properties, extract_properties_references
from gooddata_sdk.catalog.validation.references import (
    CatalogReference,
    ReferenceResolution,
    catalog_object_ids,
    extract_catalog_references,
    resolve_references,
)
from gooddata_sdk.catalog.validation.service import ValidationService, WorkspaceValidationReport
from gooddata_sdk.catalog.validation.visualization import TOTAL_TYPES

__all__ = [
    "BUCKETS_BY_VISUALIZATION",
    "BUCKET_NAMES",
    "CatalogReference",
    "DeployPlan",
    "Finding",
    "ReferenceResolution",
    "Severity",
    "ValidationError",
    "ValidationReport",
    "ValidationService",
    "TOTAL_TYPES",
    "VISUALIZATION_NAMES",
    "VISUALIZATION_URLS",
    "WorkspaceValidationReport",
    "build_deploy_plan",
    "check_buckets_for_visualization_type",
    "catalog_ids_from_layout",
    "catalog_ids_from_ldm",
    "catalog_object_ids",
    "check_layout_files",
    "check_properties",
    "extract_catalog_references",
    "extract_maql_references",
    "extract_properties_references",
    "plan_deploy",
    "resolve_references",
    "validate_layout",
    "validate_ldm",
]
