# (C) 2026 GoodData Corporation
"""Resolving the catalog objects a visualization points at.

Separate from the offline checks because this is the half that needs to know *where* the
content is going. The same object can be valid against one workspace and broken against
another, so a reference finding is only meaningful once a target is named.

Inheritance is the reason this needs care. A child workspace's declarative model holds
only the objects the child itself owns; the metrics, labels and datasets it uses may well
live in a parent. Resolving against the child's own layout would therefore report a
correct object as broken -- which is exactly the kind of false alarm that gets a validator
switched off. Resolution runs against the *effective* catalog instead, which spans the
inheritance chain, so a child's content validates on the same terms it will execute on.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import define, field

from gooddata_sdk.catalog.validation.model import Finding, Severity

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.model_container import CatalogWorkspaceContent

# The identifier types that occur inside visualization content. Taken from a real corpus
# rather than from the set of things the platform has: content refers to metrics, labels,
# datasets (date filters) and occasionally attributes, and nothing else.
_REFERENCE_TYPES = ("metric", "label", "dataset", "attribute", "fact")


@define(kw_only=True, frozen=True)
class CatalogReference:
    """One ``{"identifier": {"id": ..., "type": ...}}`` occurrence inside an object."""

    type: str
    id: str
    location: str

    @property
    def obj_id(self) -> str:
        return f"{self.type}/{self.id}"


@define(kw_only=True)
class ReferenceResolution:
    """What resolving one object's references against a workspace found.

    Deliberately only counts resolved and unresolved, with no split by where a resolved
    reference came from. Reporting "native vs inherited" would need the workspace's own
    object set reconstructed from its declarative model, and that reconstruction is not
    reliable: the platform creates labels an attribute never declares, so objects a
    workspace genuinely owns come back looking inherited. A count that is wrong in a way
    the reader cannot see is worse than a count that is not offered, so what is reported
    is only what the effective catalog can actually answer.
    """

    resolved_count: int = 0
    unresolved: list[CatalogReference] = field(factory=list)

    def summary(self) -> str:
        return f"{self.resolved_count} reference(s) resolved, {len(self.unresolved)} unresolved"


def extract_catalog_references(content: Any, *, path: str = "content") -> list[CatalogReference]:
    """Every catalog object a content blob refers to, with the path where it occurs.

    Walks the whole tree rather than enumerating known positions: unlike local identifiers,
    an ``identifier`` node means the same thing wherever it appears, and new places to put
    one keep being added (layers, parameters, conditional formatting). Walking is the
    behaviour that does not need updating when that happens.
    """
    found: list[CatalogReference] = []

    def walk(node: Any, node_path: str) -> None:
        if isinstance(node, dict):
            identifier = node.get("identifier")
            if isinstance(identifier, dict):
                ref_id, ref_type = identifier.get("id"), identifier.get("type")
                if isinstance(ref_id, str) and isinstance(ref_type, str):
                    found.append(CatalogReference(type=ref_type, id=ref_id, location=f"{node_path}.identifier"))
            for key, value in node.items():
                walk(value, f"{node_path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{node_path}[{index}]")

    walk(content, path)
    return found


def catalog_object_ids(catalog: CatalogWorkspaceContent) -> set[str]:
    """``type/id`` of everything a visualization could legitimately point at.

    Includes labels, attributes and facts as well as datasets and metrics, because content
    refers to those directly -- a catalog reduced to its datasets would report every label
    in every visualization as missing.
    """
    ids: set[str] = set()
    for collection in (catalog.datasets, catalog.metrics, catalog.attributes, catalog.labels, catalog.facts):
        for entity in collection:
            ids.add(str(entity.obj_id))
    return ids


def resolve_references(
    references: list[CatalogReference],
    *,
    effective_ids: set[str],
    object_id: str | None = None,
) -> tuple[list[Finding], ReferenceResolution]:
    """Resolve references against a workspace, reporting what did not resolve.

    Args:
        references: what the object points at.
        effective_ids: everything reachable from the target workspace, inherited included.
            Inherited objects have to be in here: resolving a child's content against only
            what the child owns reports correct objects as broken, which is precisely the
            false alarm that gets a validator turned off.
        object_id: reported on each finding.

    Returns:
        Findings for unresolved references, and the resolution counts.

    A reference whose type is not one that appears in visualization content is skipped
    rather than reported: the walk that produced it is deliberately broad, and an unknown
    type is far more likely to be a part of the format this SDK does not model than a
    genuine dangling pointer.
    """
    resolution = ReferenceResolution()
    findings: list[Finding] = []

    for reference in references:
        if reference.type not in _REFERENCE_TYPES:
            continue
        if reference.obj_id not in effective_ids:
            resolution.unresolved.append(reference)
            findings.append(
                Finding(
                    severity=Severity.ERROR,
                    code="unresolved_reference",
                    message=f"{reference.obj_id} does not exist in the target workspace or anything it inherits from",
                    object_id=object_id,
                    location=reference.location,
                )
            )
            continue
        resolution.resolved_count += 1

    return findings, resolution
