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
works at two levels:

**Each object on its own** — a visualization's required keys, its `version`, the
references its sorts and filters make into its own buckets, whether every bucket item and
filter carries the fields without which it cannot be executed, and the serialised length.

**The model as a set** — ids repeated within a collection, dashboards and filter contexts
naming objects the layout does not carry, and metric definitions that form a cycle. None of
these is visible in any single object.

Metrics are included: their references live inside a MAQL string as `{type/id}` tokens
rather than in JSON, and in most workspaces metrics outnumber everything else.

`report.ok` is false only when something is **provably** wrong. Warnings — an unrecognised
chart type or bucket name — leave it true, because an unfamiliar value usually means the
SDK is older than the platform rather than that the content is broken.

## A layout that carries its own logical model needs no server

Whether `{fact/amount}` exists normally requires asking the workspace. But a full layout
already contains the logical model, and that is where those objects are declared — so
`gdc validate --path <layout>` resolves every metric, label, dataset and fact reference
from the files alone, with nothing to log in to.

Two rules make that work, and neither is visible in the LDM as written: an attribute has a
label sharing its id even when it declares none, and a date instance's granularities become
addressable as `<instance>.<granularity>`. The reconstruction is checked rather than
trusted — against a real workspace it produces exactly the id set `get_full_catalog`
returns, and finds exactly the same problems.

A layout without an LDM says so rather than reporting a clean result it cannot justify.

## Checking against the workspace you are deploying to

```python
from gooddata_sdk import GoodDataSdk
from gooddata_sdk.catalog.validation import ValidationService

sdk = GoodDataSdk.create(host, token)
result = ValidationService(sdk).validate_analytics_model("target_workspace", model)
print(result.format())
```

This adds the question the offline checks cannot answer: do the metrics, labels and
datasets these objects name actually exist where the objects are going? References are
collected from every kind that makes them — visualizations, dashboards and filter contexts
through their identifier nodes, metrics out of their MAQL.

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

# ...and say what deploying there would change
gdc validate --path layout --workspace my_workspace --plan

# check just the object you edited
gdc validate --path layout/analytics_model/visualization_objects/my_insight.yaml

# findings as JSON, for a pipeline that does more than read the exit code
gdc validate --path layout --json
```

Pointed at a directory, the command validates the **logical data model** alongside the
analytics model: dataset references that name a dataset which is not there, joins on a
column the target does not have, grain entries naming nothing, duplicate dataset/attribute/
label/fact ids, and datasets with no table and no SQL. Every metric and visualization
stands on those joins, so a layout whose analytics model is spotless is still broken if its
LDM is not — deleting a single dataset from a real model surfaced 32 broken joins.

A note on what "a column of that dataset" means, because it is the subtlety these checks
turn on: it is not "an attribute it declares". A composite key propagates, so a dataset can
legitimately be joined on, and grained by, a component that arrives through one of its own
references. Resolving against declared attributes alone reports ordinary joins as broken.

It also reads the files themselves: one that does not
parse, one whose name disagrees with the `id` inside it, or two claiming the same `id`.
The layout writes one file per object named by its id, so a mismatch means the object
round-trips into a different file and overwrites whatever owned that name — and once the
objects are loaded, the collision has already resolved itself silently.

## Knowing what a deploy would delete

`--plan` answers the question the deploy itself never asks:

```
4676 object(s) exist in my_workspace but not in this layout. Deploying the analytics
model replaces it wholesale, so these would be DELETED:
  metrics: 3379 -- abandonment_rate, active_card_count, ... (+3374 more)
  visualization_objects: 1297 -- ...
