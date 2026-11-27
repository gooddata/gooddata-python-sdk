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
| `--judge-model MODEL` | `gpt-4o` | Model used for LLM-as-judge scoring — `agentic_general_question`, `agentic_guardrail`, `general_question`, `guardrail`, `dashboard_summary`, `document_takeaway`, `catalog_metadata` and `agentic_knowledge`. Also settable via `GD_EVAL_JUDGE_MODEL`. Two things to weigh before changing it: the gpt-5 family rejects `temperature=0`, so verdicts stop being reproducible (the run warns when this happens); and choosing the same model the agent runs means the judge grades its own family's output. |
| `--reasoning-effort LEVEL` | server default | `LOW`, `MEDIUM` or `HIGH`, sent as `options.reasoningEffort` on every chat message. Requires the `enableGenAiReasoningEffort` feature flag on the target organization — without it the server ignores the value. Applies to chat items only; `dashboard_summary`, `document_takeaway` and `catalog_metadata` items go through their own endpoints, which have no such option. |

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
nothing readable for. Agentic items also list them as `unscored_runs` / `judge_errors` in their `detail` (a document item whose takeaway-endpoint request failed
lists that failure under `request_errors` instead), and a
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

### Latency: single-shot and multi-turn

`avg_latency_s` is one number over a mixed population. The report instead keeps two kinds of item apart, by
their eval kind, and states latency for each:

- **Single-shot** — kinds that send exactly one chat message per run: every non-agentic kind, plus
  `agentic_general_question`, `agentic_guardrail`, `agentic_search` and `agentic_memory`.
- **Multi-turn** — kinds that drive a simulated user or fixture turns: `agentic_visualization` (and
  `vis_agentic`), `agentic_metric_skill`, `agentic_alert_skill`, `agentic_dashboard_skill`,
  `agentic_document_skill`, `agentic_kda_skill`, `agentic_anomaly_detection`, `agentic_what_if`,
  `agentic_agent_switcher`, `agentic_knowledge` and `agentic_conversation`.

```json
"summary": {
  "by_mode": {
    "single_shot": {"total": 12, "passed": 10,
                    "traces_s": {"n": 24, "mean": 5.39, "trimmed_mean": 5.36, "min": 3.88, "p50": 5.33, "p70": 6.23, "p90": 6.82, "p99": 7.18, "max": 7.22}},
    "multi_turn":  {"total": 6, "passed": 4,
                    "traces_s": {"n": 45, "mean": 6.91, "trimmed_mean": 6.84, "min": 2.78, "p50": 6.52, "p70": 8.03, "p90": 10.79, "p99": 13.57, "max": 14.25},
                    "runs_s":   {"n": 15, "mean": 23.55, "trimmed_mean": 23.31, "min": 12.64, "p50": 21.23, "p70": 28.52, "p90": 33.02, "p99": 36.94, "max": 37.51}}
  }
}
```

`by_mode` is in each run's `summary` and in its `comparison` entry. `total` and `passed` count the evaluated
items of that mode (skipped ones belong to neither). Every distribution is `null` when nothing was timed.
Each item also states its `mode`, its `trace_latencies_s` and its `run_latencies_s`.

- **Per trace is the main figure.** gen-ai starts one trace per chat message, so a trace is one chat turn.
  Its latency is that turn's response time, from sending the message to the end of its stream
  (`turn_wall_clock_sec`), recorded where the chat client completes the turn. It holds none of the LLM judge,
  the simulated user or conversation create/delete. `dashboard_summary` is timed the same way around its one
  request. A turn cut off by its turn or item deadline, or one that ended without a final answer (the agent's
  iteration or token limit, a content filter), still counts, with the time it ran for: those are the slowest
  turns, and the run that scored them is in the per-run figures too. A turn that ended in any other error (an
  error event, or a 503 that outlasted its retries) does not: the time is that of a failed request, not a
  response, and would only add a fast outlier. On the single-shot path such a turn ends its item as an error, so
  it has no per-run figure either. An item that errored outside its evaluator's own failure reporting
  contributes neither.
- **Single-shot** runs are exactly one trace, so `traces_s` is also the latency of a run.
- **Multi-turn** runs span several traces, so they get both views: `traces_s` over every turn of every
  conversation (comparable with single-shot), and `runs_s`, the wall clock of each whole conversation from just
  before its first message to the end of its scoring — every turn, simulated-user reply and judge call, but not
  conversation create/delete. `agentic_conversation` drives its fixture once and contributes one run per item.
  The two single-shot and multi-turn populations are never mixed.
