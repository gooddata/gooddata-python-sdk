# gooddata-eval

`gd-eval` — a CLI and library that drives the GoodData AI agent (a separate service, in
`gdc-nas`) through a dataset of natural-language questions and scores what comes back,
including side-by-side comparison across models. Each dataset item is a JSON envelope
loaded from a local folder or pulled from a Langfuse dataset. Results are aggregated into
pass@K / pass^K reports and optionally pushed to Langfuse as scored traces tied to a
dataset run. The newest and most actively developed package in the repo.

## Owns

- The `gd-eval` CLI (`gd-eval run`, `gd-eval models`)
- Dataset loading and the evaluation run loop
- Per-capability evaluators and their scoring
- Result reporting, and pushing runs, scores and trace links to Langfuse

## Does NOT Own

- The agent under evaluation — that lives in `gdc-nas` (gen-ai)
- Platform access → `gooddata-sdk`

## Architecture

| Path | Role |
|---|---|
| `cli/` | argument parsing, and `agentic_runner` — the agentic dispatch and concurrency phases |
| `core/agentic/` | multi-turn agentic evaluation per capability, **plus** all Langfuse trace polling and linking (`_langfuse.py`, `_trace_linker.py`) |
| `core/chat/` | SSE client for the agent's streaming chat endpoint |
| `core/summary/` | HTTP client for the dedicated dashboard-summary endpoint — a single-shot chat backend, not reporting |
| `core/dataset/` | dataset format and loading |
| `core/evaluators/` | single-shot evaluators and their registry |
| `core/langfuse/` | `sink.py` only — pushes single-turn scores and dataset-run items |
| `core/reporting/` | console and JSON output rendering |
| `core/scoring.py`, `core/runner.py` | scoring and orchestration |
| `core/models.py` | `DatasetItem`, `ChatResult`, `ItemReport` and friends |

**Depends on**: `gooddata-sdk`, `httpx`, `pydantic`, `orjson`, `rich`. The LLM-judge
evaluator is an optional extra (`llm-judge`, pulling `openai>=1.45,<2.0`); every `openai`
import site is guarded or deferred so the base install stays usable without it — keep it
that way.

### Two evaluation paths that share almost nothing

- **Single-shot** kinds send one chat turn and are scored by an `Evaluator` (a Protocol:
  a `test_kind` attribute plus `evaluate(item, chat_result) -> ItemEvaluation`) looked up
  from a registry in `core/evaluators/__init__.py`.
- **Agentic** kinds (`agentic_*`, `vis_agentic`) drive a full multi-turn conversation over
  the SSE endpoint and are dispatched by an explicit `if`/`elif` chain in
  `cli/agentic_runner.py`.

Many capabilities exist in **both** forms — visualization, metric skill, alert skill,
search, general question and guardrail each have a single-turn and a multi-turn
implementation, sometimes under different `test_kind` strings (`search_tool` vs
`agentic_search`). These are parallel implementations, not layers.

### Dataset items

`DatasetItem` is the envelope: `id`, `dataset_name`, `test_kind`, `question`, and
`expected_output: Any`. `expected_output` is deliberately untyped — each evaluator parses
its own shape. `test_kind` on the item is what labels the result, not the evaluator class,
which is why `knowledge_question` can reuse `GeneralQuestionEvaluator` verbatim.
`dashboard_summary` items additionally need `summary_input`.

## Gotchas

**Adding an evaluator is a registry change, not a naming convention.** Single-shot kinds go
into `_EAGER_EVALUATORS`, or `_LAZY_EVALUATOR_MODULES` plus `_LAZY_EVALUATOR_CLASSES`, in
`core/evaluators/__init__.py`. Agentic kinds need the string added to `AGENTIC_TEST_KINDS`
and a new branch in `_dispatch_agentic`. Test file naming follows the capability, but
naming a test file correctly registers nothing.

**Parallel-safety is a reviewed allowlist, and getting it wrong corrupts results.**
`WORKSPACE_MUTATING_TEST_KINDS` is computed as `AGENTIC_TEST_KINDS - PARALLEL_SAFE_TEST_KINDS`,
so a newly added kind defaults to workspace-mutating and runs serially in its own phase.
That default is correct: agent tool calls create real server-side objects (metrics, alerts).
Adding a kind to `PARALLEL_SAFE_TEST_KINDS` is a deliberate assertion that it is read-only,
which nothing in the package can prove for you.

**The SSE client's retry predicate is load-bearing.** `core/chat/sse_client.py` retries
429/502/503/504 and `httpx.RemoteProtocolError` (a mid-stream disconnect) with exponential
backoff, and treats a `METADATA_SYNC_IN_PROGRESS` payload as transient. The
`RemoteProtocolError` case was added after it was confirmed live to contaminate a small
percentage of visualization runs with a hard fail and no retry. Narrowing that predicate
reintroduces the problem.

**Langfuse trace linking is deliberately off the item critical path.** Polling for trace
ingestion has no pass/fail signal and inflates or misattributes per-item latency, so
`BackgroundTraceLinker` defers it and is drained before the report renders
(`run_trace_link_inline` is the synchronous alternative). Do not "fix" a slow item by
making trace scoring synchronous again.

**Scoring weights do not sum to 1.** `quality_score` is the fraction of boolean-valued keys
in `best_detail` that are true, falling back to `pass_at_k` when there are none (text
evaluators). `value_score` is `0.6 * quality + 0.2 * speed` — the 0.8 total is what the
code does; treat it as intentional unless you have checked with the owner.

### Fixture shapes

Group-by / attribute expectations in the alert-skill fixtures are written in AAC shape,
while the tool arguments the agent emits are AFM-shaped. Never deep-compare those two
directly — convert, or compare field by field. This applies specifically to the
attribute/group-by fields: `Filters` in the same fixtures is AFM-shaped on both sides and
is correctly deep-compared as-is. The attribute comparison itself lands with the
alert group-by work currently on `jt/gdai-2175-eval-alert-attributes`, so on `master` this
is guidance for the incoming code rather than a description of what is already there.

## Testing

Plain pytest under `tests/`, no cassettes — the agent is stubbed with
`unittest.mock`. Tests are named per capability (`test_agentic_*.py`), which is the
convention to follow when adding one.

`ty` is configured here with `allowed-unresolved-imports` for `openai.**` and
`gooddata_api_client.**`; do not widen that list to paper over a real typing problem.
