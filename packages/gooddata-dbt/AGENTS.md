# gooddata-dbt

A CLI plugin (`gooddata-dbt`) that bridges a dbt project to a GoodData workspace. It reads
a dbt project's compiled `manifest.json` and its `profiles.yml`, then uses them to register
the warehouse as a GoodData data source, generate a GoodData logical data model from the
dbt models, and deploy, store or test the analytics layer on top. It supports both dbt-core
(a local manifest) and dbt Cloud (over the dbt Cloud API).

## Owns

- The `gooddata-dbt` CLI and its subcommands — `provision_workspaces`,
  `register_data_sources`, `deploy_ldm`, `upload_notification`, `deploy_analytics`,
  `store_analytics`, `test_visualizations`, `dbt_cloud_run`, `dbt_cloud_stats`
- Conversion of dbt models and profiles into GoodData LDM and deployment inputs
- Workspace and data source provisioning helpers driven by `gooddata.yml`

## Does NOT Own

- Core SDK domain and client services → `gooddata-sdk`
- Generic orchestration and storage automation → `gooddata-pipelines`
- The dbt runtime itself, which comes from dbt's own tooling — this package does not
  depend on `dbt-core` and never invokes dbt

## Architecture

**Entry point**: `gooddata_dbt.dbt_plugin:main`.

**Depends on**: `gooddata-sdk`, plus `pyyaml`, `attrs`/`cattrs`, `requests`, `tabulate`.

The bridge artifact is dbt's compiled `manifest.json`, not the dbt project source.
`dbt/tables.py` parses it, `dbt/profiles.py` parses `profiles.yml` for connection details,
`dbt/cloud.py` covers the dbt Cloud REST and GraphQL APIs, and `gooddata/config.py` reads
the CLI's own config file.

### Config file

`gooddata.yml` — **note the extension**, `.yml` not `.yaml`; `gooddata-sdk`'s `gdc` CLI
uses `gooddata.yaml`, which is a genuinely different file. Overridable with
`--gooddata-config` or `GOODDATA_CONFIG`. See the shipped `gooddata_example.yml`. Its
top-level keys are `environment_setups` (named sets of environments and workspace
suffixes), `data_products` (named groups of model ids, each optionally with `localization`
and `skip_tests`), `organizations` (mapping profiles to data products for multi-tenant
delivery), and `global_properties`.

## Gotchas

**Only dbt models tagged `meta.gooddata.model_id` are picked up.** `read_dbt_models()`
filters the manifest's nodes on that key against the model ids declared in `gooddata.yml`,
and raises if nothing matches. An untagged table is silently absent from GoodData — this is
the first thing to check when a model "didn't show up".

**`manifest.json` carries no column data types; a warehouse scan supplies them.**
`set_data_types()` calls the GoodData scan API to fetch real column types before the LDM is
built. Under `--dry-run` every column becomes `STRING` instead. Since fact/attribute/date
classification happens *after* this step, anything that changes or skips the scan changes
the generated model shape.

**Entity classification is inferred from SQL types, not configured.** By default `NUMERIC`
types become facts, `DATE`/`TIMESTAMP`/`TIMESTAMPTZ` become date dimensions, and everything
else becomes an attribute. Override per column with `meta.gooddata.ldm_type`. Getting this
wrong silently produces a different LDM rather than an error.

**Supported warehouses are a closed, hardcoded list.** `profiles.to_data_class()` handles
`postgres`, `redshift`, `snowflake`, `vertica`, and `duckdb` only when the path starts with
`md:` (MotherDuck) — plain local DuckDB is skipped, because GoodData cannot reach a local
file. Any other `type` in `profiles.yml` raises. That function is the extension point for
adding a warehouse.

**No dbt version or manifest schema check.** The manifest's nodes are structured straight
through `attrs`/`cattrs` with no assertion on `metadata.dbt_schema_version`. A dbt upgrade
that reshapes a node fails with an opaque structuring error rather than a version mismatch.

**Insecure local defaults.** `GOODDATA_TOKEN` defaults to the well-known GoodData.CN
bootstrap token and `GOODDATA_HOST` to `http://localhost:3000` — convenient locally,
dangerous if left unset in CI. dbt Cloud subcommands additionally read `DBT_ACCOUNT_ID`,
`DBT_JOB_ID`, `DBT_PROJECT_ID` and `DBT_TOKEN`; MotherDuck reads `MOTHERDUCK_TOKEN` from
the environment directly. dbt's own `{{ env_var(...) }}` templating inside `profiles.yml`
is resolved by this package's own regex substitution, not by dbt.

**`dbt_cloud_*` targets dbt Cloud's hosted endpoints.** `cloud.getdbt.com` is hardcoded;
there is no self-hosted or alternate-region support, and these subcommands do not work
against dbt-core output.

## Testing

Package-local pytest suites under `tests/`, with resources for dbt profiles, targets and
expected GoodData layouts.
