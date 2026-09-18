---
title: "Validating visualizations"
linkTitle: "Validating visualizations"
weight: 28
---

A visualization's `content` is stored by the platform as a free-form JSON object. It is
checked for being an object and for its length, and nothing else — the structure a
renderer needs is not part of that contract. Content that no frontend can draw is
therefore accepted without complaint and fails later, one insight at a time.

That is rarely a problem for objects built in Analytical Designer, which produces the
structure by construction. It is a problem when the objects are written by hand or
generated — migrations, provisioning, anything that assembles a layout in code.

These checks close that gap for the paths that go through the SDK. They report; they never
block a write on their own.

## Checking a layout before you deploy it

```python
from pathlib import Path
from gooddata_sdk import CatalogDeclarativeAnalytics

model = CatalogDeclarativeAnalytics.load_from_disk(Path("layout"))

report = model.validate()
if not report.ok:
    print(report.format())
```

`validate()` needs no workspace and no credentials, so it can run on a pull request. It
checks each visualization's required keys, its `version`, the references its sorts and
filters make into its own buckets, and the length of the serialised content.

`report.ok` is false only when something is **provably** wrong. Warnings — an unrecognised
chart type or bucket name — leave it true, because an unfamiliar value usually means the
SDK is older than the platform rather than that the content is broken.

## Checking against the workspace you are deploying to

```python
from gooddata_sdk import GoodDataSdk
from gooddata_sdk.catalog.validation import ValidationService

sdk = GoodDataSdk.create(host, token)
result = ValidationService(sdk).validate_analytics_model("target_workspace", model)
print(result.format())
```

This adds the question the offline checks cannot answer: do the metrics, labels and
datasets these objects name actually exist where the objects are going?

Validity is a property of the object **and** the target, not of the object alone. The same
layout can be correct for one workspace and broken for another, so check it against where
it is going rather than where it came from.

### Parent and child workspaces

References resolve against the workspace's **effective** catalog, which spans its
inheritance chain.

This matters for a child workspace. A child's declarative model holds only the objects the
child itself owns — often almost nothing, with the metrics, labels and datasets it uses
living in the parent. Resolving a child's content against the child's own layout would
report correct objects as missing. Resolving against the effective catalog validates it on
the same terms it will execute on.

The corollary is that a layout exported from a child says nothing about what that child
inherits: `CatalogDeclarativeAnalytics.validate()` sees only the objects in the file.

## From the command line

```bash
# structure only, no credentials needed — suitable for CI
gdc validate --path layout

# also resolve references against a target workspace
gdc validate --path layout --workspace my_workspace

# check just the object you edited
gdc validate --path layout/analytics_model/visualization_objects/my_insight.yaml
```

Exit codes: `0` nothing provably wrong, `1` validation failed, `2` the path or the
connection was wrong. `--workspace` connects through `gooddata.yaml` beside the layout if
there is one, otherwise `GOODDATA_HOST` and `GOODDATA_TOKEN`.

Deploying an analytics model replaces the whole model, so the cheapest moment to find a
broken visualization is before that call.

## What a clean report does not mean

It means nothing **provably** wrong was found. It is not a promise that the visualization
renders: `properties` is open-ended by design and is left alone, and unknown fields are
ignored so that a newer format does not produce false alarms.
