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

from gooddata_sdk.catalog.validation.model import Finding, Severity, ValidationReport

__all__ = ["Finding", "Severity", "ValidationReport"]