- **Percentiles** use linear interpolation between closest ranks (NumPy's default), so `p50` is the median and
  the report carries no separate median field. On a small sample the high percentiles sit at or near the
  maximum: P99 over fewer than 100 samples is effectively the slowest one, which is why `n` always travels with it.
- **Trimmed mean** (`trimmed_mean`) is the average of the middle 80%: the fastest 10% and the slowest 10% of the
  samples are dropped from each end (`n * 10 // 100` of them, so 25 samples drop two each) before averaging. It is
  not the median, which is one middle value (`p50`). It is `null` below 10 samples, where there is nothing to
  trim and the figure would only repeat `mean`.
- **Older reports** have no `by_mode`. The HTML report says so and nothing is backfilled.

`avg_latency_s` and the other existing fields are unchanged. The console prints each run's pass counts per
mode and one `Latency, <population> (n=...)` line per distribution beneath its summary line, and Trace
P50/P90/P99 columns (single-shot) in the multi-model comparison.

---

## `gd-eval report`

Turns JSON report(s) into one HTML file you can actually navigate. No server, no
credentials, no external assets — it opens over `file://`, attaches to a Jira issue and
survives a Slack thread. It follows GoodData's product look (colours, type, status chips). The faces are Inter, with
Funnel Display for headings, named but never loaded, so a viewer without them gets the system sans and the file stays
self-contained.

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
| `--redact` | Drop conversation/response ids and raw reasoning, and rename models to `Model A`, `Model B`, … A model keeps its letter across all its runs, which are then numbered (`Run 1 · Model A`, `Run 2 · Model A`). Pass rate, per-item results, questions and latency survive. |

The report is a *view* over the JSON. Unfiltered, every figure on it is read from the report, so it cannot
disagree with the console or the JSON. Narrow the selection with a filter and the figures are recomputed in the
page from the selected items' own records, by the same rules gd-eval uses. The page reads top to bottom as a
document, in plain words: a *test case* is one prompt given to the assistant, an *attempt* is one go at it, and the
two formats are *single-question* tests (one answer, no follow-up) and *conversation* tests (a back-and-forth with a
simulated user), which are `single_shot` and `multi_turn` in the JSON.

- **A masthead** with the report's title (`--title`, or "Run history", "Run comparison", "Model comparison" or
  "Run results" plus the model and workspace), when it was generated in the reader's own time zone, and a **Run setup** tooltip listing what
  is the same in every run (model, provider, workspace, dataset, test cases, attempts per test case, pass rule) and
  what differs. Results from different setups are not directly comparable, so a caution icon on a latency row and the
  *New* / *Removed* marks in the test case table say where two runs stopped being alike.
- **View by** — a dropdown above the filters that lays the same report out two ways. **Date** is the layout the
  rest of this list describes: a column per run, oldest to latest by start time, with change lines, sparklines and the latency line
  chart. **Model** compares language models instead: a column per model, ranked best first by the console's winner
  rule (pass rate, then quality, then the quicker average), with no time axis. Where a model has several runs its
  latest stands for it, so each model is read at its most recent state. The Run filter becomes a Model filter, the hint
  beside the dropdown says what is being compared (and names the dates when the compared runs differ in date), and the
  Run setup tooltip does not flag the model itself as a difference. Every report opens on Date, including one that
  compares several models (`gd-eval run --model a --model b --html`); choose Model to compare them. A single run has
  nothing to switch between, so the dropdown is hidden. In the Model view the page reads, top to bottom:
  - **Results** — one row per model, best pass rate first, with a bar of how its evaluated test cases ended (passed
    green, failed red, could not be graded orange), so the green part is the pass rate beside it, and the **Median
    latency** of one attempt (half the attempts were faster, half slower). A list under the table says what each term means. The counts and the
    caution icon (a model evaluated on different test cases than the one with the most) are the date view's Outcomes
    table. There are no headline cards by model: the table is the first thing on the page.
  - **Quality against speed** — each model as a point: the share of test cases it passed against the median time of
    one attempt, the same pass rate as the Results table and the same median as the latency tables. Up and to the left is better. Time runs from zero;
    the pass rate uses the range the models span. It needs two models with timings.
  - **By category** — a heat map of the pass rate per category and model, the best model in each row marked, the
    categories where the models differ most first. Every cell prints its share and its counts, so the shade is never the
    only signal. This is where a model that wins overall but loses on one category shows.
  - **Consistency across attempts** — per model, the share of test cases that passed on at least one attempt (pass@K,
    the light bar) beside the share that passed on every attempt (pass^K, the dark bar), and how many passed only some.
    A long gap is a model that can do the task but not reliably. It appears only for a report that recorded
    `pass_power_k` and attempted a test case more than once.
  - **Latency sections** — the same four percentiles, one row per model, quickest first, with a bar per figure drawn
    from zero beside the numbers. The quickest and slowest model in each column are marked as in the date view.
  - **Test cases** — one result column per model in ranked order, a response-time column per model, and an **Across
    models** column in place of *Since previous run*: *Mixed* (some models passed and some did not; hover to see who),
    *All pass* or *All fail*. A skipped or ungraded test case is left out of the verdict. The table opens on the
    *Mixed* ones, the test cases where the models differ.
- **Filters in two tiers** — the **Filter the report** bar at the top (category, format, result and run) decides what
  the whole page covers: the Results cards, the outcomes table, the latency tables and the test case table all follow it, so the runs stay
  comparable. The Test cases section repeats those four and adds the search box and the expression; they narrow the
  table only, inside whatever the top bar allows, and only offer what the top bar leaves. Category, result and run are
  attribute filters like the product's: a search box, an All row, the values with an **Only** shortcut and a count,
  then Cancel and Apply. Changes are staged in the popup and take effect on Apply; closing it any other way discards
  them. Nothing ticked means all. The run filter chooses which runs are shown; a result matches a test case when any of
  the runs in play has it (so "Failed" over previous and latest finds every test case that broke in either), and the
  expression is evaluated once per run in play with the same any-run rule. A filtered page states how many test cases
  it covers, and each tier has its own Reset.
