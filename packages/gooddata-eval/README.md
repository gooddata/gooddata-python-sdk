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
| `gd-eval models` | List LLM providers and models configured in the org. |

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
| `--langfuse-dataset NAME` | Pull items by name from a Langfuse dataset. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |
| `--kind TEST_KIND` | Fallback `test_kind` for dataset items that do not embed one. Defaults to `visualization`; use e.g. `agentic_metric_skill` for multi-turn agentic evaluation. Items that declare their own `test_kind` ignore this. |

#### Model selection

| Flag | Description |
|---|---|
| `--model MODEL` | Model id to evaluate. Repeat to compare multiple models. Accepts `provider/model` syntax to disambiguate when a model is offered by multiple providers (e.g. `--model "Foundry4o/gpt-5.2"`). Defaults to the workspace's current active model. |

#### Evaluation

| Flag | Default | Description |
|---|---|---|
| `--runs K` | `2` | Independent runs per item (pass@K). An item passes if any run passes. |
| `--concurrency K` | `1` | Number of items evaluated concurrently. `1` = sequential (default). Increase to load-test the agent under simultaneous requests — see *Concurrency and workspace safety* below. |
| `--judge-model MODEL` | `gpt-4o` | Model used for LLM-as-judge scoring — `agentic_general_question`, `agentic_guardrail`, `general_question`, `guardrail` and `dashboard_summary`. Also settable via `GD_EVAL_JUDGE_MODEL`. Two things to weigh before changing it: the gpt-5 family rejects `temperature=0`, so verdicts stop being reproducible (the run warns when this happens); and choosing the same model the agent runs means the judge grades its own family's output. |
| `--reasoning-effort LEVEL` | server default | `LOW`, `MEDIUM` or `HIGH`, sent as `options.reasoningEffort` on every chat message. Requires the `enableGenAiReasoningEffort` feature flag on the target organization — without it the server ignores the value. Applies to chat items only; `dashboard_summary` items go through the summary endpoint, which has no such option. |

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
| `--quiet` | Suppress per-item progress. Per-model result tables and the comparison summary are still printed. |
| `--preserve-failed` | Keep failed conversations on the server instead of deleting them, so they can be inspected afterwards. Applies to the single-turn chat path; agentic kinds manage their own conversation lifecycle. |
| `--timers` | Print per-turn `[timer]` diagnostics — GoodData response, judge, and simulated-user seconds as they happen. Off by default: an 18-item `--runs 2` run emits ~72 lines and buries the progress output. The same measurements are always in the JSON report's `latency_breakdown_s`, so this only adds a live view. Also settable via `GD_EVAL_TIMERS=1`. |

#### Langfuse sink

| Flag | Description |
|---|---|
| `--langfuse` | Log scores and traces to Langfuse after each item. Requires `--langfuse-dataset`. Names each experiment run `{dataset_name}_{timestamp}_{model}`, suffixed `_effort-{level}` when `--reasoning-effort` is set (so runs differing only by effort stay separate) and `_run{N}` per run when `--runs` > 1 — e.g. `general_question_2026-09-02-11-13_gpt-5.2_run0`. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |

Set `TAVERN_E2E_SKIP_TRACE_LINK=1` to skip trace lookup entirely (scores are then orphaned; the run says so).

**A local `--dataset` cannot be attached to a Langfuse run.** `--langfuse` is refused alongside `--dataset`
because a local folder's item ids are not Langfuse dataset item ids. But trace linking does not depend on that
flag — each `evaluate_agentic_*` builds its own client whenever `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are
exported — so a local run still finds its traces and writes its scores onto them, and only the per-run grouping
fails, with one `404 from dataset-run-items` reported per run. The run warns about this before it starts. Use
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

Each item reports **how many of its runs passed**, not only whether one did:

```json
"runs": 5, "runs_passed": 4, "pass_at_k": true, "pass_power_k": false
```

`pass_at_k` is "did any run pass" and is what `passed` counts. `runs_passed` is the fact that separates a
reliable item from a coin-flip — without it a 5/5 item and a 1/5 item are identical in every field, because
`quality_score` is derived from the best run alone. `pass_power_k` is true only when every run passed, and the
run summary carries `passed_all_runs` beside `passed`; a large gap between the two means the model is
inconsistent rather than wrong. The console shows `4/5 runs passed` in `Notes` for a non-unanimous pass and
stays quiet for a unanimous one, and its summary line reads `3/4 passed, 1 on every run`.

`runs` is what the item actually ran, which is not always the requested `--runs`: `agentic_conversation` takes
no K and drives its fixture exactly once.

Each item additionally carries a per-phase breakdown:

```json
"latency_breakdown_s": {
  "agent_s": 4.02,          // GoodData's own response time — the system under test
  "judge_s": 1.31,          // LLM-as-judge scoring, post-hoc
  "simulated_user_s": 0.0,  // our simulated user composing the next turn (multi-turn kinds)
  "langfuse_s": 5.70        // trace lookup + score writing, off the critical path
}
```

An item may also carry `unscored_runs` / `judge_errors` in its `detail` (and a
`dashboard_summary` item `ungraded_criteria`). These appear only when the LLM judge returned something
unreadable for part of an item. Such a run — or, for `dashboard_summary`, such a criterion — is excluded from
pass@K and from the quality score rather than counted as a failure: scoring it 0 would be indistinguishable from
the judge genuinely failing the answer, which is the confusion `JudgeResponseError` exists to end. `pass@K` still
holds on the runs that *were* graded, so an item can pass with `unscored_runs` set; `pass^K` cannot, because a
run nobody graded leaves "all K passed" unverified. When *no* run or criterion could be graded the item errors
instead of reporting failures. Their presence means the pass@K was computed over fewer runs than `--runs` asked
for, so treat the result as weaker evidence and check the judge (`GD_EVAL_JUDGE_DIAGNOSTICS=1`, or raise
`JUDGE_MAX_COMPLETION_TOKENS` if the cause is `finish_reason=length`).

`agent_s` + `judge_s` + `simulated_user_s` are the instrumented parts of the item's `latency_s`; they do not add
up to it exactly, because `latency_s` is wall-clock around the whole item and also covers the conversation
create/delete round trips, SDK construction and any cleanup. `langfuse_s` sits **beside** `latency_s`, never
inside it, because trace linking runs outside every item's critical path (see above) — summing all four would
re-inflate exactly what that design removes.

A phase that a kind does not have reports `0.0` rather than an invented number, so read the zeroes as "not
applicable here", not "instant". Today:

| Field | Populated by |
|---|---|
| `agent_s` | `agentic_general_question`, `agentic_metric_skill` |
| `judge_s` | `agentic_general_question` only — `agentic_metric_skill` compares MAQL by string, it has no LLM judge |
| `simulated_user_s` | `agentic_metric_skill` only — `agentic_general_question` is single-turn, it has no simulated user |
| `langfuse_s` | every agentic kind, but only on the `gd-eval` path and only when Langfuse credentials are present |

The other six agentic kinds report `0.0` for the first three. Trace linking itself happens whenever
`LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are exported, with or without `--langfuse`, because each
`evaluate_agentic_*` falls back to `try_make_langfuse_client()`. But its *duration* is measured by the CLI
runner rather than by `evaluate_agentic_*`, so a direct library caller sees `langfuse_s: 0.0` even though its
linking ran. Pass `TAVERN_E2E_SKIP_TRACE_LINK=1` to opt out of linking altogether.

