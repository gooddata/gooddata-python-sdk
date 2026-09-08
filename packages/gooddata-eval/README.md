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
| `--langfuse-dataset NAME` | Pull items by name from a Langfuse dataset. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |

#### Model selection

| Flag | Description |
|---|---|
| `--model MODEL` | Model id to evaluate. Repeat to compare multiple models. Accepts `provider/model` syntax to disambiguate when a model is offered by multiple providers (e.g. `--model "Foundry4o/gpt-5.2"`). Defaults to the workspace's current active model. |

#### Evaluation

| Flag | Default | Description |
|---|---|---|
| `--runs K` | `2` | Independent runs per item (pass@K). An item passes if any run passes. |
| `--concurrency K` | `1` | Number of items evaluated concurrently. `1` = sequential (default). Increase to load-test the agent under simultaneous requests. Progress output interleaves when K > 1. |
| `--reasoning-effort LEVEL` | server default | `LOW`, `MEDIUM` or `HIGH`, sent as `options.reasoningEffort` on every chat message. Requires the `enableGenAiReasoningEffort` feature flag on the target organization — without it the server ignores the value. Applies to chat items only; `dashboard_summary` items go through the summary endpoint, which has no such option. |

#### Output

| Flag | Description |
|---|---|
| `--json PATH` | Write a JSON report to this path. Always uses the nested `{models, runs, comparison}` shape even for a single model. |
| `--html PATH` | Write a self-contained HTML report to this path (same output as `gd-eval report`). |
| `--redact` | Make the HTML customer-safe. See `gd-eval report`. |
| `--quiet` | Suppress per-item progress. Per-model result tables and the comparison summary are still printed. |

#### Langfuse sink

| Flag | Description |
|---|---|
| `--langfuse` | Log scores and traces to Langfuse after each item. Requires `--langfuse-dataset`. Creates one named experiment run per model (`gd-eval-{timestamp}-{model}`, suffixed `-effort-{level}` when `--reasoning-effort` is set so runs differing only by effort stay separate). Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |

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

---

## `gd-eval report`

Turns JSON report(s) into one HTML file you can actually navigate. No server, no
credentials, no external assets — it opens over `file://`, attaches to a Jira issue and
survives a Slack thread.

```bash
# one run
gd-eval report results.json -o report.html

# several runs side by side -- each file becomes its own column
gd-eval report aug-21.json sep-07.json -o comparison.html --title "H200 regression check"

# customer-safe
gd-eval report results.json -o customer.html --redact
```

| Flag | Description |
|---|---|
| `-o, --out PATH` | Where to write the HTML. Required. |
| `--title TEXT` | Title shown in the report header. |
| `--redact` | Drop conversation/response ids and raw reasoning, and rename models to `Model A`, `Model B`, … Pass rate, per-item results, questions and latency survive. |

The report is a *view* over the JSON — it computes no numbers of its own. It gives you:

- **Run cards and a comparison table** — pass rate, quality, latency per run.
- **An item table** with a pass/fail column per run, so a model or run-over-run
  regression is one glance rather than a hand-assembled spreadsheet.
- **An expression filter** for cross-cutting questions the fixed filters can't
  anticipate, e.g. `d.filter_ranking_score === false` or
  `d.expected_metric_uris.length > 1 && !d.metrics_correct`. Available variables:
  `d` (the focused run's `detail`), `it` (its item), `i` (the row, `i.per[label]` for any
  run), `q` (question), `kind`.
- **The conversation**, when the item ran the agentic multi-turn path — every turn in
  order, with the simulated user marked apart from a real question, so you can see
  whether the agent got there or was handed the answer.
- **A per-item drawer** — checks as pass/fail chips, expected vs actual side by side,
  full reasoning, conversation/response ids.
- **A latency timeline** from `detail.latency_breakdown`, in execution order, one bar per
  step. Clicking a step expands its full record, joined by `index`: the paragraph a
  reasoning step was summarised from, or a tool call's arguments and result from
  `detail.tool_calls`.

`--redact` additionally drops `transcript` and `tool_calls`: the exchange shows that the
simulated user is primed with the expected output, and a tool result carries
semantic-layer internals and real query rows. The turn count and the timeline shape
survive.

Passing several files keyed by file name is the whole run-over-run mechanism: no
database, no run registry, just the JSON files you already have on disk.

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

## `gd-eval generate`