- **Results** — three headline cards for the latest run: test cases passed (of those evaluated: skipped ones are not
  counted, as in the console's percentage), the average quality score and the median time per attempt. That last one
  pools every format on the page and counts whole attempts, grading included, so it matches neither per-response latency table
  below it; its tooltip says which formats it covers. With an earlier run each card carries one change line in words, "down from 86% on Sep 28", rather
  than a signed number. The line is green when that direction is good and red when it is not, with a chevron and
  screen-reader text (*Better* / *Worse*) so colour is not the only signal. From three runs each card also has a
  sparkline of every run: hover a point for its value, click it to compare the latest run with that one instead of the
  previous. The dot being compared with is drawn white, and a key under the cards says so (latest run, compared with,
  other runs) and that a click on any other dot moves the comparison; it shows only when a sparkline does. A pick that
  a filter has removed, or that has become the latest run, falls back to the previous run. The
  pass-rate card links to the test case table to see *which* ones changed; the split by format lives in that table's
  filters.
- **Outcomes** — how every test case ended, as a table with one row per run, newest first, in the same layout as the
  latency tables. A run is identified by three columns: the **Run date**, the day and time it started (`summary.started_at`,
  shown in the reader's own time zone, the UTC stamp on hover; a report written before it existed shows the date its file is
  named for, without a time), and the **Run name**, the name the run was given, as given, so a run named `2026-09-28` reads
  `2026-09-28` here although the charts style it as "Sep 28", and the **Model** it evaluated, its provider on hover. Then **Passed**, **Failed**, **Could not be graded** (an error left it without a verdict) and
  **Skipped** (not run), then the **Pass rate**. The four are the values of the Result filter, and the pass rate is
  the card's: passed out of the evaluated test cases, skipped ones left out, as in the console. The highest pass rate
  is marked green with an up chevron and the lowest red with a down chevron, and the latest run is marked in lime. A
  caution icon flags a run evaluated over a different number of test cases than the one before, because its pass
  rate is then not a like-for-like change. The counts are read from the run's `summary` (`passed`, `failed`,
  `errored`, `skipped`); a filtered view recounts them from the selected test cases, and a report written before
  `summary.failed` existed shows what the other three leave.
- **Latency sections** — **Single-question tests · response time** first, then **Conversation tests**, which shows
  both per response (each assistant reply, one gen-ai trace) and per conversation (start to finish, with the
  simulated user and the judge). Each opens with a **line chart** of the median (P50), P70, P90 and P99 across the
  runs, oldest on the left and the latest on the right, drawn from zero so line heights compare honestly; the lines
  share one blue that darkens towards the tail. Hover or focus a run for its crosshair and every figure, in a tooltip
  that says how many responses it rests on. A line needs two runs with timings, so with one run the chart is left
  out. End labels name each line and give its latest value, and are dropped when two would touch. Under the chart a
  table has one row per run, newest first, identified by the same **Run date**, **Run name** and **Model** columns as the outcomes table, with the same four figures. The quickest run in each column is marked
  green and the slowest red, each with a chevron (down for least time, up for most) so colour is not the only
  signal, and the latest run is marked in lime. A caution icon flags a run timed on a different number of samples
  than the one before. Unfiltered they are read from `by_mode`; a filtered view recomputes them in the page by the
  same rules. The fastest and slowest single response, the average and the trimmed average stay in the JSON (P99
  over a few dozen samples sits close to the slowest one, which is why `n` travels with it in the tooltip and
  the cell hint). Seconds read with one decimal and no redundant ".0" (`3s`, `4.6s`).
- **A test case table**, newest first: the latest run's result, a **Since previous run** column, then the earlier runs
  going back in time (click any result to open the drawer on that run). Each run's column is headed by its run date over
  its run name, one to a line (hover the heading for the full run label); by model the columns are headed by the model. The change column reads *Regressed* (passed in
  the previous run, not in the latest), *Fixed*, *Flaky* (flipped between pass and fail more than once), *New*
  (in no earlier run) or *Removed* (in an earlier run, gone from the latest). A test case skipped in the latest run
  has no label, since the change would describe earlier runs. With several runs the table opens on the regressions. Two time columns
  keep the populations apart: **Response time** is the median of the test case's assistant responses, and **Time per
  attempt** is the mean wall-clock of a whole attempt (the responses plus the judge and, for conversations, the
  simulated user). With more than two runs shown they follow the latest run only. Hover a value to see every sample
  behind it; the drawer labels its two latency chips the same way. A report written before per-trace timing has no
  response figure and shows `avg_latency_s` as the attempt figure.
- **An expression filter**, folded under *Advanced: filter by a check expression* in the Test cases section, for
  cross-cutting questions the fixed filters can't anticipate, e.g. `d.filter_ranking_score === false` or
  `d.expected_metric_uris.length > 1 && !d.metrics_correct`. Available variables:
  `d` (the checks of the run being read, its `detail`), `it` (that run's result), `i` (the row, `i.per[label]` for any
  run), `q` (question), `kind` (category id).
- **The conversation**, when the test case ran the agentic multi-turn path — every turn in
  order, with the simulated user marked apart from a real question, so you can see
  whether the agent got there or was handed the answer.
- **A per-test-case drawer** — checks as pass/fail chips, expected vs actual side by side,
  the latency timeline, conversation/response ids.
