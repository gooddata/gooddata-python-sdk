# gooddata-eval

CLI to evaluate the GoodData AI agent against a dataset of natural-language
questions on a chosen workspace and LLM model.

## Install

    uv add gooddata-eval

Or install `gd-eval` as a standalone tool:

    uv tool install gooddata-eval

## Quick start

```bash
export GOODDATA_TOKEN='your-api-token'

gd-eval run \
  --host  https://your.gooddata.cloud \
  --workspace  demo \
  --dataset  ./my-dataset \
  --model  gpt-5.2 \
  --runs  2 \
  --json  results.json
```

## All flags

### Connection

| Flag | Env var | Description |
|---|---|---|
| `--host HOST` | — | GoodData host URL (e.g. `https://your.gooddata.cloud`). |
| `--token TOKEN` | `GOODDATA_TOKEN` | API token. Pass via flag or env var. |
| `--profile NAME` | — | Profile name in `~/.gooddata/profiles.yaml` (same file as the `gdc` CLI). Provides host + token when both flags are omitted. |
| `--workspace ID` | — | **Required.** Workspace id to evaluate against. |

### Dataset source (pick one)

| Flag | Description |
|---|---|
| `--dataset PATH` | Path to a flat folder of JSON files — one question per file. |
| `--langfuse-dataset NAME` | Pull dataset items by name from Langfuse. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` env vars. |

### Model selection

| Flag | Description |
|---|---|
| `--model ID` | LLM model id to evaluate (e.g. `gpt-5.2`). Defaults to the workspace's currently active model. If the model is offered by a different provider than the active one, the workspace's active provider is switched automatically. |
| `--provider NAME_OR_ID` | LLM provider name or id. Use when `--model` is offered by multiple providers and you need to pick one. Accepts either the human-readable provider name or its UUID id. |

### Evaluation

| Flag | Default | Description |
|---|---|---|
| `--runs K` | `2` | Number of independent conversation runs per item (pass@K). An item passes if any run passes. |

### Output

| Flag | Description |
|---|---|
| `--json PATH` | Write a machine-readable JSON report (keyed by item id, with per-item scores) to this path. Console summary is always printed. |
| `--quiet` | Suppress per-item progress output. Only the final table and summary are printed. |

### Langfuse sink

| Flag | Description |
|---|---|
| `--langfuse` | Log evaluation results to Langfuse after each item. Requires `--langfuse-dataset` (so item ids can be linked to Langfuse dataset items). Creates a named experiment run (`gd-eval-{timestamp}-{model}`) in the Langfuse dataset. Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |

## Dataset format

A dataset is a folder of `.json` files, one per question. Each file must
contain a common envelope:

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

See the full dataset specification for `expected_output` shapes per test kind.

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
is the fraction of satisfied criteria. A runnable template lives in
[`examples/summary_dataset/`](examples/summary_dataset/).

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

`general_question` and `guardrail` items are scored by an LLM judge (GPT-4o)
that compares the agent's text response against your expected-output description.
This requires the OpenAI Python package and an API key:

```bash
uv add 'gooddata-eval[llm-judge]'        # project dependency
# or, for the standalone gd-eval tool:
uv tool install 'gooddata-eval[llm-judge]'
```

Set your OpenAI key before running:

```bash
export OPENAI_API_KEY='sk-...'
```

Without `[llm-judge]`, items with `test_kind: general_question` or `guardrail`
are reported as **skipped**.


## Exit codes

| Code | Meaning |
|---|---|
| `0` | Run completed. Evaluation failures do **not** cause a non-zero exit — check the report. |
| `2` | Operational error: bad connection, missing model, unreadable dataset, missing credentials. |

## Scores (in JSON report and Langfuse)

| Score | Description |
|---|---|
| `pass_at_k` | 1 if any of the K runs passed strict checks, else 0. |
| `quality_score` | Fraction of strict check flags that are `True` (0.0–1.0). Shown in CLI as a percentage. |
| `value_score` | Weighted blend: 0.6 × quality + 0.2 × speed (where speed = max(0, 1 − latency/60s)). |
| `latency_s` | Average per-run latency in seconds. |
