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

Every item reports `runs_ungraded` beside `runs_passed`: runs the agent answered but the LLM judge returned
nothing readable for. Agentic items also list them as `unscored_runs` / `judge_errors` in their `detail`, and a
`dashboard_summary` item carries `ungraded_criteria`. Such a run — or, for `dashboard_summary`, such a
criterion — is excluded from pass@K and from the quality score rather than counted as a failure: scoring it 0
would be indistinguishable from the judge genuinely failing the answer, which is the confusion
`JudgeResponseError` exists to end. `pass@K` still holds on the runs that *were* graded, so an item can pass with
`runs_ungraded` set; `pass^K` cannot, because a run nobody graded leaves "all K passed" unverified. For
`dashboard_summary` an ungraded `must_include` / `must_not_include` criterion likewise cannot carry a pass —
"the judge could not tell" is not evidence the fact is present — while an ungraded `rubric` line only narrows
the quality score. When *no* run could be graded (for `dashboard_summary`: no gating criterion on any run) the
item errors instead of reporting failures. A non-zero count means pass@K was computed over fewer runs than
`--runs` asked for, so treat the result as weaker evidence and check the judge (`GD_EVAL_JUDGE_DIAGNOSTICS=1`,
or raise `JUDGE_MAX_COMPLETION_TOKENS` if the cause is `finish_reason=length`). The console says so in `Notes`
(`1 run(s) ungraded`, `2 criterion(s) ungraded`).

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
| `--enrich-ranked <N>` | additionally derive up to N ranked questions (see below); default 0 (off) |
| `--skip-ambiguous` | drop items naming something the model carries more than once; reported either way |
| `--min-questions` / `--min-shapes` / `--min-filtered` | quality gate, default 15, 3 and 1 |

### Ranked questions (`--enrich-ranked`)

Analysts sort in Analytical Designer and save the chart without persisting the sort, so
`sort_by`/`ranking_filter` coverage is near zero on most real models — the eval can
punish a spurious ranking but never confirm the agent builds a required one.
`--enrich-ranked N` fills that gap by *deriving* ranked items from the specs already
extracted. Adding a limit or a sort to a definition that executes cannot make it
unanswerable, and "the top 3 X by Y" has exactly one correct spec, so a derived item is
less ambiguous to grade than the insight it came from.

The budget is spent best-grounded first:

1. **Insights whose own title promised a ranking their definition never implemented** —
   "Top Returned Reasons" saved with `sorts: []`. The direction comes from the title
   (`highest`/`most`/`largest` vs `lowest`/`least`/`worst`) and the N too when it states
   one; a title naming both ends names neither and is still skipped.
2. **Ranking filters added to a plain breakdown** — one metric, one non-date dimension,
   no existing sort. N follows the dimension's element count, so a top-5 over six values
   is never emitted.
3. **Sort-only variants**, which order without limiting.

Eligibility is deliberately narrow: two metrics leave "top 3 by what?" unanswered, a
second dimension leaves the N ambiguous between the pair and within a group, and a date
dimension turns the result into "top 3 months", which nobody asks. Variants are
deduplicated by resolved definition — differently-titled insights over one metric and
dimension would otherwise produce the same question twice — and bases are taken
round-robin by metric so one popular metric cannot become a third of the corpus.

Derived items carry `derived_from` (the insight id) and `derived_basis` (`title` when a
human's chart title asked for the ranking, `shape` when this generator chose to add
one), so a pass rate over each can be computed separately.

### Items that cannot say what they mean

Two classes of question are unwinnable however well the agent behaves, and both are
reported:

- **A name the model carries more than once.** One workspace has six labels all titled
  "Product Title"; a question naming one cannot say which is meant, and a perfect chart
  over the wrong one scores zero. `--skip-ambiguous` drops them; the count and the
  offending names are printed either way.
- **A date granularity's cyclical twin.** `MONTH` walks consecutive calendar months,
  `MONTH_OF_YEAR` stacks every January together. Date dimensions are therefore briefed
  by what they do ("one point per calendar month over time, not month-of-year") and the
  writer is told to say it in natural words while keeping the date dataset's name —
  never as a label id in prose ("Order Created At - Month").

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
  `visualizationUrl` records what a human clicked, not what the question constrains —
  with one exception: a chart with no breakdown *must* name its form ("as a KPI", "as a
  single number"). Without it the agent reads a bare "Show me Gross Revenue" as a metric
  lookup, activates only its search skill and builds nothing.

Everything the writer sees is a display name (`Spend Amount`, `Merchant Name`), never a
raw URI, so questions read like a person wrote them.

**What it won't do.** Insights it can't express without guessing are skipped with a
printed reason, never approximated: derived (arithmetic/PoP) measures, measure-level
filters, `uris`-form attribute filters, unmapped chart types, hidden objects, and
insights whose title promises behaviour their definition lacks (though `--enrich-ranked`
implements a promised *ranking* rather than discarding it). If too few survive, the
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

In Langfuse every score is written to the experiment run's root observation — `traceId` plus `observationId` of
the item's own root span. On the agentic path each score is mirrored onto the agent's gen-ai trace as well
(`traceId` only), so a score survives even when one of the two traces is missing.

| Score | Description |
|---|---|
| `pass_at_k` | 1 if any of the K runs passed strict checks, else 0. |
| `quality_score` | Fraction of strict check flags that are `True` (0.0–1.0). Shown in CLI as a percentage. |
| `value_score` | Weighted blend: 0.6 × quality + 0.2 × speed (speed = max(0, 1 − latency/60s)). |
| `latency_s` | Average per-run latency in seconds. |
| `provider_type` | Model vendor + gateway label (e.g. `ANTHROPIC`, `BEDROCK/ANTHROPIC`, `AZURE/OPENAI`). Stored in Langfuse trace metadata and tags. |