- **A latency timeline** from `detail.latency_breakdown`, in execution order, one bar per
  step. Every step has a chevron that opens its full record in place, joined by `index`: the
  paragraph a reasoning step was summarised from, or a tool call's arguments and result from
  `detail.tool_calls`. A reasoning paragraph's markdown `**title**` is shown as bold text,
  not as asterisks. Any number of steps can be open at once, and the chevron above the list
  opens or closes all of them. The reasoning therefore lives on the timeline; a separate
  Reasoning section appears only for paragraphs no step points at (or when a run recorded no
  timeline).
- **A print stylesheet** that drops the filters and the drawer, so "Save as PDF" gives a clean page.

A report that merges several files names each run after its file, and a file named for its date (`2026-09-28.json`)
reads as "Sep 28". A model is read from the run itself (`model` and the provider), never from the file name, so files
named for their model work as well as files named for their date. In the Date view the page treats the runs as one
model followed over time; when a report holds several models it adds the model to each run's name and points at
**Model** (see above) for the comparison.

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
`search_tool`, `general_question`, `guardrail`, `dashboard_summary`, `document_takeaway`,
`catalog_metadata`.

### `visualization` items

The `expected_output` lists the candidate charts in the AAC format, and the item passes when
the agent's chart matches one of them. Keys beside the candidates add item-level checks:

```json
{
  "id": "sankey-001",
  "dataset_name": "agent_visualization_extended_charts",
  "test_kind": "visualization",
  "question": "Show how net sales flow from product category to customer country.",
  "expected_output": {
    "visualization": {
      "type": "sankey_chart",
      "query": {"fields": {"m": {"using": "metric/net_sales"}, "c": {"using": "label/product_category"},
                           "d": {"using": "label/customer_country"}}},
      "metrics": ["m"],
      "from": "c",
      "to": "d",
      "buckets_strict": true
    },
    "requires_visualization_part": true
  }
}
```

Item-level keys, all optional except the candidates:

- `visualization` — one candidate chart, or a list of them. `expected_outputs`
  (`[{"visualization": {...}}, ...]`) is the same list in the agentic fixture form.
- `requires_execution` — the agent must also run the chart it built.
- `expects_visualization: false` — the agent must answer without a chart, for example by asking
  for a part the request leaves out. The item then lists no candidates.
- `visualization_optional: true` — either an answer without a chart, or a chart that matches a
  candidate, is right.
- `answer_must_include` / `answer_must_not_match` — regular expressions, matched without regard
  to case against the final answer. Every `answer_must_include` pattern must match, and no
  `answer_must_not_match` pattern may.
- `format_intents` — per metric uri, how the metric's numbers must read, for example
  `{"metric/net_sales": {"divide_by": 1000000, "decimals": 1, "suffix": "M"}}`.
- `requires_visualization_part` — the chart must come back as a part of the answer, not only as
  the arguments of the chart tool call.
- `date_filter_from_context` — `true` or `{"dataset": "<date dataset>"}`: a candidate without a
  date filter also accepts the chart carrying a date filter of the dashboard in the item's
  `user_context`. See *Date filter carried over from the dashboard* below.

Switches on a candidate chart:

- `buckets_strict` — compare bucket by bucket, not only the union of the buckets, so swapped
  heatmap rows and columns or a reversed sankey fail.
- `metrics_ordered` — compare the metrics by position, for bullet roles and bubble axes.

Any other key, at item level or on a candidate chart, makes the item error before any request
is sent, because a misspelled key would otherwise be dropped and its check would never run:

```
ValueError: the expectation states ['answer_must_inlcude'], which is not one of ['answer_must_include', ...]
ValueError: a candidate chart states ['bucket_strict'], which the chart model does not read
```

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

### `document_takeaway` items

Takeaway items call the AI Publisher takeaway endpoint
(`POST /api/v1/ai/workspaces/{ws}/takeaway`) with a `takeaway_input` block, authored in
snake_case and sent as the endpoint's camelCase body. In a Langfuse dataset the block goes
in the item's `metadata` (or its `input` object), and `input` can stay a plain case label;
an item carrying `takeaway_input` is a `document_takeaway` item unless it declares another
`test_kind`. The endpoint needs the `enableGenAiReportTakeaways` feature flag.

```json
{
  "id": "takeaway-001",
  "dataset_name": "agent_document_takeaway",
  "test_kind": "document_takeaway",
  "question": "P01 default format, Sales page, no instructions",
  "takeaway_input": {
    "visualizations": ["<visualization id>", {"visualization_id": "<id>", "filters": []}],
    "filter_context": [],
    "instructions": {"document": null, "slot": null, "format_hint": null},
    "max_characters": 300
  },
  "expected_output": {
    "no_data": false,
    "format": {"no_lists": false},
    "must_include": ["States one finding that connects at least two of the charts"],
    "must_not_include": [],
    "rubric": []
  }
}
```

`takeaway_input` requires `visualizations`; unknown keys are rejected. Every
`expected_output` key is optional:

- `no_data` — whether the endpoint must answer `noData`; when either side says no data,
  nothing else is graded.
- `format` — overrides of the deterministic checks, which gate pass/fail: `bold_headline`,
  `max_headline_words` (10), `max_sentences` (2), `max_words` (50), `single_paragraph`,
  `no_lists`, `no_headings`. `false` or `null` switches a check off; unknown keys are
  rejected. `length` (`max_characters`), `no_ids` and `no_meta` always apply.
- `default_rules` — `false` drops the default judge criteria (one finding; no executive
  summary, chart walk-through, background opener, figures, dates, causes the data cannot
  show, chart description).
- `must_include`, `must_not_include`, `rubric` — the item's own judge criteria, graded like
  `dashboard_summary`.