```

Deploying an analytics model is a `PUT` of the whole model: anything the workspace owns
and the layout omits is removed. A migration is exactly when the local copy is most likely
to be incomplete, and the deletions are silent and not undoable.

Exit codes: `0` nothing provably wrong, `1` validation failed, `2` the path or the
connection was wrong. `--workspace` connects through `gooddata.yaml` beside the layout if
there is one, otherwise `GOODDATA_HOST` and `GOODDATA_TOKEN`.

Deploying an analytics model replaces the whole model, so the cheapest moment to find a
broken visualization is before that call.

## Buckets and chart types

A chart type's buckets are not interchangeable: a line chart's dimension bucket is `trend`
while a column chart's is `view`, so a line chart carrying a `view` bucket stores without
complaint and draws nothing. Neither the required-key checks nor the local-identifier
resolution can see that — the content is well-formed, it is simply not what a line chart is.

The table covers the chart types the platform's execution converter handles, and says only
what that converter can be read to say — which bucket each type takes each dimension from.
Measure buckets are accepted everywhere, because the converter collects measures by walking
all buckets rather than by name; only the attribute buckets are looked up per type, so only
those can be wrong. A type with no entry gets no opinion rather than a rejection, and
findings are warnings, because a chart type can learn a new bucket before the SDK hears
about it. Pass your own `rules` to `check_buckets_for_visualization_type` to cover a type
the SDK does not know.

Two vocabularies come with it. `VISUALIZATION_URLS` is every chart type the platform can
convert, in both spellings that occur in stored content (`local:table` and `table`), and
`BUCKET_NAMES` is every bucket name the converter recognises. Both are checked by default,
both report warnings, and both can be switched off:

```python
validate_content(content, known_visualization_urls=None)  # on a platform newer than this SDK
```

## Filter values, and why they are opt-in

Every other check here asks whether the layout is *well formed*. This one asks whether it
is still *true*. A filter pinned to `in: {values: ["EMEA"]}` is perfectly valid content, and
the day that region is renamed the chart filtered by it quietly returns nothing — no error,
just an empty dashboard, which is the failure people notice last and diagnose slowest.

It is the only check that reads **data** rather than metadata, so it costs a
`SELECT DISTINCT` against the data source per label. It is therefore asked for by name and
refuses to run without a workspace:

```bash
gdc validate --path <layout> --workspace <ws> --check-filter-values
```

Asking for it without `--workspace` is a usage error rather than a no-op — silently
dropping it would report a clean run for a check that never happened.

Three things keep it affordable and quiet:

- **One query per label, not per value or per object.** The server is asked which of a
  given list exist, so a filter naming forty values costs the same single call as one
  naming a single value, and twenty charts pinned to the same label share one query. On a
  real corpus that turned 28 attribute filters into 6 queries.
- **Findings are warnings.** An overnight load can make a finding here disappear without
  anything being edited, so it must not fail a build the way a structural fault does.
- **Only value-based filters are checked.** Elements given by reference (`uris`) name
  primary-label values rather than resolvable titles, a `null` entry means the NULL element
  rather than a value to look up, and an empty list is a no-op. All three are skipped rather
  than guessed at. A label that cannot be queried at all reports nothing here — that is the
  reference check's finding, and saying it twice in different words helps nobody.

## Totals

A bucket's `totals` are the one place a bucket refers to something rather than declaring
it, and the only reference that points *across* buckets: the measure a total sums lives in
the measures bucket, while the total itself hangs off the attribute bucket that grains it.
Both `measureIdentifier` and `attributeIdentifier` are resolved against the bucket items,
the same way a sort is, and a total missing one of the three fields it cannot be computed
without is an error. The calculation itself (`sum`, `avg`, `max`, `min`, `med`, `nat`) is
checked as a warning, since that set can gain members.

## Properties

`properties` holds the rendering configuration, and nearly all of it is deliberately left
alone. Stored content carries `controls` keys the platform models nowhere — `legend`,
`xaxis`, `colorMapping`, `dualAxis` and many more — because the renderer owns that
vocabulary. There is no "unknown key" check and there should never be one: it would fire on
ordinary working charts.

What is checked is the handful of fields the platform itself reads, where nothing else can
see a mistake:

- **Geo position labels.** `controls.latitude`, `controls.longitude` and
  `controls.tooltipText` hold *label identifiers* that the platform turns into buckets.
  They are catalog references living in a plain string, so the reference walk — which looks
  for `identifier` nodes — goes straight past them, and a geo chart whose latitude label was
  renamed loses the field silently. These resolve like any other reference, against a
  workspace or against the layout's own logical model, and an unresolved one is an error.
- **Measures named by local identifier.** `controls.secondary_xaxis.measures` and the keys
  of `controls.inlineVisualizations` point at bucket items the same way a sort does.
- **Enumerated values**, such as `measureGroupDimension`, which decides whether a table is
  transposed.

Everything except the geo references is a warning.

## What a clean report does not mean

It means nothing **provably** wrong was found. It is not a promise that the visualization
renders: most of `properties` is open-ended by design and is left alone, and unknown fields
are ignored so that a newer format does not produce false alarms.
