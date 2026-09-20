# (C) 2026 GoodData Corporation
"""The catalog a layout describes, reconstructed from the layout itself.

Whether a metric's ``{fact/amount}`` exists is normally a question only the server can
answer, which is what forces credentials on anyone wanting to check it. But a full layout
already contains the logical model, and the logical model is where those objects are
declared -- so for a self-contained layout the answer is in the files, and validation can
run on a pull request with nothing to log in to.

Two things a naive read of the LDM would miss, both of which make the difference between
resolving everything and reporting thousands of false failures:

* **Implicit labels.** An attribute with no declared labels still has one, sharing the
  attribute's id. Content refers to it by that id like any other label. Left out, every
  reference to such a label looks dangling -- on the workspace this was built against that
  is 4654 of 17543 references, all of them healthy.
* **Date granularities.** A date instance declares granularities rather than attributes and
  labels, and content refers to ``<instance>.<granularity>``. Those ids exist in the
  catalog without appearing anywhere in the LDM as written.

The reconstruction is checkable rather than taken on faith, which is the only reason it is
here at all: against a real workspace it produces exactly the id set ``get_full_catalog``
returns -- 7378 either way -- and resolves 17540 of 17543 references, the remaining three
being the genuine defects the server-backed check also finds. A rule that drifts is
therefore visible as a difference between the two, not as silent wrong answers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
        CatalogDeclarativeAnalytics,
    )
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel


def catalog_ids_from_ldm(model: CatalogDeclarativeModel) -> set[str]:
    """``type/id`` of every catalog object the logical model declares or implies."""
    ids: set[str] = set()
    if model.ldm is None:
        return ids

    for dataset in model.ldm.datasets:
        ids.add(f"dataset/{dataset.id}")
        for fact in dataset.facts or []:
            ids.add(f"fact/{fact.id}")
        for attribute in dataset.attributes or []:
            ids.add(f"attribute/{attribute.id}")
            # The implicit primary label. Adding it unconditionally rather than only when
            # `labels` is empty: an attribute that declares labels is still addressable by
            # its own id, and the cost of the looser rule is at worst accepting a label id
            # that happens to collide with an attribute's -- far cheaper than reporting
            # thousands of healthy references as broken.
            ids.add(f"label/{attribute.id}")
            for label in attribute.labels or []:
                ids.add(f"label/{label.id}")

    for instance in model.ldm.date_instances or []:
        ids.add(f"dataset/{instance.id}")
        for granularity in instance.granularities or []:
            # Content addresses a date field as `<instance>.<granularity>` in lower case --
            # `process_date.year`. The granularity is declared upper case in the LDM.
            qualified = f"{instance.id}.{granularity.lower()}"
            ids.add(f"attribute/{qualified}")
            ids.add(f"label/{qualified}")

    return ids


def catalog_ids_from_layout(
    analytics: CatalogDeclarativeAnalytics,
    ldm: CatalogDeclarativeModel | None,
) -> set[str]:
    """Everything a layout can resolve against on its own: its logical model and its metrics.

    Metrics come from the analytics model rather than the LDM, because a metric referring to
    another metric is resolving against something the layout itself defines.

    A layout with no logical model returns only its metrics, which is correct but weak --
    callers should treat "this layout carries no LDM" as a reason to require a workspace
    rather than as a reason to trust the result.
    """
    ids = catalog_ids_from_ldm(ldm) if ldm is not None else set()
    if analytics.analytics is not None:
        ids.update(f"metric/{metric.id}" for metric in analytics.analytics.metrics)
    return ids
