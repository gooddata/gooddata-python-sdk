# gooddata-fdw

A PostgreSQL Foreign Data Wrapper that exposes GoodData insights and semantic-model
computations as ordinary SQL tables. It is a Python class loaded by the multicorn
extension, not a compiled Postgres extension of its own: a user registers a foreign server
pointing at `gooddata_fdw.GoodDataForeignDataWrapper`, then either imports a foreign schema
(auto-generating one table per insight plus a `compute` pseudo-table) or hand-writes
`CREATE FOREIGN TABLE` statements. Every `SELECT` against these tables is a live API call
to GoodData, not a local table scan.

## Owns

- The FDW implementation that surfaces GoodData data as PostgreSQL foreign tables
- `IMPORT FOREIGN SCHEMA` support and the bundled SQL helper procedure
- The translation layer from a SQL query into an SDK execution
- Column-type mapping between GoodData types and PostgreSQL types

## Does NOT Own

- Core API and service client behavior → `gooddata-sdk`
- Flight RPC server infrastructure → `gooddata-flight-server`
- FlexConnect function runtime → `gooddata-flexconnect`

## Architecture

**Depends on**: `gooddata-sdk`, and at runtime a multicorn/PostgreSQL environment —
multicorn 1.4.0 with PostgreSQL 12 is what the package is tested against. Note that
multicorn is deliberately *not* a pip dependency; it is an OS-level Postgres extension.

| Module | Role |
|---|---|
| `fdw.py` | `GoodDataForeignDataWrapper` — `import_schema()` and `execute()` |
| `executor.py` | per-table-type execution strategies |
| `import_workspace.py` | foreign-table generation during import |
| `column_utils.py`, `column_validation.py`, `naming.py` | type mapping, validation, naming |
| `options.py` | server/table option parsing |
| `environment.py` | multicorn imports, with test stubs |
| `sql/` | `create_extensions.sql`, `import_gooddata.sql` |

### Setup, in PostgreSQL

```sql
CREATE EXTENSION multicorn;
CREATE EXTENSION foreign_table_exposer;

CREATE SERVER gooddata FOREIGN DATA WRAPPER multicorn
  OPTIONS (wrapper 'gooddata_fdw.GoodDataForeignDataWrapper',
           host 'https://example.gooddata.com', token '...');

CALL import_gooddata('my_workspace', 'all');   -- wraps IMPORT FOREIGN SCHEMA
```

### Two table shapes

`object_type` is `insights`, `compute` or `all`, and the choice determines which executor
runs at query time:

- **`insights`** — one foreign table per insight in the workspace. Queries run through the
  insight, equivalent to `for_visualization`.
- **`compute`** — a single non-relational `compute` pseudo-table mapping every metric, fact
  and label in the workspace catalog. Queries select arbitrary combinations and are
  translated into `Attribute`/`Metric` objects and executed via `sdk.tables.for_items`.

This distinction is the single most important architectural fact here for anyone touching
import or execution code.

## Gotchas

**Filter pushdown is limited, and the limits are known rather than bugs.** Only simple
attribute `IN` filters and single-day-granularity date ranges push down. `OR` never pushes
down. Pushdown works for `compute` and hand-written tables but not for `insights`-imported
tables. And against `compute`, a column used in `WHERE` but absent from `SELECT` fails
outright, due to a multicorn limitation. There are `# TODO: push down more filters` markers
in `executor.py` — treat these as documented boundaries before "fixing" them.

**multicorn is stubbed under pytest.** `environment.py` imports the real multicorn only
when neither `pytest` nor `sphinx` is in `sys.modules`, substituting stub classes for
`ForeignDataWrapper`, `ColumnDefinition`, `Qual` and `TableDefinition` otherwise. That is
why the unit tests run with no Postgres present, why the multicorn dependency is commented
out in `pyproject.toml`, and why `ty` has `allowed-unresolved-imports = ["multicorn"]`.
Do not try to `pip install multicorn`, and do not assume stub behavior generalizes to the
real runtime.

**This is a read-only FDW.** `rowid_column`, `insert`, `update` and `delete` are no-op
passthroughs to the multicorn base class. There is no partial write support to build on.

**Numeric precision comes from import options, not code.** Metric and fact columns become
`DECIMAL` sized from the metric's display format or the `numeric_max_size` import option;
attribute and label types are derived through the SDK's converter store. A precision
mismatch is usually an import-option problem.

**Low-churn package.** Substantive source changes are infrequent — most recent commits are
release and tooling automation. Nothing in the repo marks it deprecated, and it is
classified Production/Stable, but do not assume recent behavior verification.

## Testing

Package-local pytest suites under `tests/`, with cassettes in `tests/execute/fixtures/`.

The FDW tests need a service the default stack does not start:

```bash
docker compose --profile fdw up -d      # PostgreSQL + gooddata-fdw extension on port 2543
```
