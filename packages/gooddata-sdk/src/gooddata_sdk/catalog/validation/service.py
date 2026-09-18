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

from gooddata_sdk.catalog.validation.model import Finding, ValidationReport
from gooddata_sdk.catalog.validation.references import (
    ReferenceResolution,
    catalog_object_ids,
    extract_catalog_references,
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
        """Validate one visualization for a target workspace: structure, then references."""
        return self._validate_all(
            [visualization],
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
        visualizations = list(model.analytics.visualization_objects) if model.analytics is not None else []
        return self._validate_all(
            visualizations,
            effective_ids=self._effective_ids(workspace_id),
            known_visualization_urls=known_visualization_urls,
            known_bucket_names=known_bucket_names,
        )

    @staticmethod
    def _validate_all(
        visualizations: list[CatalogDeclarativeVisualizationObject],
        *,
        effective_ids: set[str],
        known_visualization_urls: frozenset[str] | None,
        known_bucket_names: frozenset[str] | None,
    ) -> WorkspaceValidationReport:
        findings: list[Finding] = []
        totals = ReferenceResolution()

        for visualization in visualizations:
            findings.extend(
                visualization.validate(
                    known_visualization_urls=known_visualization_urls,
                    known_bucket_names=known_bucket_names,
                ).findings
            )
            reference_findings, resolution = resolve_references(
                extract_catalog_references(visualization.content),
                effective_ids=effective_ids,
                object_id=visualization.id,
            )
            findings.extend(reference_findings)
            totals.resolved_count += resolution.resolved_count
            totals.unresolved.extend(resolution.unresolved)

        return WorkspaceValidationReport(
            report=ValidationReport(findings=findings),
            resolution=totals,
            objects_checked=len(visualizations),
        )
