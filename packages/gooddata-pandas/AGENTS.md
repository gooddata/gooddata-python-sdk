# gooddata-pandas

A thin adapter layer over `gooddata-sdk` that turns GoodData executions into pandas
`Series` and `DataFrame` objects. `GoodPandas` wraps an SDK client and, per workspace,
hands out two factories: `SeriesFactory` and `DataFrameFactory`. Underneath, an execution
definition is built from user-friendly column and index specs, and the result is converted
to pandas either by paging through JSON or — with the optional `arrow` extra — by pulling a
single Arrow IPC table.

## Owns

- Creating pandas `Series` and `DataFrame` objects from GoodData data
- Translating user-friendly column/index specs into an SDK `ExecutionDefinition`
- Converting execution results (JSON-paged or Arrow) into pandas structures, including
  grand-total and subtotal handling

## Does NOT Own

- Core SDK behavior → `gooddata-sdk`
- Raw generated endpoints → `gooddata-api-client`

## Architecture

| Module | Role |
|---|---|
| `good_pandas.py` | `GoodPandas` entry point; hands out the two factories |
| `series.py` | `SeriesFactory` |
| `dataframe.py` | `DataFrameFactory` |
| `data_access.py` | `ExecutionDefinitionBuilder`; spec → execution, JSON paging |
| `result_convertor.py` | paged JSON result → pandas |
| `arrow_convertor.py`, `arrow_types.py` | Arrow table → pandas |
| `utils.py` | index construction, column naming |

```python
from gooddata_pandas import GoodPandas

gp = GoodPandas(host="https://example.gooddata.com", token="...")
df = gp.data_frames(workspace_id="demo").for_visualization(visualization_id="...")
```

`GoodPandas.create_from_profile()` is an alternative constructor reading a profile file.

### The two factories are not symmetric

`data_frames(workspace_id)` and `series(workspace_id)` both return factories, but they
expose different method sets:

- **`SeriesFactory`** — `indexed`, `not_indexed`. That is all. There is no series
  equivalent of `for_visualization` or `for_exec_def`; reaching for one gets an
  `AttributeError`.
- **`DataFrameFactory`** — `indexed`, `not_indexed`, `for_items`, `for_visualization`,
  `for_created_visualization`, `for_exec_def`, `for_exec_def_arrow`, `for_arrow_table`,
  `for_exec_result_id`, `result_cache_metadata_for_exec_result_id`.

### `indexed` vs `not_indexed`

`indexed()` builds a pandas `Index` or `MultiIndex` from one or more labels and returns the
remaining columns as data. `not_indexed()` returns a default integer-indexed frame in which
the requested attribute labels appear as ordinary columns alongside the metrics.
`for_items()` and `for_visualization()` choose between the two automatically via
`auto_index`, depending on whether both attributes and measures are present.

## Gotchas

**Return types differ by method family.** `indexed`, `not_indexed`, `for_items` and
`for_visualization` return a bare `pandas.DataFrame`. `for_exec_def`, `for_exec_def_arrow`,
`for_arrow_table`, `for_exec_result_id` and `for_created_visualization` return a
`(DataFrame, DataFrameMetadata)` tuple, where the metadata carries totals-row indexes, the
execution response and primary-label info. `df = factory.for_exec_def(...)` gets you a
tuple, not a frame.

**The Arrow path is a second, opt-in execution path.** `GoodPandas(use_arrow=True,
arrow_config=ArrowConfig(...))`, the `use_arrow` flag on the factory methods, and
`for_exec_def_arrow` / `for_arrow_table` all route through `arrow_convertor.py` instead of
the JSON pager. It requires the `arrow` extra (`gooddata-pandas[arrow]`, which pulls
`pyarrow` and `orjson`). Several parameters — `result_page_len`, `page_size`,
`result_size_dimensions_limits`, `optimized` — are ignored or warned about under
`use_arrow=True`, so a caller tuning them there is tuning nothing.

**Two independent pagination knobs with different defaults.** `indexed`, `not_indexed`,
`for_items`, `for_visualization` and the `SeriesFactory` methods page via `result_page_len`
(default 1000, in `data_access.py`). `for_exec_def` and `for_exec_result_id` page via
`page_size` (default 100, in `result_convertor.py`). These are separate mechanisms — do not
assume one unified default.

**`index_by` cannot reference a metric.** `ExecutionDefinitionBuilder` raises `ValueError`
if you try. Index specs take labels; metrics are data.

## Testing

Uses VCR cassettes under `tests/dataframe/fixtures/` and `tests/series/fixtures/` — the
second-largest cassette set in the repo (91 files, behind `gooddata-sdk`'s 689). See the
root `AGENTS.md` for the recording procedure.
