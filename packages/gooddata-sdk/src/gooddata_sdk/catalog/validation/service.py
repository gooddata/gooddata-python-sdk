# (C) 2026 GoodData Corporation
"""Validating declarative objects against a live workspace.

The offline checks answer from the object alone; these answer "is this object valid *for
this workspace*", which is a different question and the one that matters before a deploy.
A layout built against a parent can be perfectly well-formed and still unusable in a
workspace that does not inherit the metrics it names.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from gooddata_sdk.catalog.validation.layout import LAYOUT_REFERENCE_TYPES, object_references
from gooddata_sdk.catalog.validation.model import ValidationReport
from gooddata_sdk.catalog.validation.references import (
    ReferenceResolution,
    catalog_object_ids,
    resolve_references,
)

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
        CatalogDeclarativeAnalytics,
        CatalogDeclarativeVisualizationObject,
    )
    from gooddata_sdk.sdk import GoodDataSdk


@define(kw_only=True)
class WorkspaceValidationReport:
    """A validation report plus what resolving against the workspace actually found.

    The counts are carried alongside the findings because a report that only says "no
    problems" gives a reader no way to tell a thorough check from one that checked nothing:
    an empty layout and a fully valid one both produce no findings, and only the counts
    distinguish them.
    """

    report: ValidationReport = field(factory=ValidationReport)
    resolution: ReferenceResolution = field(factory=ReferenceResolution)
    objects_checked: int = 0

    @property
    def ok(self) -> bool:
        return self.report.ok

    def __bool__(self) -> bool:
        return self.ok

    def format(self) -> str:
        return "\n".join(
            [
                f"{self.objects_checked} object(s) checked against the workspace's effective "
                f"catalog (inherited objects included), {self.resolution.summary()}.",
                self.report.format(),
            ]
        )


class ValidationService:
    """Validates declarative objects against a workspace, inheritance included.

    Constructed with an SDK because the question needs the server: what a workspace can
    actually see spans its inheritance chain, and a layout file shows only what one
    workspace owns.
    """

    def __init__(self, sdk: GoodDataSdk) -> None:
        self._sdk = sdk

    def _effective_ids(self, workspace_id: str) -> set[str]:
        """Everything the workspace can see, its inheritance chain included.

        One call, and deliberately the *effective* catalog rather than the workspace's own
        declarative model: a child owns almost nothing and inherits the rest, so its own
        model is not the set its content has to resolve against.
        """
        return catalog_object_ids(self._sdk.catalog_workspace_content.get_full_catalog(workspace_id))

    def validate_visualization(
        self,
        workspace_id: str,
        visualization: CatalogDeclarativeVisualizationObject,
        *,
        known_visualization_urls: frozenset[str] | None = None,
        known_bucket_names: frozenset[str] | None = None,
    ) -> WorkspaceValidationReport:
        """Validate one visualization for a target workspace: structure, then references.

        Wrapped as a one-object model so it takes exactly the path a whole layout does --
        the checks that matter for a single object are the same ones, and keeping two
        implementations is how they drift apart.
        """
        from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (  # noqa: PLC0415
            CatalogDeclarativeAnalytics as _Model,
        )

        model = _Model.from_dict(
            {"analytics": {"visualizationObjects": [visualization.to_dict(camel_case=True)]}}, camel_case=True
        )
        return self._validate_model(
            model,
            effective_ids=self._effective_ids(workspace_id),
            known_visualization_urls=known_visualization_urls,
            known_bucket_names=known_bucket_names,
        )

    def validate_analytics_model(
        self,
        workspace_id: str,
        model: CatalogDeclarativeAnalytics,
        *,
        known_visualization_urls: frozenset[str] | None = None,
        known_bucket_names: frozenset[str] | None = None,
    ) -> WorkspaceValidationReport:
        """Validate every visualization in a model against a target workspace.

        The model is usually one loaded from disk and about to be deployed, and the target
        need not be the workspace it came from -- checking a layout against where it is
        *going* is the point.
        """
        return self._validate_model(
            model,
            effective_ids=self._effective_ids(workspace_id),
            known_visualization_urls=known_visualization_urls,
            known_bucket_names=known_bucket_names,
        )

    @staticmethod
    def _validate_model(
        model: CatalogDeclarativeAnalytics,
        *,
        effective_ids: set[str],
        known_visualization_urls: frozenset[str] | None,
        known_bucket_names: frozenset[str] | None,
    ) -> WorkspaceValidationReport:
        """Everything the files can answer, plus every reference resolved against the target.

        References are collected from every kind that makes them -- visualizations and
        dashboards through their identifier nodes, metrics out of their MAQL -- rather than
        from visualizations alone. Metrics usually outnumber everything else in a workspace,
        and theirs are the references most likely to dangle after a migration.

        Layout references are excluded here and left to the layout check: a dashboard naming
        a visualization is asking about an object in the layout, not in the catalog, and
        resolving it against the catalog would report every dashboard in a child workspace.
        """
        report = model.validate(
            known_visualization_urls=known_visualization_urls,
            known_bucket_names=known_bucket_names,
        )
        totals = ReferenceResolution()

        catalog_refs = [
            (object_id, reference)
            for object_id, reference in object_references(model)
            if reference.type not in LAYOUT_REFERENCE_TYPES
        ]
        for object_id, reference in catalog_refs:
            findings, resolution = resolve_references([reference], effective_ids=effective_ids, object_id=object_id)
            report.extend(findings)
            totals.resolved_count += resolution.resolved_count
            totals.unresolved.extend(resolution.unresolved)

        objects_checked = (
            sum(
                len(getattr(model.analytics, name, []) or [])
                for name in ("visualization_objects", "analytical_dashboards", "metrics", "filter_contexts")
            )
            if model.analytics is not None
            else 0
        )
        return WorkspaceValidationReport(report=report, resolution=totals, objects_checked=objects_checked)
