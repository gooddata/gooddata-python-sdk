# gooddata-eval

`gd-eval` — a CLI and library that drives the GoodData AI agent (a separate service, in
`gdc-nas`) through a dataset of natural-language questions and scores what comes back,
including side-by-side comparison across models. Each dataset item is a JSON envelope
loaded from a local folder or pulled from a Langfuse dataset. Results are aggregated into
pass@K / pass^K reports and optionally pushed to Langfuse as scored traces tied to an
experiment. The newest and most actively developed package in the repo.

## Owns

- The `gd-eval` CLI (`generate`, `run`, `report`, `models`)
- Dataset loading and the evaluation run loop
- Per-capability evaluators and their scoring
- Result reporting, and pushing experiments, scores and trace links to Langfuse

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
| `core/dataset/` | dataset format, loading, and `from_insights.py` — dataset generation from a workspace's real insights |
| `core/evaluators/` | single-shot evaluators and their registry |
| `core/langfuse/` | the whole Langfuse v4 client: `_env` (base URL + credentials), `otlp` (OTLP/JSON encoding), `experiment` (root-span construction, score targets), `observations` (trace reads), `client` (httpx calls), `sink` (single-shot results as experiments) |
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

## Running the pipeline

Four subcommands, in the order you use them. Everything runs through `uv`; never a bare
`python`. There is no build step -- `uv run` syncs the environment from `uv.lock` on first
use, so a fresh clone needs nothing but:

```bash
uv run --package gooddata-eval gd-eval <subcommand> --help
```

`openai` is an optional extra (`llm-judge`) so the published package stays installable
without it, but the `dev` dependency group pulls it in, which is why a plain `uv run` here
has the phrasing step and the LLM judge. Installing `gooddata-eval` from PyPI does not --
there the extra is explicit, and every `openai` import site is guarded or deferred.

Connection is the same for every subcommand that talks to the platform: `--host` +
`--token`, or `GOODDATA_TOKEN` in the environment, or `--profile <name>` reading
`~/.gooddata/profiles.yaml`. Precedence is flags > env > profile.

### 1. `generate` — build a dataset from a workspace

Reverse-engineers `visualization` items out of the charts a workspace already has, so the
expected output is copied from a live object rather than invented. Needs `OPENAI_API_KEY`
for the phrasing step, or `--no-phrase` to emit mechanical `Show <title>` questions.

```bash
uv run --package gooddata-eval gd-eval generate \
  --host "$GOODDATA_HOST" --workspace "$WORKSPACE_ID" \
  --dataset-name ecommerce --out ./datasets/ecommerce \
  --snapshot-out /tmp/ws.json \
  --phrase-model gpt-4o --skip-ambiguous
```

Iterate offline instead of re-fetching: `--snapshot-out` writes everything the generator
read as one JSON file, and `--snapshot-in` replays it with no host, token or network. Add
`--dry-run` to print the shape counts and each spec's brief without writing anything —
the fastest way to see what a workspace yields.

Quality gates fail the command (exit 1) below `--min-questions` (15) or `--min-filtered` (1). Lower them for a smoke test; do not lower them to ship a dataset.
`--langfuse-out` additionally writes a Langfuse-importable file, and `--id-prefix` rewrites
ids on that export only, because Langfuse item ids are unique per project.

Insights the AAC spec cannot express without guessing are skipped with a printed reason
(`SKIP <id>: derived measure (previousPeriodMeasure)`). Read those — they are the
generator telling you what it refused to invent, not noise.

### 2. `run` — evaluate

```bash
uv run --package gooddata-eval gd-eval run \
  --host "$GOODDATA_HOST" --workspace "$WORKSPACE_ID" \
  --dataset ./datasets/ecommerce --kind visualization \
  --model gpt-5.2 --model ProviderName/gpt-4o \
  --runs 3 --gate power --concurrency 4 \
  --json ./results/run.json --html ./results/run.html
```

`--dataset` reads a local folder; `--langfuse-dataset` pulls one by name instead. `--kind`
only supplies a default for items that do not carry their own `test_kind`. Repeat
`--model` to compare models in one run. `--runs` with `--gate power` measures stability
(every run must pass) rather than pass@K. `--langfuse` pushes the run as a scored
experiment, needing `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`.

`--concurrency` is capped for you where it matters: kinds that create workspace objects
run one at a time regardless, see the parallel-safety gotcha below.

### 3. `report` — compare runs

```bash
uv run --package gooddata-eval gd-eval report \
  ./results/*.json -o ./results/comparison.html --title "luna vs 4o" --redact
```

Several JSON reports become side-by-side columns keyed by file name. `--redact` is the
customer-safe form: conversation ids, response ids and raw reasoning dropped, model names
replaced with "Model A", "Model B".

### 4. `models` — what the org has configured

```bash
uv run --package gooddata-eval gd-eval models --host "$GOODDATA_HOST"
```

Run this before guessing a `--model` string.

### Environment

| Variable | Used by |
|---|---|
| `GOODDATA_TOKEN` | every platform-facing subcommand |
| `OPENAI_API_KEY` | `generate` phrasing, and the LLM-as-judge evaluators |
| `GD_EVAL_JUDGE_MODEL` | judge model, same as `--judge-model` |
| `GD_EVAL_AGENT_ID` | which agent to drive, same as `--agent-id` |
| `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` | `--langfuse`, `--langfuse-dataset` |
| `GOODDATA_EVAL_CHAT_*` | SSE retry, backoff and timeout knobs |
| `GD_EVAL_TIMERS` | same as `--timers` |

A gitignored `.env` at the repo root is the normal place for these; load it with
`set -a && . ./.env && set +a` before the command.

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

**A generated item's `expected_output` is copied, never invented — keep it that way.**
`core/dataset/from_insights.py` converts each insight with the platform's own
`declarative_visualization_to_aac()` (from `gooddata-code-convertors`, via `gooddata-sdk`),
so the mapping is not ours to get wrong. What is ours is deciding what the evaluator cannot
yet score — derived measures and measure-level filters convert fine and then compare wrong,
so they are skipped with a printed reason — and stripping the no-op filters AD saves for an
"All" selection, which would otherwise let a question claim a filter its chart lacks. Teach
the comparator about a construct and the matching skip can go; do not make one convert by
hand. Chart type names are the convertor's, which are also the agent's — do not rename them. One
granularity is patched in `CONVERTOR_GRANULARITY_FIXES`: `week_us` → `WEEK_US` is a convertor
bug, the platform enum is `WEEK`.

**The snapshot is a plain-JSON contract.** `--snapshot-in`/`--snapshot-out` is what makes
the generator testable offline and iterable without re-fetching, and it is why the
generator reads the declarative analytics model rather than `sdk.visualizations`. Anything
that changes the fetch shape invalidates every saved snapshot.

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
