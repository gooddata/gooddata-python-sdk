# (C) 2026 GoodData Corporation
"""Reading the catalog objects a metric's MAQL refers to.

A metric's references are not JSON -- they are embedded in a MAQL string as ``{type/id}``
tokens::

    SELECT {metric/orders} / {metric/sessions} WHERE {label/status} = "Processed"

so the ``identifier``-node walk that finds a visualization's references sees none of them.
Metrics are usually the most numerous objects in a workspace by a wide margin, and every
one of those references can dangle exactly the way a visualization's can, which is why
they are worth reading out of the string rather than left unchecked.

Only references are extracted. Nothing here parses MAQL or judges whether the expression
is meaningful: that is the server's job, and a half-parser that disagrees with it would
report healthy metrics as broken.
"""

from __future__ import annotations

import re

from gooddata_sdk.catalog.validation.references import CatalogReference

# ``{type/id}``. The id runs to the closing brace and may contain dots (``process_date.year``
# for a date attribute's granularity), hyphens and underscores, so it is matched as
# "anything but a brace" rather than by an id grammar that would have to keep up with
# whatever the platform allows next.
_REFERENCE = re.compile(r"\{(\w+)/([^}]+)\}")

# Double-quoted element values, e.g. ``WHERE {label/status} = "Processed"``. Blanked before
# references are read so that a brace inside a value cannot be mistaken for a reference.
# No metric in the corpus this was written against does that, which is exactly why the
# guard is here: the day one does, the failure would be a phantom reference to an object
# that never existed, reported against a metric that is perfectly fine.
_STRING_LITERAL = re.compile(r'"[^"\n]*"')


def _blank_literals(maql: str) -> str:
    """Replace the contents of quoted literals with spaces, preserving every offset.

    Offsets are preserved rather than the literals removed so that a reference's position
    in the blanked string is still its position in the original, which is what makes the
    reported location point at the real text.
    """
    return _STRING_LITERAL.sub(lambda m: '"' + " " * (len(m.group(0)) - 2) + '"', maql)


def extract_maql_references(maql: str | None, *, path: str = "content.maql") -> list[CatalogReference]:
    """Every ``{type/id}`` reference in a MAQL expression, in order of appearance.

    Args:
        maql: the expression, as stored. Typed as optional because metric content is
            free-form: a metric with no ``maql``, or one holding something that is not a
            string, must yield no references rather than raise in the middle of a layout.
        path: reported as the base of each finding's location; the character offset of the
            reference is appended, since a long metric can name the same object twice and
            only the offset distinguishes them.

    Returns:
        References, including duplicates -- a metric that names the same object twice
        yields two, so the count reflects the expression rather than a deduplicated set.
    """
    if not isinstance(maql, str) or not maql:
        return []
    searchable = _blank_literals(maql)
    return [
        CatalogReference(type=match.group(1), id=match.group(2), location=f"{path}@{match.start()}")
        for match in _REFERENCE.finditer(searchable)
    ]


def referenced_metric_ids(maql: str | None) -> set[str]:
    """Ids of the metrics this expression references, for dependency-graph work.

    Split out from :func:`extract_maql_references` because cycle detection cares only about
    metric-to-metric edges: a metric referring to a label or a fact cannot take part in a
    cycle, and including those would make the graph mostly noise.
    """
    return {reference.id for reference in extract_maql_references(maql) if reference.type == "metric"}