Reverse-engineers a `visualization` dataset out of the charts a customer has already
built, so you get eval questions without hand-authoring any. Reads the workspace's
declarative analytics model (read-only), translates each visible insight's buckets,
sorts and filters into an `expected_output.visualization` spec, then asks an LLM to
write the analyst question that chart answers. Because `expected_output` is copied from
a live object rather than authored, every question is grounded in the real LDM by
construction — the LLM only writes English.

**Setup:** host + token (read access to the workspace), and `OPENAI_API_KEY` plus the
`llm-judge` extra for the phrasing step (`uv add 'gooddata-eval[llm-judge]'`; skip both
with `--no-phrase`).

```bash
export GOODDATA_TOKEN='your-api-token'

# 1. see what a workspace yields before writing anything
gd-eval generate \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset-name  ecommerce \
  --dry-run

# 2. generate, phrase, validate, and export
gd-eval generate \
  --host  https://your.gooddata.cloud \
  --workspace  ecommerce_demo \
  --dataset-name  ecommerce \
  --dashboard  dash_1_returns \
  --out  ./my-dataset \
  --langfuse-out  out/langfuse-dataset.json

# 3. run it
gd-eval run --host … --workspace ecommerce_demo --dataset ./my-dataset --model gpt-5.2
```

`--workspace` is where insights are read from; `--dataset-name` is the `dataset_name`
written into every item (and the default output folder).

| Flag | Effect |
|---|---|
| `--dashboard <id>` | restrict to insights on that dashboard (repeatable); default is the whole workspace |
| `--out <dir>` | output folder (default `./<dataset-name>`); this is what `gd-eval run --dataset` reads |
| `--snapshot-out` / `--snapshot-in` | save/replay the fetched model — replay needs no host, token, or network |
| `--langfuse-out <file>` | also write a Langfuse-importable dataset JSON |
| `--id-prefix` | prefix exported Langfuse item ids (they're unique per *project*, so re-importing an item under its original id is a 409) |
| `--no-phrase` | skip the LLM; emit mechanical `Show <title>` questions |
| `--phrase-model` | OpenAI model for phrasing (default `gpt-4o`) |
| `--no-viz-type` | always blank the expected chart type |
| `--min-questions` / `--min-shapes` / `--min-filtered` | quality gate, default 15, 3 and 1 |

**The question must never contradict its own expected output.** Four rules enforce that:

- The writer is briefed on buckets, sorts and filters only — never the insight title,
  and never the chart type. Titles routinely describe intent the definition doesn't
  implement ("Products by Most Items Sold" over `sorts: []`).
- Every generated question is checked against its spec, and any hit is a hard error:
  ranking words (`top`, `most`, `highest`, …) require a real sort or ranking filter;
  filter words (`only`, `last quarter`, `in 2025`, …) require a real date or attribute
  filter; a breakdown clause requires a non-empty `view_by`/`segment_by` and vice versa;
  a metric may never be broken down by itself; and no template residue (`breakdown
  dimension`, `{…}`) may survive. A violation is fed back once for a rewrite, then
  dropped — and a drop fails the run.
- The writer's rules are built per insight, so an insight with no `view_by` is never
  asked to name a breakdown at all.
- `type` is set only when the question actually names a chart form. An insight's
  `visualizationUrl` records what a human clicked, not what the question constrains.

Everything the writer sees is a display name (`Spend Amount`, `Merchant Name`), never a
raw URI, so questions read like a person wrote them.

**What it won't do.** Insights it can't express without guessing are skipped with a
printed reason, never approximated: derived (arithmetic/PoP) measures, measure-level
filters, `uris`-form attribute filters, unmapped chart types, hidden objects, and
insights whose title promises behaviour their definition lacks. If too few survive, the
quality gate fails the run rather than fabricating items to hit the minimum — point at
more dashboards, or lower `--min-questions`.

Every written item is validated as a `DatasetItem` with a scorable AAC visualization
before the command reports success.

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

| Score | Description |
|---|---|
| `pass_at_k` | 1 if any of the K runs passed strict checks, else 0. |
| `quality_score` | Fraction of strict check flags that are `True` (0.0–1.0). Shown in CLI as a percentage. |
| `value_score` | Weighted blend: 0.6 × quality + 0.2 × speed (speed = max(0, 1 − latency/60s)). |
| `latency_s` | Average per-run latency in seconds. |
| `provider_type` | Model vendor + gateway label (e.g. `ANTHROPIC`, `BEDROCK/ANTHROPIC`, `AZURE/OPENAI`). Stored in Langfuse trace metadata and tags. |
