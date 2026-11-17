# gooddata-eval

CLI to evaluate the GoodData AI agent against a dataset of natural-language
questions on a chosen workspace and LLM model — including multi-model comparison.

## Install

    uv add gooddata-eval

Or install `gd-eval` as a standalone tool:

    uv tool install gooddata-eval

## Commands

| Command | Description |
|---|---|
| `gd-eval run` | Run an evaluation dataset against one or more models. |
| `gd-eval report` | Render JSON report(s) as one self-contained HTML file. |
| `gd-eval models` | List LLM providers and models configured in the org. |
| `gd-eval generate` | Generate a `visualization` dataset from a workspace's existing insights. |


---

## `gd-eval run`

### Quick start — single model

```bash
export GOODDATA_TOKEN='your-api-token'

gd-eval run \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset  ./my-dataset \
  --model  gpt-5.2 \
  --runs  1 \
  --json  results.json
```

### Multi-model comparison

Pass `--model` multiple times to evaluate the same dataset against several
models and get a side-by-side comparison:

```bash
gd-eval run \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset  ./my-dataset \
  --model  gpt-5.2 \
  --model  claude-opus-4-7 \
  --runs  1 \
  --json  comparison.json
```

When the same model id is offered by multiple providers, use the
`provider/model` syntax to disambiguate:

```bash
  --model  "Foundry4o_4.1_5.2/gpt-5.2" \
  --model  "HN_Anthropic/claude-opus-4-7"
```

Both provider name and provider id are accepted as the prefix.

### Targeting a specific AI Hub agent

GoodData has no admin-settable "default agent": when a conversation doesn't
name one, the platform picks whichever agent was last used or last edited in
that workspace. If your org has several AI Hub agents configured (e.g. one
scoped to visualization only, another with every skill enabled), evaluating
without `--agent-id` can silently exercise the wrong one — a
`metric_skill`/`alert_skill` item run against a visualization-only agent will
never pass, no matter how well-formed the question is.

```bash
export GD_EVAL_AGENT_ID='eval-all-skills'

gd-eval run \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset  ./my-dataset \
  --model  gpt-5.2 \
  --runs  1 \
  --json  results.json
```

Or pass it explicitly instead of via the env var:

```bash
gd-eval run \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset  ./my-dataset \
  --agent-id  eval-all-skills \
  --model  gpt-5.2 \
  --runs  1
```

### All flags

#### Connection

| Flag | Env var | Description |
|---|---|---|
| `--host HOST` | — | GoodData host URL. |
| `--token TOKEN` | `GOODDATA_TOKEN` | API token. Pass via flag or env var. |
| `--profile NAME` | — | Profile name in `~/.gooddata/profiles.yaml` (same file as the `gdc` CLI). |
| `--workspace ID` | — | **Required.** Workspace id to evaluate against. |
| `--agent-id ID` | `GD_EVAL_AGENT_ID` | AI Hub agent every conversation should target. GoodData has no admin-settable default agent — without this, each conversation falls back to whichever agent the platform's last-used/last-edited heuristic resolves, which may not have every skill under test enabled. |

#### Dataset source (pick one)

