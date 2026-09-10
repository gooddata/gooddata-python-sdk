# gooddata-sdk

The main developer-facing SDK for GoodData Cloud, and the package everything else in this
repo builds on. A `GoodDataSdk` object wraps a generated `GoodDataApiClient` and exposes
typed service objects for managing workspaces, data sources, users, permissions and
organization settings; running AFM executions (including result caching and a
conversational-analytics surface); reading insight and table results; and exporting
dashboards. It also owns the on-disk side of the platform: bidirectional conversion
between GoodData's internal declarative JSON model and two human-authorable YAML forms —
the older declarative layout tree and the newer flat Analytics-as-Code (AAC) format — plus
the `gdc` CLI that deploys and clones an organization between a live instance and a
git-friendly directory tree.

## Owns

- `GoodDataSdk` — construction, auth, custom headers, proxy and TLS options
- Catalog services — workspaces, workspace content, data sources, users, permissions,
  organization, appearance, AI lake
- Compute — AFM execution, result caching, and the AI chat / semantic search surface
- Insight reads (`visualizations`) and tabular reads (`tables`)
- Dashboard export to PDF, tabular and slides (`export`)
- Declarative layout export/import, and AAC conversion via `gooddata-code-convertors`
- The `gdc` CLI for deploy and clone

## Does NOT Own

- pandas Series/DataFrame access → `gooddata-pandas`
- dbt integration → `gooddata-dbt`
- Arrow Flight server → `gooddata-flight-server`
- Custom data source framework → `gooddata-flexconnect`
- Lifecycle automation workflows → `gooddata-pipelines`
- PostgreSQL FDW integration → `gooddata-fdw`
- Raw generated endpoints → `gooddata-api-client`

## Architecture

### Services

`GoodDataSdk` exposes each service as a lazily-constructed property. There is no naming
convention to infer from — this is the complete list:

| Property | Service |
|---|---|
| `catalog_workspace` | workspace CRUD, hierarchy, declarative workspace layout |
| `catalog_workspace_content` | LDM and analytics model, layout store/load, AAC |
| `catalog_data_source` | data source registration, scanning, PDM |
| `catalog_user`, `catalog_permission` | users, user groups, permission assignment |
| `catalog_organization` | organization settings, JWKs, identity providers |
| `catalog_appearance` | color palettes and theming |
| `catalog_ai_lake` | AI lake objects |
| `compute` | AFM execution, result cache, AI chat and search |
| `visualizations` | insight reads |
| `tables` | tabular reads on top of executions |
| `export` | dashboard export (PDF / tabular / slides) |
| `support` | support and diagnostics endpoints |
| `client` | the underlying generated `GoodDataApiClient` |

Note what is *not* here: there is no dashboard service. `visualizations` reads insights
only; dashboards are reachable solely through the declarative and AAC layout machinery.

### Client construction

```python
from gooddata_sdk import GoodDataSdk

sdk = GoodDataSdk.create("https://example.gooddata.com", "<api-token>")
workspaces = sdk.catalog_workspace.list_workspaces()
```

**Pass host and token positionally.** The parameters are named `host_` and `token_` with
trailing underscores, and `create()` also takes `**custom_headers_`. Calling
`create(host=..., token=...)` therefore raises `TypeError: missing 2 required positional
arguments`, and if you pass them positionally *and* by keyword, the keyword copies are
silently accepted as custom HTTP headers instead of being rejected. `create_from_profile()`
reads host and token from a profile file instead.

### Layouts and AAC

Layout code lives under `catalog/workspace/`. AAC conversion functions and workspace-level
load/store are in `catalog/workspace/aac.py`, and the AAC↔declarative conversion itself
runs through `gooddata-code-convertors` (WASM).

### CLI

`src/gooddata_sdk/cli/` provides `gdc`, with two actions: `gdc deploy` and `gdc clone`
(`--only` narrows them to specific entity types).

## Gotchas

**Layout `path` defaults bind at import time.** Every store/load method on
`CatalogWorkspaceContentService` defaults its path to `Path.cwd()` as a Python default
argument, which is evaluated once when the module is first imported. If the process later
calls `os.chdir()` and then calls one of these with no explicit path, files go to the
*original* directory with no error. Always pass an explicit `Path` in code that changes
directories.

**`gdc` mixes AAC and declarative by entity type, not by mode.** Workspace content is read
and written as AAC (`load_aac_workspace_from_disk` / `store_aac_workspace_to_disk`), while
data sources, users, user groups and workspace data filters use plain declarative YAML
(`CatalogDeclarative*.load_from_disk` / `.store_to_disk`). This is a fixed per-type split,
not two alternative formats to choose between — adding a new entity type to deploy or clone
means deciding which bucket it belongs in.

**`gooddata.yaml` is both the CLI config and the SDK profile file.** `gdc` parses it for
`source_dir` and `--only` granularity, then hands the same path to
`GoodDataSdk.create_from_profile(profiles_path=...)` for host and token. A token written as
`$SOME_ENV_VAR` is resolved from the environment rather than used literally. Getting the
file's shape wrong breaks deploy/clone and auth at the same time.

**`gdc` searches parent directories.** `_find_config_file` checks the working directory and
then every parent, so an invocation deep in a tree can pick up a `gooddata.yaml` you did
not expect. Note the spelling: this CLI uses `gooddata.yaml`, while `gooddata-dbt` uses
`gooddata.yml`.

## Testing

Cassette-heavy — `tests/catalog/fixtures/` is the single largest churn point in the repo.
The recording procedure is in the root `AGENTS.md`.

`tests/catalog/refresh/` holds a layout that *replaces* the docker-compose layout partway
through some catalog tests, so a change to the default layout usually has to be made in
both places. `tests/catalog/expected/` holds comparison fixtures. `CONTRIBUTING.md`
enumerates the rest.

Extend the existing tests when adding to an existing surface — a new property or enum value
belongs in the fixtures and round-trip assertions that already cover it.
