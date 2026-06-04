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

### All flags

#### Connection

| Flag | Env var | Description |
|---|---|---|
| `--host HOST` | — | GoodData host URL. |
| `--token TOKEN` | `GOODDATA_TOKEN` | API token. Pass via flag or env var. |
| `--profile NAME` | — | Profile name in `~/.gooddata/profiles.yaml` (same file as the `gdc` CLI). |
| `--workspace ID` | — | **Required.** Workspace id to evaluate against. |

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

#### Output

| Flag | Description |
|---|---|
| `--json PATH` | Write a JSON report to this path. Always uses the nested `{models, runs, comparison}` shape even for a single model. |
| `--quiet` | Suppress per-item progress. Per-model result tables and the comparison summary are still printed. |

#### Langfuse sink

| Flag | Description |
|---|---|
| `--langfuse` | Log scores and traces to Langfuse after each item. Requires `--langfuse-dataset`. Creates one named experiment run per model (`gd-eval-{timestamp}-{model}`). Requires `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`. |

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
`search_tool`, `general_question`, `guardrail`.

## Supported test kinds

| test_kind | What the agent must produce | Extra required |
|---|---|---|
| `visualization` | Correct AAC visualization (metrics, dimensions, filters, type) | — |
| `metric_skill` | `create_metric` tool call with correct MAQL and format | — |
| `alert_skill` | `create_metric_alert` tool call with correct operator, threshold, trigger, filters, metric, recipients | — |
| `search_tool` | `search_objects` tool call (correct function called = pass; correct arguments = quality score) | — |
| `general_question` | Text answer judged by LLM | `[llm-judge]` |
| `guardrail` | Refusal/redirect (visualization response auto-fails) | `[llm-judge]` |

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