| Flag | Description |
|---|---|
| `--dataset PATH` | Flat folder of JSON files — one question per file. |
| `--langfuse-dataset NAME` | Pull items by name from a Langfuse dataset. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` and `LANGFUSE_BASE_URL` (or the legacy `LANGFUSE_HOST`). |
| `--kind TEST_KIND` | Fallback `test_kind` for dataset items that do not embed one. Defaults to `visualization`; use e.g. `agentic_metric_skill` for multi-turn agentic evaluation. Items that declare their own `test_kind` ignore this. |

#### Model selection

| Flag | Description |
|---|---|
| `--model MODEL` | Model id to evaluate. Repeat to compare multiple models. Accepts `provider/model` syntax to disambiguate when a model is offered by multiple providers (e.g. `--model "Foundry4o/gpt-5.2"`). Defaults to the workspace's current active model. |

#### Evaluation

| Flag | Default | Description |
|---|---|---|
| `--runs K` | `2` | Independent runs per item. |
| `--gate` | `any` | Which verdict decides an item: `any` = pass@K (a run passing is enough), `power` = pass^K (every run must pass, so the verdict measures stability). Identical at `--runs 1`. Kinds that repeat K runs only — `power` is refused when the dataset also has non-agentic items or `agentic_conversation`, which are always decided on pass@K. |
| `--concurrency K` | `1` | Number of items evaluated concurrently. `1` = sequential (default). Increase to load-test the agent under simultaneous requests — see *Concurrency and workspace safety* below. |
| `--judge-model MODEL` | `gpt-4o` | Model used for LLM-as-judge scoring — `agentic_general_question`, `agentic_guardrail`, `general_question`, `guardrail`, `dashboard_summary` and `document_takeaway`. Also settable via `GD_EVAL_JUDGE_MODEL`. Two things to weigh before changing it: the gpt-5 family rejects `temperature=0`, so verdicts stop being reproducible (the run warns when this happens); and choosing the same model the agent runs means the judge grades its own family's output. |
| `--accept-context-date-filter` | off | Visualization scoring also accepts a date filter the agent carried over from the dashboard in the item's `user_context` when the expected output has none. Changes verdicts, so it is opt-in; also settable via `GD_EVAL_ACCEPT_CONTEXT_DATE_FILTER=1`. See *Date filter carried over from the dashboard* below. |
| `--reasoning-effort LEVEL` | server default | `LOW`, `MEDIUM` or `HIGH`, sent as `options.reasoningEffort` on every chat message. Requires the `enableGenAiReasoningEffort` feature flag on the target organization — without it the server ignores the value. Applies to chat items only; `dashboard_summary` and `document_takeaway` items go through their own endpoints, which have no such option. |

**Concurrency and workspace safety.** Agentic kinds that create workspace objects
(`agentic_metric_skill`, `agentic_alert_skill`, `agentic_conversation`, `agentic_kda_skill`) always run one at a
time whatever `--concurrency` says — a metric or alert created and dropped mid-run would otherwise be visible to
another item reading the same catalog. **That protection is for the agentic kinds only:** the single-turn
`metric_skill` and `alert_skill` kinds are still fanned out and the agent performs the same server-side writes on
that path, so avoid raising `--concurrency` on a dataset of those against a shared workspace. Progress output
interleaves when K > 1, and per-item latencies rise, so they stop being clean single-request measurements.

#### Output

| Flag | Description |
|---|---|
| `--json PATH` | Write a JSON report to this path. Always uses the nested `{models, runs, comparison}` shape even for a single model. |
| `--html PATH` | Write a self-contained HTML report to this path (same output as `gd-eval report`). |
| `--redact` | Make the HTML customer-safe. See `gd-eval report`. |
| `--quiet` | Suppress per-item progress. Per-model result tables and the comparison summary are still printed. |
| `--preserve-failed` | Keep failed conversations on the server instead of deleting them, so they can be inspected afterwards. Applies to the single-turn chat path; agentic kinds manage their own conversation lifecycle. |
| `--timers` | Print per-turn `[timer]` diagnostics — GoodData response, judge, and simulated-user seconds as they happen. Off by default: an 18-item `--runs 2` run emits ~72 lines and buries the progress output. The same measurements are always in the JSON report's `latency_breakdown_s`, so this only adds a live view. Also settable via `GD_EVAL_TIMERS=1`. |

#### Langfuse sink

| Flag | Description |
|---|---|
| `--langfuse` | Log scores and traces to Langfuse after each item. Requires `--langfuse-dataset`. Names each experiment run `{dataset_name}_{timestamp}_{model}`, suffixed `_effort-{level}` when `--reasoning-effort` is set (so runs differing only by effort stay separate) and `_run{N}` per run when `--runs` > 1 — e.g. `general_question_2026-09-02-11-13_gpt-5.2_run0`. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` and `LANGFUSE_BASE_URL` (or the legacy `LANGFUSE_HOST`). |