`word_count` and `headline_word_count` are reported in the item detail. The default judge
criteria are calibrated with `make calibrate-takeaway` (needs `OPENAI_API_KEY`); re-run it
after changing their wording. The judge reads the item's `input` as the page label, and the
label can change a verdict, so describe the page and the request in plain words.

The client retries 429/5xx answers and connection failures. A request error that survives
the retries is handled differently by the two entry points: `gd-eval run` aborts the item
with that error, whatever `--runs` is, while the CI entry point
(`evaluate_document_takeaway`) records it as an errored run, keeps the item's other runs,
and raises only when no run completed. A read timeout is not retried, and the CI entry
point records it as an errored run too. Any other 4xx and an unsupported URL scheme are
never retried and fail the item in both.

### `catalog_metadata` items

Catalog items call the Analytics Catalog generate endpoints
(`POST /api/v1/actions/workspaces/{ws}/ai/analyticsCatalog/generateTitle` or
`/generateDescription`) for one object, named by a `catalog_input` block. In a Langfuse
dataset the block goes in the item's `metadata` or its `input` object (`input` wins); a
value that is not an object fails the item. An item carrying
`catalog_input` is a `catalog_metadata` item unless it declares another `test_kind`. The
judge reads the item's `question` as the ground truth, so state the object's real metadata
there in plain words (what a metric computes, which filters a visualization has).

```json
{
  "id": "catalog-001",
  "dataset_name": "analytics_catalog_generate",
  "test_kind": "catalog_metadata",
  "question": "Description for the metric '# of Single Orders'. Its MAQL counts customers who placed exactly one order.",
  "catalog_input": {"object_type": "Metric", "object_id": "of_orders_1", "output": "description"},
  "expected_output": {
    "must_include": ["Says that it counts customers who placed exactly one order."],
    "must_not_include": ["Says the metric counts orders rather than customers."],
    "rubric": []
  }
}
```

`object_type` is one of `Visualization`, `Dashboard`, `Metric`, `Fact`, `Attribute`;
`output` is `title` or `description`; unknown keys are rejected. Every `expected_output`
key is optional:

- `expect_note` — `true` for an object the endpoint must decline: the item passes on no
  text plus a non-empty `note`, and nothing else is graded.
- `format` — overrides of the deterministic checks, which gate pass/fail: `max_words`
  (title 10, description 80), `max_sentences` (title 1, description 4), `no_end_period`
  (title), `no_markup`, `no_ids`. `false` or `null` switches a check off; unknown keys are
  rejected. A generated text (`generated`) and an empty `note` (`no_note`) always apply.
- `must_include`, `must_not_include`, `rubric` — judge criteria, graded like
  `dashboard_summary`. Criteria may name the object's metadata; the judge sees no data.

A 200 answer with no usable text (a null value without a note, or the placeholder
`"string"`) is asked again once; `unusable_retries` in the item detail records it, with
`word_count`. The judge steps are calibrated with `make calibrate-catalog-metadata` (needs
`OPENAI_API_KEY`); re-run it after changing them. Request errors are handled as for
`document_takeaway`; the CI entry point is `evaluate_catalog_metadata`.

### `agentic_agent_switcher` items

Agent-switcher items drive one conversation through several agents. The conversation is created
with `agent_id`; a turn with `switch_to` calls
`POST /api/v1/ai/workspaces/{ws}/chat/conversations/{id}/switchAgent` before its message is sent.
Each of the `--runs` replays every turn on a new conversation. Switching needs the agent-switching
feature flag. With it off, gen-ai binds the new conversation to another agent, and the run fails
before its first message, naming the flag; a 404 on a switch fails the run too. In a Langfuse dataset the block goes in
the item's `metadata` or its `input` object; an item carrying it is an `agentic_agent_switcher`
item unless it declares another `test_kind` or its `expectedOutput` has a `visualization` key (that
infers `vis_agentic`); `metadata.test_kind: "agentic_agent_switcher"` forces the switcher kind.
`question` only labels the item. Stop an item's turns at the alert proposal: the kind never confirms
a proposal and deletes no alerts, so a turn that confirms one ("Yes, create it") creates a real alert
that stays in the workspace.

```json
{
  "id": "switch-001",
  "dataset_name": "agent_switcher",
  "test_kind": "agentic_agent_switcher",
  "question": "Plan with the planner agent, build the alert with the builder agent",
  "expected_output": {},
  "agent_switcher_input": {
    "agent_id": "planner",
    "turns": [
      {"message": "I want to watch revenue every week and hear when it drops below 1000."},
      {
        "message": "Set that up now.",
        "switch_to": "builder",
        "checks": {
          "must_include": ["Restates the plan the user gave earlier: weekly revenue, below 1000."],
          "must_not_include": ["Asks the user to repeat the plan."],
          "skills_used": ["alert"],
          "skills_not_used": ["visualization"],
          "alert_metric": "revenue"
        }
      },
      {"message": "Also chart revenue by region.", "checks": {"visualization": {"metrics": ["revenue"], "attributes": ["region"]}}}
    ]
  }
}
```

`agent_id` and at least one turn are required; unknown keys are rejected at every level. Every
`checks` key is optional:

- `must_include`, `must_not_include` — LLM judge criteria for this turn's answer. The judge sees the
  transcript so far, each earlier answer labelled with the agent that gave it.
