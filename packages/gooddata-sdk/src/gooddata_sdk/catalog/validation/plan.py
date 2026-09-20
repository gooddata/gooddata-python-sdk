# (C) 2026 GoodData Corporation
"""What deploying a layout would actually do to a workspace.

Deploying the analytics model is a ``PUT`` of the whole model: the workspace's own objects
are replaced by the ones in the payload, so an object the workspace has and the layout does
not is **deleted**. Nothing warns about that. A migration is exactly when the local copy is
most likely to be incomplete -- a partial export, a filtered checkout, a merge that dropped
a folder -- and the deletions are silent and not undoable.

This answers the question before the call: what is created, what is updated, and what
disappears. It is not validation and reports no findings; it describes a consequence.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
        CatalogDeclarativeAnalytics,
    )
    from gooddata_sdk.sdk import GoodDataSdk

# The collections a deploy replaces. Kept explicit so a collection the SDK gains later is
# absent from the plan rather than silently assumed to behave like the others.
_COLLECTIONS = (
    "analytical_dashboards",
    "analytical_dashboard_extensions",
    "attribute_hierarchies",
    "dashboard_plugins",
    "export_definitions",
    "filter_contexts",
    "memory_items",
    "metrics",
    "parameters",
    "visualization_objects",
)


@define(kw_only=True)
class CollectionPlan:
    """What a deploy does to one collection."""

    collection: str
    created: list[str] = field(factory=list)
    updated: list[str] = field(factory=list)
    deleted: list[str] = field(factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.created or self.updated or self.deleted)


@define(kw_only=True)
class DeployPlan:
    """The whole plan, one entry per collection that changes."""

    workspace_id: str
    collections: list[CollectionPlan] = field(factory=list)

    @property
    def deletes_anything(self) -> bool:
        return any(plan.deleted for plan in self.collections)

    @property
    def total_deleted(self) -> int:
        return sum(len(plan.deleted) for plan in self.collections)

    def format(self, *, sample: int = 5) -> str:
        """A readable plan. Deletions are listed first and in full up to ``sample``.

        Ordered that way deliberately: creates and updates are what the author intended,
        deletions are what they did not, and a plan that buries the deletions under two
        hundred routine updates is the plan nobody reads to the end.
        """
        if not self.collections:
            return f"No changes: the layout matches {self.workspace_id}."

        lines: list[str] = []
        if self.deletes_anything:
            lines.append(
                f"{self.total_deleted} object(s) exist in {self.workspace_id} but not in this layout. "
                f"Deploying the analytics model replaces it wholesale, so these would be DELETED:"
            )
            for plan in self.collections:
                if plan.deleted:
                    shown = ", ".join(plan.deleted[:sample])
                    more = f" (+{len(plan.deleted) - sample} more)" if len(plan.deleted) > sample else ""
                    lines.append(f"  {plan.collection}: {len(plan.deleted)} -- {shown}{more}")
            lines.append("")

        lines.extend(
            f"{plan.collection}: {len(plan.created)} created, {len(plan.updated)} updated"
            for plan in self.collections
            if plan.created or plan.updated
        )
        return "\n".join(lines)


def _ids(model: CatalogDeclarativeAnalytics, collection: str) -> list[str]:
    if model.analytics is None:
        return []
    return [obj.id for obj in (getattr(model.analytics, collection, []) or [])]


def build_deploy_plan(
    current: CatalogDeclarativeAnalytics,
    incoming: CatalogDeclarativeAnalytics,
    *,
    workspace_id: str,
) -> DeployPlan:
    """Diff what a workspace has against what a layout would put there.

    Both sides are the workspace's *own* objects: a declarative model never contains what a
    child inherits, so an inherited object is in neither and cannot appear as a deletion.
    That is correct -- a deploy cannot delete what the workspace does not own.
    """
    plan = DeployPlan(workspace_id=workspace_id)
    for collection in _COLLECTIONS:
        existing, arriving = set(_ids(current, collection)), set(_ids(incoming, collection))
        entry = CollectionPlan(
            collection=collection,
            created=sorted(arriving - existing),
            updated=sorted(arriving & existing),
            deleted=sorted(existing - arriving),
        )
        if not entry.is_empty:
            plan.collections.append(entry)
    return plan


def plan_deploy(sdk: GoodDataSdk, workspace_id: str, incoming: CatalogDeclarativeAnalytics) -> DeployPlan:
    """Fetch what the workspace owns today and diff the layout against it."""
    current = sdk.catalog_workspace_content.get_declarative_analytics_model(workspace_id)
    return build_deploy_plan(current, incoming, workspace_id=workspace_id)