##### Langfuse v4

One run is one Langfuse **experiment**. Each evaluated item becomes its own trace whose root span carries the
experiment and dataset-item attributes (`langfuse.experiment.name`, `langfuse.experiment.dataset.id`,
`langfuse.experiment.item.id`), and the four scores attach to that root observation. gd-eval speaks to Langfuse
over four REST endpoints and uses no Langfuse SDK, so it runs on every Python version the package supports:

| Endpoint | Used for |
|---|---|
| `POST /api/public/otel/v1/traces` | exporting the experiment root span as OTLP/HTTP JSON |
| `POST /api/public/scores` | one score per write, on a trace or on a single observation inside it |
| `GET /api/public/v2/observations` | finding the agent's gen-ai trace for a conversation |
| `GET /api/public/dataset-items` | loading `--langfuse-dataset` items, and resolving an item's dataset id |

Two consequences of v4's immutable observations. gd-eval sets `version` only on its own experiment span, never on
the agent's gen-ai trace — filter on the gd-eval experiment's `langfuse.version` to compare models. And on the
agentic kinds the latency in `value_score` is the gen-ai trace's root generation latency, read from the
observations endpoint; the single-shot `--langfuse` sink keeps using the item's own measured average latency.

Langfuse Cloud drops v3 on **2026-11-16**; a self-hosted Langfuse must be on v4 for any of this to work.

Set `TAVERN_E2E_SKIP_TRACE_LINK=1` to turn the whole **agentic** Langfuse write path off — no trace lookup, no
span export and no scores for `agentic_*` items. The run says so once. It does not reach the `--langfuse` sink,
which still writes a span and four scores for every single-shot item; drop `--langfuse` to silence that too.