- `skills_used`, `skills_not_used` — skills whose tools this turn must (not) run: the `skillsInUse`
  names on the turn's `toolCall` items, read from the conversation items after the last turn. A skill
  still active from an earlier turn counts as soon as one of its tools runs, with no new `set_skills`
  call; a skill that was requested but whose tools never ran does not count. When the items cannot be
  read, every skills check fails.
- `alert_metric` — the primary (first) measure of the turn's alert proposal is this metric id, with or
  without the `metric/` prefix; the comparison measure of a metric-to-metric alert does not count.
- `visualization` — a chart created in this turn uses these `metrics` and `attributes` (label ids),
  with or without the `metric/` / `label/` prefix; extra fields are allowed.

Two diagnostics are read from the conversation items after the last turn of a run that sent every
turn: `agent_stamped` (every assistant item of a turn carries the agent active at that turn) and
`switch_marker` (one system marker with `trigger` `agent_switched` per switch, carrying the new
agent). They are API contracts: the run detail (`diagnostics`, `diagnostic_failures`) and Langfuse
scores record them, but they never fail a run. A run stopped earlier (another bound agent, a failed
switch or send) records neither. When the items cannot be read, a run with a skills check fails, and
any other run records `items_read` under `diagnostic_failures` and is still graded. Items belong to
the turn whose `responseId` they carry, so a send the client retried does not shift the later turns.
A switch to the agent already bound changes nothing and expects no marker. A run fails before its
first message when the new conversation is bound to another agent (`agent_bound`). Per-turn checks
are reported as `turn<N>_<check>`, e.g. `turn2_skills_used`, `turn2_include_0`. The CI entry point
is `evaluate_agentic_agent_switcher`, which takes the whole item; `--agent-id` does not apply.

### `agentic_memory` items

Memory items check AI memory (organization- and workspace-level memory items). Each run sends
`question` in a new conversation and is graded twice; it passes only when both pass:

- `memory_injected` (code) — the memory items gen-ai injected into the turn's prompt, read from the
  `applyMemory` detail of the turn's conversation items (`/items`), hold every title in
  `memory_input.injected` and none in `memory_input.not_injected`. A turn with other details and
  no `applyMemory` injected nothing, so an item with only `not_injected` titles passes there.
  gen-ai records the details only while the `enableGenAiInteractionIntelligence` feature flag is on
  for the organization. A turn with no detail at all, or items that cannot be read, leave the
  injected memory unknown: the run fails with the check `memory_read` (also the name of its
  Langfuse score) and the exit `chat_error`. The message of a turn without details names the flag.
- `memory_answer_pass` (judge) — the answer against `expected_output`, with the
  `agentic_general_question` judge steps. The judge reads text only, so a chart the turn created
  is given to it as one line with the chart's title and type.

Titles are compared exactly. Injected means "in the prompt", not "followed": gen-ai presents memory
as defaults, so whether the answer applies an item is the judge's part. In a Langfuse dataset the
block goes in the item's `metadata` or its `input` object; an item carrying it is an `agentic_memory`
item unless it declares another `test_kind` or its `expectedOutput` has a `visualization` key (that
infers `vis_agentic`), as for the other structured inputs; `metadata.test_kind: "agentic_memory"`
forces the memory kind.

```json
{
  "id": "om-auto-returns",
  "dataset_name": "org_memory",
  "test_kind": "agentic_memory",
  "question": "Which product categories had the most returned orders in 2024? Anything I should keep in mind?",
  "expected_output": "The answer mentions that orders can be returned within 30 days of delivery.",
  "memory_input": {
    "injected": ["help-line", "returns-30-days"],
    "not_injected": ["returns-14-days-disabled"]
  }
}
```

At least one title is required, and a title cannot be in both lists. The CI entry point is
`evaluate_agentic_memory`, which takes the whole item.

### `agentic_knowledge` items

Knowledge items ask the AI chat questions it answers from knowledge documents (tools
`search_knowledge` and `get_knowledge_chunks`). Each run is a fresh conversation that sends
`expected_output.setup_turns` in order (no simulated user), then `question`, and grades the
answer to `question`. `question` is the graded turn; `setup_turns` (a JSON array of non-empty
strings, optional) holds the earlier user turns of a multi-turn item, as in `agentic_search`.
In a Langfuse dataset, set `test_kind` (in
`metadata` or `expectedOutput`) to route an item to this kind.

```json
{
  "id": "kn-001",
  "dataset_name": "agent_knowledge",
  "test_kind": "agentic_knowledge",
  "question": "And for 45 %?",
  "expected_output": {
    "setup_turns": ["Who must approve a 30 % discount?"],
    "expected_documents": ["Discount Policy"],
    "forbidden_documents": ["Discount Policy 2023"],
    "expected_source": "the parent workspace",
    "must_include": ["Says that discounts above 40 % are not allowed."],
    "must_not_include": ["Says that the CFO must approve the discount."]
  }
}
```

Every `expected_output` key is optional; unknown keys and wrong types are rejected before
any request. Code checks over the knowledge tool results of all turns gate the verdict, so a
failed item shows whether retrieval (document never found) or reasoning (found, answered
wrong) failed:

- `expect_search` (default `true`) — at least one `search_knowledge` call (`knowledge_searched`).
- `expected_documents` — each title is in some knowledge tool result (`expected_documents_found`).
- `forbidden_documents` — no title is in any knowledge tool result (`forbidden_documents_absent`).
- `expected_source` — an expected document's result carries this `source` label
  (`expected_source_found`); needs `expected_documents`. One of gen-ai's labels: `this
  workspace`, `the parent workspace`, `an ancestor workspace`, `AI Hub`.
- `must_include`, `must_not_include`, `rubric` — judge criteria on the answer to `question`,
  graded like `dashboard_summary`; the judge reads the setup turns and their answers as INPUT.

Titles match case-insensitively on a result's `title` or `filename`. An answer to `question`
without text fails (`answered`). Diagnostics that never gate: `documents_retrieved`,
`sources_cited` (titles in the answer's trailing "Sources" list) and `turn_count`. Langfuse
gets `knowledge_pass` plus each code check as its own score per run; `quality_score` counts the
code checks and judge verdicts. A run the judge could not grade is an ERROR (`eval_error`), not
a fail. The judge steps are calibrated with
`make calibrate-knowledge` (needs `OPENAI_API_KEY`); the CI entry point is
`evaluate_agentic_knowledge`.

### `agentic_alert_skill` update items

An alert item with `"mode": "update"` asks the agent to change an alert that exists before the
question. Each run creates the setup alert through the API, asks `question`, then reads the
stored alert again and deletes it. A setup alert an earlier run left is deleted first; an alert
with the same title that no evaluation created stops the item instead, so give each setup alert
a title unique in the workspace. The simulated user confirms the requested change and declines
any other change.

```json
{
  "question": "Raise the threshold of my \"Net Sales floor u1\" alert to $60,000.",
  "expected_output": {
    "mode": "update",
    "setup_alert": {
      "attributes": {
        "title": "Net Sales floor u1",
        "state": "ACTIVE",
        "alert": {
          "execution": {
            "measures": [
              {
                "localIdentifier": "net_sales",
                "definition": {"measure": {"item": {"identifier": {"id": "net_sales", "type": "metric"}}}}
              }
            ],
            "attributes": [],
            "filters": []
          },
          "condition": {
            "comparison": {
              "operator": "LESS_THAN",
              "left": {"localIdentifier": "net_sales", "title": "Net Sales"},
              "right": {"value": 50000}
            }
          },
          "trigger": "ALWAYS"
        }
      },
      "relationships": {"analyticalDashboard": {"data": {"id": "<dashboard id>", "type": "analyticalDashboard"}}}
    },
    "expected_change": {"threshold": 60000}
  }
}
```

- `setup_alert` — the automation entity as the API returns it: `attributes` (with a unique
  `title` the agent finds the alert by) and optional `relationships`. Without `recipients` the
  alert goes to the token owner; without `notificationChannel` it uses the organization's
  channel with the lowest id.
- `expected_change` — the new value of each changed field: `threshold` and `operator`
  (comparison and relative alerts), `sensitivity` and `granularity` (anomaly alerts),
  `trigger`, `trigger_interval` (with the `ONCE_PER_INTERVAL` trigger), `title`, `state`
  (`ACTIVE`/`PAUSED`), `filters` (the whole list, in any order) and `dashboard_id`. A
  `trigger` change may set or clear the interval, unless the alert is `ONCE_PER_INTERVAL`
  before and after it.

An update item takes no other key, and a change the setup alert cannot take is rejected before
any request. The run publishes four scores instead of the creation checks:
`alert_update_called` (an `update_metric_alert` or `update_alert_state` call on the alert
succeeded, also after a failed one), `alert_update_correct` (the stored alert holds every
expected value), `alert_update_preserved` (no other stored field changed; the timestamps,
the editors and the generated `description` are not compared) and `alert_not_recreated`
(the alert still exists and the agent created none). A failing run reports the update
arguments and every field that changed unasked.

### `agentic_kda_skill` field checks

A KDA item is scored on completion: `kda_triggered`, `kda_executed`, `kda_success` and
`kda_turn_completed`. With `"check_fields": true` the run must also match every field of the
`create_key_driver_analysis` call and the summary its execution returns:

```json
{
  "question": "What drove the change in Total Sales Amount in Q4 2024 versus Q3 2024, excluding the United States East region?",
  "expected_output": {
    "check_fields": true,
    "Measure": {"id": "total_sales_amount_daily_store", "type": "metric"},
    "Date Attribute": "transaction_date.quarter",
    "Analyzed Period": "2024-4",
    "Reference Period": "2024-3",
    "Filters": [
      {"type": "attribute_filter", "using": "label/dim_geography_region.region_name", "state": {"exclude": ["United States East"]}}
    ],
    "Summary": {"analyzed_value": 13868253.55, "reference_value": 15142121.31, "change": -1273867.76, "absolute_tolerance": 0.01}
  }
}
```

| Score | Passes when |
|---|---|
| `kda_measure_correct` | the measure has the id and type of a `Measure` candidate (one object or a list), and its aggregation when the candidate states one |
| `kda_date_attribute_correct` | `date_attribute_id` equals `Date Attribute` |
| `kda_analyzed_period_correct`, `kda_reference_period_correct` | the period has the expected parts, numbers compared as numbers (`2024-1` is `2024-01`, `2024-Q3` is not `2024-3`) |
| `kda_filters_correct` | the non-date filters equal `Filters` in any order (`[]` for none). Date filters are not compared: the periods set the scope, and a date filter that changes the numbers fails the summary |
| `kda_summary_correct` | the execution succeeded and each of `analyzed_value`, `reference_value` and `change` the item states is within `absolute_tolerance` (default 0.01) |

`any_of` lists complete alternatives for a question two answers fit. Each option replaces some
of the fields, and a run passes when one option matches all six. The summary depends on the
date attribute, so an option that changes one states both:

```json
"any_of": [
  {"Date Attribute": "transaction_date.quarter", "Summary": {"analyzed_value": 184, "reference_value": 163}},
  {"Date Attribute": "return_date.quarter", "Summary": {"analyzed_value": 191, "reference_value": 156}}
]
```

A missing field, an unknown key, `check fields` or `any of` spelled with a space or capitals, a
measure type or aggregation the tool does not take, an attribute filter without one non-empty
`include` or `exclude` list of strings, a date filter in `Filters` or `any_of` without
`check_fields` is rejected before any request. The execute call is paired with the create whose
`kda_ref` it names; an execute naming a ref no create of the turn returned is not counted, and a
create the tool rejected after an analysis ran does not replace it. `filters` that are not a list
fail `kda_filters_correct`; omitted ones are no filters. The six names are `KDA_FIELD_SCORES`; a run that never called
create publishes none of them. A failing run reports the expected and the actual value of each
field it failed.

### Items asked in a dashboard context (`user_context`)

An item can be asked the way a user asks from an open dashboard or an attached widget.
Its `user_context` is sent verbatim as `userContext` on every chat message of the item,
follow-up and clarification messages included — the server treats a message without one
as a cleared context. Requires the `enableAiContextSetup` feature flag on the target
organization — without it the server ignores the dashboard view. Applies to chat items
only; `dashboard_summary` and `document_takeaway` items carry their scope in
`summary_input` / `takeaway_input` instead. No
`userContext` key is sent at all when neither the item nor, for `agentic_conversation`,
the current turn sets one.

```json
{
  "id": "ctx-001",
  "dataset_name": "my_dataset_ctx",
  "test_kind": "general_question",
  "question": "Which dashboard am I looking at, and what does it cover?",
  "user_context": {
    "view": {
      "dashboard": {
        "id": "sales_overview",
        "title": "Sales Overview",
        "widgets": [
          {"widgetType": "insight", "widgetId": "w1", "title": "Revenue by Month", "visualizationId": "revenue_by_month"}
        ]
      }
    }
  },
  "expected_output": "Names the Sales Overview dashboard and summarizes its charts."
}
```

The schema belongs to the AI chat API (`UserContext`: `view.dashboard`,
`referencedObjects`, `activeObject`), so it is not validated here beyond being an object.
In a Langfuse dataset, put it in the item `metadata` (or in the `input` object) under
`user_context`. An object in `input` wins and `metadata` is then not read; a missing or
`null` value in `input` falls back to `metadata`. The value used must be an object or `null`;
anything else fails the dataset load.

#### Date filter carried over from the dashboard

A user who asks for a new chart from an open dashboard without naming a period may get the
dashboard's date filter on the chart, and the product accepts that as well as a chart with no
date filter. An item says so with `date_filter_from_context`:

```json
"expected_output": {
  "visualization": {"type": "headline_chart", "query": {"fields": {"m": {"using": "metric/gross_margin_pct"}}}, "metrics": ["m"]},
  "date_filter_from_context": {"dataset": "dataset/transaction_date"}
}
```

Each candidate without a date filter then also counts once more per date filter in
`user_context.view.dashboard.filters`, with that filter added. Both sides resolve against the
same day, so a relative and an absolute period that cover the same days match. The date dataset
of the added filter is, in order: the `dataset` the key states; the one the dashboard filter
names in `using` (a bare id such as `order_date` reads as `dataset/order_date`); for the
dashboard's common date filter, which names none, the one the chart's only date filter uses.
`true` therefore accepts any date dataset for the common date filter. The key's `dataset` must
be a bare id or a `dataset/` URI; anything else, such as `label/region` or a misspelled
`datset/order_date`, is an error. A dashboard filter whose `using` is not a date dataset adds
no candidate.

A candidate that states a date filter is not extended: a question that names a period is scored
on that period only. A chart with two date filters matches no added candidate. Ranking and
attribute filters are unaffected.

When the chart matches an added candidate, the run detail carries
`filter_date_context: {"inherited": true, "dataset": ...}` and a failure summary shows
`date : True (matches the dashboard date filter in user_context)`. The expected output reported
is still the candidate the item states; `expected_filters` shows the dashboard filter it was
scored with. A stated candidate that matched the date wins over an added one it ties with. Without the key an item is
scored exactly as before, so an item that must reject the dashboard's period ("all time")
simply leaves it out. The key on an item whose `user_context` has no dashboard date filter is
an error, raised before any request. Applies to `visualization`, `vis_agentic` and
`agentic_visualization` items; `agentic_conversation` turns do not read it.

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
| `catalog_metadata` | Analytics Catalog title or description for one object (via the `analyticsCatalog/generate*` endpoints): format checks plus a rubric scored by LLM | `[llm-judge]` |
| `agentic_agent_switcher` | One conversation switched between agents: each answer stamped with the active agent, one switch marker per switch, and per-turn judge, skill, alert and chart checks | `agent_switcher_input`; `[llm-judge]` for judge criteria |
| `agentic_knowledge` | Answer from knowledge documents, after optional setup turns: retrieval checks on the knowledge tool results plus a rubric on the last answer scored by LLM | `[llm-judge]` |

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
