# Evaluating the Summary Skill

> Presentation deck — one slide per `---` separator.

---

## Evaluating the Summary Skill

**Goal:** verify GoodData's dashboard-summary feature — both that it *works* and that it's *good*.

**Challenge:** summaries are free text — non-deterministic, no single "correct" answer.

**Strategy:** split into two concerns, test each with the right tool.

---

## Two concerns, two tools

| | **Does it work?** | **Is it good?** |
|---|---|---|
| Concern | Integration / pipeline wiring | Content quality / regressions |
| Tool | **Playwright e2e** (chat skill) | **`gd-eval`** (`/summary` endpoint) |
| Asserts | A summary appears, no error | Rubric criteria, model A vs B |
| Cadence | CI smoke | Eval / model-comparison runs |

→ Don't force one tool to do both. Quality is `gd-eval`'s job; integration is Playwright's.

---

## The two server-side paths

| | **`/summary` endpoint** | **Chat skill (`userContext`)** |
|---|---|---|
| Endpoint | `POST .../ai/workspaces/{ws}/summary` | `POST .../chat/.../messages` |
| Input | viz IDs + dashboard ID + filters | full context **incl. `resultId`s** |
| AFM exec | **server-side (automatic)** | must be done first (frontend does it) |
| Response | plain JSON (sync) | SSE stream |

- **Quality** → evaluate via the **endpoint** (clean JSON, no AFM/SSE plumbing).
- **Chat skill** → smoke-test via **Playwright** (the real UI builds `userContext` + runs AFM for free).

---

## Quality eval — how `gd-eval` does it

1. New `SummaryClient` POSTs the request → gets JSON `{ summary, ... }`.
2. Summary text wrapped into the existing `ChatResult`.
3. New `dashboard_summary` evaluator scores it with the **LLM judge**.
4. Standard scores out: `pass@K`, `quality_score`, `value_score`, `latency`.
5. Optional **Langfuse** experiment logging — unchanged.

---

## Why not exact-match? → Rubric scoring

A good summary can be phrased many valid ways → **don't compare strings**.

`expected_output` is a **rubric of checkable criteria**; the judge scores each true/false:

```
quality_score = (criteria satisfied) / (total criteria)
```

- Partial credit (7/8 facts = 0.875) → smooth, stable metric.
- Non-determinism averages out instead of flipping pass/fail.
- Plugs into existing scoring — no core change.

---

## What goes in the dataset

```jsonc
{
  "id": "sales-overview-01",
  "test_kind": "dashboard_summary",
  "question": "Summarize the Sales Overview dashboard",   // label
  "summary_input": {                       // → request to /summary
    "dashboard_id": "sales_overview",
    "visualizations": ["revenue_by_quarter", "revenue_by_region"],
    "filter_context": [],
    "format_hint": "3 bullet points"
  },
  "expected_output": {                     // → the rubric (judge target)
    "must_include":     ["Revenue ≈ $4.2M", "Grew QoQ", "West is top region"],
    "must_not_include": ["Segments/metrics not in the data", "Fabricated numbers"],
    "rubric":           ["Captures trend", "Names best/worst segment", "Respects format"]
  }
}
```

- **must_include** → facts that define **pass/fail**
- **must_not_include** → hallucination / accuracy guards
- **rubric** → soft quality dimensions (graded only)

---

## Handling non-determinism

- **Agent variance** → run `--runs K`; watch **mean quality + pass rate**, not just best-of-K.
- **Judge variance** → low temperature + **decomposed yes/no criteria** (biggest lever).
- **Ground facts in real data** — numbers must match what the visualizations return (allow tolerance, "≈ $4.2M").
- ⚠️ Datasets are **workspace-coupled** (IDs + expected numbers tied to one environment).

---

## Chat skill — Playwright smoke test

Tests the *real* pipeline: UI → chat → summary skill → AFM → LLM.

- **The UI does the hard parts for free** — assembles `userContext`, executes AFM for `resultId`s. No Python AFM client needed.
- **Keep assertions loose:** summary panel renders, text non-empty, no error, within timeout.
- ❌ Do **not** assert content quality here — that's what makes e2e flaky.

⚠️ **Prerequisite:** confirm the chat skill and the `/summary` endpoint share the **same summarizer**. If yes → endpoint quality-eval covers the skill's content too. If they diverge → chat-skill quality is only smoke-covered.

---

## Out of the box vs. to be implemented

**✅ Reused as-is**
- CLI, connection, profiles, model/provider selection
- Run loop, `pass@K`, `quality`/`value`/`latency` scores
- LLM-as-judge infrastructure (`[llm-judge]` extra)
- Console + JSON reports; Langfuse source & sink

**🛠️ To implement — quality (`gd-eval`)**
- `SummaryClient` → calls `/summary`, maps JSON → `ChatResult`
- `dashboard_summary` test kind + `summary_input` dataset fields
- Multi-criterion judge (rubric → list of booleans)
- Backend dispatch by `test_kind`; docs + tests

**🛠️ To implement — integration (Playwright)**
- One e2e smoke test in the web-app suite

---

## Summary

- **Two concerns, two tools:** quality via `gd-eval` + `/summary`; integration via Playwright.
- **Rubric-based dataset** — facts to include, things to avoid, quality criteria.
- **Graded scoring** tames non-determinism; reuses existing `gd-eval` metrics.
- **Playwright** smoke-tests the chat skill cheaply (UI builds the hard parts).
- **First check:** do both paths share the summarizer? Drives whether quality is fully covered.