**A local `--dataset` cannot be attached to a Langfuse experiment.** `--langfuse` is refused alongside
`--dataset` because a local folder's item ids are not Langfuse dataset item ids. But trace linking does not
depend on that flag — each `evaluate_agentic_*` builds its own client whenever
`LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are exported — so a local run still finds its traces and writes its
scores onto them, and only the per-run grouping fails: the dataset-item lookup 404s and the run reports the item
as one that does not exist in Langfuse, once. The run also warns about this before it starts. Use
`--langfuse-dataset` when you want runs that are comparable across models, or `TAVERN_E2E_SKIP_TRACE_LINK=1` to
skip linking altogether.

**When trace linking happens.** Finding a gen-ai trace means polling until Langfuse has ingested it, which is
lag measured in seconds to minutes. That work produces no verdict — the pass/fail is already decided — so it
does not run inline per item. Every item's Langfuse block is queued and the whole batch runs *after* the agent
phase, draining before any report is written. Two consequences worth knowing:

- **No item's `latency_s` includes trace linking.** Its cost is reported separately as
  `latency_breakdown_s.langfuse_s`, and the run prints
  `[langfuse] trace linking finished in Xs for N item(s); slowest Ys`. If `slowest` approaches the **120s**
  batched retry budget, links are timing out and scores are being orphaned — look for
  `[langfuse] WARNING: no trace found for conversation ...`.
- **The budget depends on who is waiting.** 120s is affordable only because the batch blocks nobody. A direct
  library caller (`evaluate_agentic_*` without a `submit_trace_link`) polls inline, on its own critical path, and
  gets **35s** instead — the same cost as before batching existed, so no inline caller pays for a budget raised
  on the CLI's behalf. Either way a trace that is already ingested costs nothing: the loop looks before it sleeps.
Scores are always final before the command exits — the run blocks on the batch. Interrupting with Ctrl-C drops
whatever is still queued rather than making you wait it out: both the queued trace links and, under
`--concurrency`, the items that have not started. The handful of items already in flight still have to finish —
worker threads are joined at exit and an in-progress agent call cannot be cancelled — so expect to wait up to one
`--concurrency`-wide wave, not the rest of the dataset.

### JSON report shape

The JSON report always uses the nested multi-model shape:

```json
{
  "models": ["gpt-5.2", "claude-opus-4-7"],
  "runs": {
    "gpt-5.2":        { "summary": { "passed": 22, ... }, "items": { ... } },
    "claude-opus-4-7": { "summary": { "passed": 18, ... }, "items": { ... } }
  },
  "comparison": {
    "gpt-5.2":        { "passed": 22, "total": 31, "pass_rate": 0.71, "avg_quality_score": 0.81, ... },
    "claude-opus-4-7": { "passed": 18, "total": 31, "pass_rate": 0.58, "avg_quality_score": 0.72, ... }
  }
}
```

Winner is selected by **pass rate → quality score → latency** (lower latency wins all-equal ties).

The HTML report orders runs by when they started (`summary.started_at`, an ISO 8601 UTC timestamp that `gd-eval run` writes
into each run's `summary`, `null` when a run was never timed), so the order the files are passed to
`gd-eval report` does not decide which run is the latest. A report without it falls back to the date a run's file is
named for (`2026-09-28.json`), and if any run has neither it keeps the order the files were given in.

Each item reports **how many of its runs passed**, not only whether one did:

```json
"runs": 5, "runs_passed": 4, "pass_at_k": true, "pass_power_k": false, "gate_passed": true
```

`pass_at_k` is "did any run pass" — always literal, whatever the gate. `gate_passed` is the verdict the item
was decided on and is what `passed` counts; the two differ only under `--gate power`, where an item that
passed 4 of 5 runs is `"pass_at_k": true, "gate_passed": false`. `runs_passed` is the fact that separates a
reliable item from a coin-flip — without it a 5/5 item and a 1/5 item are identical in every field, because
`quality_score` is derived from the best run alone. `pass_power_k` is true only when every run passed, and the
run summary carries `passed_all_runs` beside `passed`; a large gap between the two means the model is
inconsistent rather than wrong. The console shows `4/5 runs passed` in `Notes` for a non-unanimous pass and
stays quiet for a unanimous one, and its summary line reads `3/4 passed, 1 on every run`.

`runs` is what the item actually ran, which is not always the requested `--runs`: `agentic_conversation` takes
no K and drives its fixture exactly once.

Which of the two decides pass/fail is `--gate`: `any` (default) gates on `pass_at_k`, `power` gates on
`pass_power_k`. The run records it as a top-level `gate`, and a failure under `power` says so —
`Gate pass^3 failed: 2/3 runs passed — unstable, not a clean failure` — because the message body describes
the best run, which under pass^K can be a run that passed, and the console repeats the count in `Notes` for
the same reason. When some runs were ungraded the note says so instead of calling the remainder unstable.
`agentic_conversation` has no K gate, so `--gate power` is refused for a dataset containing one rather than
labelling a report `power` that only part of the dataset was decided under.

**Which runs failed, and why.** A failure message names every failing run right after the gate note, with the
reason its loop stopped and only the checks it failed (expected/actual where the kind knows them), then the best
run's summary as before:

```
Gate pass^3 failed: 2/3 runs passed — unstable, not a clean failure. Failing runs: run 2/3 FAIL (loop exit: success): filters_correct[date: expected none, actual ...].
```

The same data is in each `failed_runs[]` record: `exit_reason` (the run's `LoopExit`, `null` for a kind without
one), `outcome` (see below) and, for the visualization, alert, metric and dashboard skills, `failed_checks`
(`[{"name", "label"?, "expected"?, "actual"?}]`, each `expected`/`actual` longer than 160 characters stored cut to
that length; the run's `detail` keeps the whole value).

None of this changes a verdict, a score or an exception type; it only says more about each failure.

### Harness errors are labelled, not rescored

A run can fail because the test harness failed, not the agent: the simulated user's own model call fails, or the
judge cannot grade the answer. Each failing run is labelled in `failed_runs[].outcome`
(`{"status": "fail" | "error", "reason": ...}`) by one rule (`core/outcome.py`, `classify_run`). The rule is
fail-closed -- only these causes are `error`, anything else, an unknown cause included, is `fail`:

| Cause | Label |
|---|---|
| `simulated_user_failed` | `error` |
| the judge or scorer could not grade the run (`judge_failed`) | `error` |
| `chat_error` (a gen-ai error event, a broken stream, a 5xx after its retries) | `fail` -- on the product path, a customer sees it too |
| `agent_timeout`, `turn_incomplete` (the agent was too slow, or ended its turn without an answer) | `fail` |
| `success`, `budget_exhausted`, `agent_silent`, `not_run`, anything else | `fail` |

The label decides nothing: an `error` run counts as a run that did not pass, so every gate, pass rate and score is
what it was before labels existed. It shows up in four places:

- the "Failing runs" part of the message: `run 1/3 ERROR (simulated_user_failed)`, without the run's checks, which
  failed because the harness did;
- `failed_runs[].outcome`;
- on the raised exception, `outcome` = `{"status": "error", "reason": ...}` when **every** run of the item errored
  (the item says nothing about the agent; its message starts `Harness error, no run was scored (<reason>).`), and
  `shadow` -- what a candidate rule that leaves `error` runs out of the gate (at least ceil(K/2) scored runs, else
  `error`) would have given: `{"verdict": "pass" | "fail" | "error", "runs_scored", "runs_total"}`. Recorded so the
  rule can be judged on real runs; nothing uses it;
- in Langfuse, an `error` run gets an extra score `eval_error` = 1, commented with the reason. Its other scores are
  written as always.

A runner turns these into its own report. The gdc-nas Tavern harness, for example, adds them to the JUnit testcase
as properties and keeps the failure a failure.

Applies to the agentic visualization, alert, metric, dashboard, KDA, anomaly detection and what-if kinds, and to
judge failures of the general question, guardrail and document skill kinds. `agentic_conversation` records its
turns' exits but does not label them yet.

**Changed exit value:** a run whose turn timed out or ended without a final answer used to record `exit_reason`
`chat_error`; it now records `agent_timeout` or `turn_incomplete`, in the run detail and in `failed_runs[]`. Filters
on `exit_reason == "chat_error"` see fewer runs. The item budget (`--item-timeout`) runs from conversation creation,
so an `agent_timeout` from it can include the simulated user's replies and the chat retries' backoff.

#### Date filter carried over from the dashboard (opt-in)

A user who asks for a new chart from an open dashboard without naming a period may get
the dashboard's date filter on the chart, and the product accepts that. By default the
visualization scoring still requires the chart's date filters to equal the expected ones.
Pass `--accept-context-date-filter` to `gd-eval run`, set `GD_EVAL_ACCEPT_CONTEXT_DATE_FILTER=1`
(`0`, `false`, `no`, `off` and empty mean off), or pass `accept_context_date_filter=True` to
`check_filters` to also accept, for the date filter only, a chart that:

- has exactly one date filter, whose period equals a `date_filter` in
  `user_context.view.dashboard.filters` (resolved against the same day), and
- belongs to an item whose expected output has no date filter.

The dashboard's common date filter (no `using`) accepts any date dataset, one that names a
dataset accepts only that one; the one the chart used is reported in the run detail as
`filter_date_context: {"inherited": true, "dataset": ...}`, and a failure summary shows
`date : True (inherited from dashboard context)`. A chart with no date filter passes as
before; an expected date filter, a different period, ranking and attribute filters stay
strict. Applies to `visualization`, `vis_agentic` and `agentic_visualization` items; with the
variable unset the scores and the detail are exactly as without it.

With the flag on, an expected output cannot say "all time, on purpose": an expected output
with no date filter then also accepts a chart that copied the dashboard's period. An item
that must reject the dashboard's period needs to run without the flag.

`agentic_conversation` items take the item's `user_context` as the context of the first
turn. A turn in `expected_output.turns` can set its own `user_context`, which applies
from that turn on until another turn changes it, as the attached context does in the UI:

| Turn | Context sent |
|---|---|
| no `user_context` key | the current one, unchanged |
| `"user_context": {...}` | this one, from this turn on |
| `"user_context": null` | none, from this turn on |

## Supported test kinds

| test_kind | What the agent must produce | Extra required |
|---|---|---|
| `visualization` | Correct AAC visualization (metrics, dimensions, filters, type) | — |
| `metric_skill` | `create_metric` tool call with correct MAQL and format | — |
| `alert_skill` | `create_metric_alert` tool call with correct operator, threshold, trigger, filters, metric, recipients | — |
| `search_tool` | `search_objects` tool call (correct function called = pass; correct arguments = quality score) | — |
| `general_question` | Text answer judged by LLM | `[llm-judge]` |
| `guardrail` | Refusal/redirect (visualization response auto-fails) | `[llm-judge]` |
| `dashboard_summary` | Dashboard summary (via `/summary` endpoint) scored against a rubric by LLM | `[llm-judge]` |
| `document_takeaway` | One short takeaway for a page (via `/takeaway` endpoint): deterministic format checks plus a rubric scored by LLM | `[llm-judge]` |

## Optional extras

### `[llm-judge]` — LLM-as-judge evaluators

`general_question` and `guardrail` items are scored by a GPT-4o judge, and
`gd-eval generate` uses the same package to write question text.
Requires the OpenAI package and `OPENAI_API_KEY`:

```bash
uv add 'gooddata-eval[llm-judge]'
# or for the standalone tool:
uv tool install 'gooddata-eval[llm-judge]'
```

Without `[llm-judge]`, those items are **skipped** and `gd-eval generate` needs
`--no-phrase`.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Run completed. Evaluation failures do **not** cause a non-zero exit. |
| `1` | `gd-eval generate` only: a quality gate failed, an item was dropped, or a written item failed validation. |
| `2` | Operational error: bad connection, missing model, unreadable dataset, missing credentials. |

## Scores (in JSON report and Langfuse)

In Langfuse every score is written to the experiment run's root observation — `traceId` plus `observationId` of
the item's own root span. On the agentic path each score is mirrored onto the agent's gen-ai trace as well
(`traceId` only), so a score survives even when one of the two traces is missing.

| Score | Description |
|---|---|
| `pass_at_k` | 1 if **any** of the K runs passed strict checks, else 0. |
| `pass_power_k` | 1 only if **every** one of the K runs passed. Agentic kinds only. |
| `gate_passed` | The verdict that decided the item: `pass_at_k` under `--gate any`, `pass_power_k` under `--gate power`. Agentic kinds only. |
| `quality_score` | Fraction of strict check flags that are `True` (0.0–1.0). Shown in CLI as a percentage. |
| `value_score` | Weighted blend: 0.6 × quality + 0.2 × speed (speed = max(0, 1 − latency/60s)). |
| `latency_s` | Average per-run latency in seconds. |
| `provider_type` | Model vendor + gateway label (e.g. `ANTHROPIC`, `BEDROCK/ANTHROPIC`, `AZURE/OPENAI`). Stored in Langfuse trace metadata and tags. |

Score names carry no K; K and the gate are on the dataset-run metadata as `eval_k` and `eval_gate`.
`agentic_visualization` also still writes its historic `pass_at_{K}` / `pass_power_{K}` pair.