---

## `gd-eval models`

List all LLM providers and their models in the org. Marks the active model
for a workspace when `--workspace` is given:

```bash
gd-eval models \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo
```

```
┃ Provider       ┃ Provider ID ┃ Model ID          ┃ Family    ┃ Active   ┃
│ Foundry4o      │ foundry_…   │ gpt-5.2           │ OPENAI    │ ◀ active │
│                │             │ gpt-4o            │ OPENAI    │          │
│ HN_Anthropic   │ hn_anthr_…  │ claude-opus-4-7   │ ANTHROPIC │          │
```

---

## Dataset format

A dataset is a folder of `.json` files, one per question:

```json
{
  "id":           "stable-unique-id",
  "dataset_name": "my_dataset",
  "test_kind":    "visualization",
  "question":     "Show revenue by quarter",
  "expected_output": { }
}
```

Supported `test_kind` values: `visualization`, `metric_skill`, `alert_skill`,
`search_tool`, `general_question`, `guardrail`, `dashboard_summary`.

### `dashboard_summary` items

Summary items call the dedicated summary endpoint
(`POST /api/v1/ai/workspaces/{ws}/summary`) instead of the chat endpoint, so
they carry an extra `summary_input` block, and the `expected_output` is a
**rubric** rather than an exact answer (summaries are free text):

```json
{
  "id": "summary-001",
  "dataset_name": "summary_pilot",
  "test_kind": "dashboard_summary",
  "question": "Summarize the Sales Overview dashboard.",
  "summary_input": {
    "dashboard_id": "sales_overview"
  },
  "expected_output": {
    "must_include":     ["States the overall revenue trend", "Identifies the top segment"],
    "must_not_include": ["Numbers or segments not present in the visualizations"],
    "rubric":           ["Reads as a coherent business summary"]
  }
}
```

`summary_input` requires only `dashboard_id` (the endpoint summarizes the whole
dashboard). Optional fields narrow the scope: `visualizations` (list of ids),
`filter_context` (AFM filters), `tab_id`, and `format_hint`.

The `expected_output` rubric:

- `must_include` — facts a good summary must contain; **all** must pass for the item to pass.
- `must_not_include` — hallucination/accuracy guards; **any** violation fails the item.
- `rubric` — soft quality dimensions; they affect `quality_score` but do not gate pass/fail.

Each criterion is scored independently by the LLM judge, so `quality_score`
is the fraction of satisfied criteria.

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

## Optional extras

### `[llm-judge]` — LLM-as-judge evaluators

`general_question` and `guardrail` items are scored by a GPT-4o judge.
Requires the OpenAI package and `OPENAI_API_KEY`:

```bash
uv add 'gooddata-eval[llm-judge]'
# or for the standalone tool:
uv tool install 'gooddata-eval[llm-judge]'
```

Without `[llm-judge]`, those items are **skipped**.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Run completed. Evaluation failures do **not** cause a non-zero exit. |
| `2` | Operational error: bad connection, missing model, unreadable dataset, missing credentials. |

## Scores (in JSON report and Langfuse)

| Score | Description |
|---|---|
| `pass_at_k` | 1 if any of the K runs passed strict checks, else 0. |
| `quality_score` | Fraction of strict check flags that are `True` (0.0–1.0). Shown in CLI as a percentage. |
| `value_score` | Weighted blend: 0.6 × quality + 0.2 × speed (speed = max(0, 1 − latency/60s)). |
| `latency_s` | Average per-run latency in seconds. |
| `provider_type` | Model vendor + gateway label (e.g. `ANTHROPIC`, `BEDROCK/ANTHROPIC`, `AZURE/OPENAI`). Stored in Langfuse trace metadata and tags. |
