# (C) 2026 GoodData Corporation
import json
import re
import shutil
import subprocess

import orjson
import pytest
from gooddata_eval.cli.main import main
from gooddata_eval.core.reporting.html_report import _aliases, build_html, load_report_files, merge_docs


def _doc(model: str, passed: bool) -> dict:
    return {
        "models": [model],
        "runs": {
            model: {
                "model": model,
                "workspace_id": "ws1",
                "summary": {"total": 1, "passed": int(passed), "failed": int(not passed), "avg_latency_s": 2.5},
                "items": {
                    "item-1": {
                        "test_kind": "visualization",
                        "question": "How many orders?",
                        "pass_at_k": passed,
                        "conversation_id": "conv-secret",
                        "response_id": "resp-secret",
                        "reasoning": ["**Thinking**\n\ninternal thoughts"],
                        "detail": {
                            "metrics_correct": passed,
                            "latency_breakdown": [
                                {"seq": 0, "kind": "tool", "name": "search", "index": 0, "duration_s": 1.0}
                            ],
                            "turns": 2,
                            "transcript": [
                                {"turn": 1, "role": "user", "text": "How many orders?"},
                                {"turn": 1, "role": "assistant", "text": "Which order status?"},
                                {"turn": 2, "role": "simulated_user", "text": "primed with the expected answer"},
                            ],
                        },
                        "failed_runs": [
                            {
                                "run_index": 2,
                                "passed": False,
                                "error": None,
                                "conversation_id": "run-conv-secret",
                                "response_id": "run-resp-secret",
                                "reasoning_step_count": 1,
                                "reasoning_steps": ["**Thinking**\n\nper-run internal thoughts"],
                                "tool_call_count": 1,
                                "tool_names": ["search_objects"],
                                "latency_s": 3.5,
                                "detail": {
                                    "metrics_correct": False,
                                    "turns": 1,
                                    "transcript": [
                                        {"turn": 1, "role": "simulated_user", "text": "per-run primed answer"}
                                    ],
                                    "tool_calls": [{"name": "search_objects", "result": "row data"}],
                                },
                            }
                        ],
                    }
                },
            }
        },
        "comparison": {model: {"passed": int(passed), "total": 1, "pass_rate": float(passed)}},
    }


def _embedded(html: str) -> dict:
    blob = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1)
    return json.loads(blob)


def test_merges_files_into_one_run_per_source(tmp_path):
    for name, passed in (("run-a", True), ("run-b", False)):
        (tmp_path / f"{name}.json").write_bytes(orjson.dumps(_doc("gpt-5", passed)))

    doc = load_report_files([tmp_path / "run-a.json", tmp_path / "run-b.json"])

    # Same model in both files must stay two columns, not overwrite each other.
    assert sorted(doc["runs"]) == ["run-a · gpt-5", "run-b · gpt-5"]
    assert sorted(doc["comparison"]) == ["run-a · gpt-5", "run-b · gpt-5"]


def test_legacy_single_run_file_is_accepted(tmp_path):
    legacy = _doc("gpt-5", True)["runs"]["gpt-5"]
    (tmp_path / "old.json").write_bytes(orjson.dumps(legacy))

    assert list(load_report_files([tmp_path / "old.json"])["runs"]) == ["gpt-5"]


def test_html_embeds_parseable_data_and_no_external_refs():
    html = build_html(_doc("gpt-5", False))

    data = _embedded(html)
    assert data["runs"]["gpt-5"]["items"]["item-1"]["conversation_id"] == "conv-secret"
    assert not re.search(r'(src|href)="(?!#)', html), "report must be self-contained"


def test_redact_drops_ids_reasoning_and_model_name():
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "conv-secret" not in html
    assert "resp-secret" not in html
    assert "internal thoughts" not in html
    assert "gpt-5" not in html
    data = _embedded(html)
    assert list(data["runs"]) == ["Model A"]
    # The evaluation itself survives redaction -- only identity goes.
    assert data["runs"]["Model A"]["items"]["item-1"]["question"] == "How many orders?"
    assert data["runs"]["Model A"]["items"]["item-1"]["detail"]["latency_breakdown"]


def test_redact_gives_one_model_one_alias_across_its_runs() -> None:
    """The alias follows the model, not the run, or one model's history reads as several models and the page
    says the report holds more than one. The runs are numbered instead."""
    merged = merge_docs([("2026-09-28", _doc("gpt-5", True)), ("2026-10-05", _doc("gpt-5", False))])

    html = build_html(merged, redact=True)

    assert "gpt-5" not in html
    data = _embedded(html)
    assert list(data["runs"]) == ["Run 1 · Model A", "Run 2 · Model A"]
    assert list(data["comparison"]) == ["Run 1 · Model A", "Run 2 · Model A"]
    # What the page counts models by (its provider and its model name) is the same for both runs.
    assert {run["model"] for run in data["runs"].values()} == {"Model A"}
    assert {entry["provider_name"] for entry in data["comparison"].values()} == {""}


def test_redact_alias_survives_past_twenty_six_models() -> None:
    """chr(65 + n) walked off the alphabet: the 27th model was `Model [`."""
    doc = {"runs": {f"m{i}": {"model": f"model-{i}", "items": {}} for i in range(30)}, "comparison": {}}

    names = [name.removeprefix("Model ") for _, name in _aliases(doc).values()]

    assert len(set(names)) == 30
    assert all(name.isalpha() for name in names), names
    assert names[25:28] == ["Z", "AA", "AB"]


def test_redact_gives_each_model_its_own_letter_and_numbers_only_a_repeated_model() -> None:
    merged = merge_docs([("a", _doc("gpt-5", True)), ("b", _doc("claude", True)), ("c", _doc("gpt-5", False))])

    data = _embedded(build_html(merged, redact=True))

    assert list(data["runs"]) == ["Run 1 · Model A", "Model B", "Run 2 · Model A"]
    assert [run["model"] for run in data["runs"].values()] == ["Model A", "Model B", "Model A"]
    # Each run keeps its own results under its new label.
    assert data["comparison"]["Run 2 · Model A"]["passed"] == 0
    assert data["comparison"]["Run 1 · Model A"]["passed"] == 1


def test_redact_keeps_apart_a_model_id_served_by_two_providers() -> None:
    """The page tells models apart by provider as well as id, so redaction must not merge them."""
    openai, azure = _doc("gpt-5", True), _doc("gpt-5", True)
    openai["comparison"]["gpt-5"]["provider_name"] = "OpenAI"
    azure["comparison"]["gpt-5"]["provider_name"] = "Azure"

    html = build_html(merge_docs([("a", openai), ("b", azure)]), redact=True)

    assert "OpenAI" not in html and "Azure" not in html
    assert list(_embedded(html)["runs"]) == ["Model A", "Model B"]


def test_redact_reads_the_model_from_the_label_of_a_run_that_does_not_name_it() -> None:
    """An older report has no `model` on the run; the page falls back to the part of the label after the source."""
    first, second = _doc("gpt-5", True), _doc("gpt-5", False)
    del first["runs"]["gpt-5"]["model"], second["runs"]["gpt-5"]["model"]

    data = _embedded(build_html(merge_docs([("a", first), ("b", second)]), redact=True))

    assert list(data["runs"]) == ["Run 1 · Model A", "Run 2 · Model A"]


def test_redact_drops_the_transcript_but_keeps_the_turn_count():
    html = build_html(_doc("gpt-5", False), redact=True)

    # The simulated user is primed with the expected output, so the exchange discloses how
    # we score. "It took 2 turns" is still a fair thing to show a customer.
    assert "primed with the expected answer" not in html
    detail = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["detail"]
    assert "transcript" not in detail
    assert detail["turns"] == 2


def test_redact_reaches_inside_failed_runs():
    """Per-run records carry their own ids and their own raw reasoning.

    Redacting only the item's top level left the identical content one level down: the
    top-level `reasoning` was dropped while the same text survived verbatim in
    `failed_runs`, in a report labelled customer-safe.
    """
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "run-conv-secret" not in html
    assert "run-resp-secret" not in html
    assert "per-run internal thoughts" not in html

    run = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["failed_runs"][0]
    assert "conversation_id" not in run
    assert "response_id" not in run
    assert "reasoning_steps" not in run
    # What the run actually did survives -- the same line the top level draws.
    assert run["run_index"] == 2
    assert run["passed"] is False
    assert run["reasoning_step_count"] == 1
    assert run["tool_names"] == ["search_objects"]
    assert run["latency_s"] == 3.5


def test_redact_reaches_inside_a_failed_run_s_own_detail():
    """A per-run `detail` carries the same transcript and tool payloads as the top one."""
    html = build_html(_doc("gpt-5", False), redact=True)

    assert "per-run primed answer" not in html
    assert "row data" not in html

    detail = _embedded(html)["runs"]["Model A"]["items"]["item-1"]["failed_runs"][0]["detail"]
    assert "transcript" not in detail
    assert "tool_calls" not in detail
    assert detail["turns"] == 1
    assert detail["metrics_correct"] is False


def test_failed_runs_survive_an_unredacted_report():
    """The field is diagnostic data; only `--redact` strips it."""
    run = _embedded(build_html(_doc("gpt-5", False)))["runs"]["gpt-5"]["items"]["item-1"]["failed_runs"][0]

    assert run["conversation_id"] == "run-conv-secret"
    assert run["reasoning_steps"] == ["**Thinking**\n\nper-run internal thoughts"]


def test_closing_script_tag_in_data_cannot_break_out():
    doc = _doc("gpt-5", False)
    doc["runs"]["gpt-5"]["items"]["item-1"]["question"] = "</script><script>alert(1)</script>"

    html = build_html(doc)

    # The blob must survive to the end of the payload -- if a "</script>" inside the data
    # had terminated the host tag early, this capture would be truncated and not parse.
    assert _embedded(html)["runs"]["gpt-5"]["items"]["item-1"]["question"] == "</script><script>alert(1)</script>"


def test_cli_report_command_writes_html(tmp_path):
    src = tmp_path / "results.json"
    src.write_bytes(orjson.dumps(_doc("gpt-5", True)))
    out = tmp_path / "report.html"

    assert main(["report", str(src), "-o", str(out), "--title", "MSXi eval"]) == 0
    assert "MSXi eval" in out.read_text()


@pytest.mark.parametrize("redact", [False, True])
def test_cli_report_command_needs_no_credentials(tmp_path, monkeypatch, redact):
    monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
    monkeypatch.delenv("GOODDATA_HOST", raising=False)
    src = tmp_path / "results.json"
    src.write_bytes(orjson.dumps(_doc("gpt-5", True)))
    out = tmp_path / "report.html"

    argv = ["report", str(src), "-o", str(out)] + (["--redact"] if redact else [])
    assert main(argv) == 0
    assert out.exists()


_TRACES = {"n": 4, "mean": 2.5, "min": 1.0, "p50": 2.5, "p70": 3.1, "p90": 3.7, "p99": 3.97, "max": 4.0}
_RUNS = {"n": 2, "mean": 20.0, "min": 10.0, "p50": 20.0, "p70": 24.0, "p90": 28.0, "p99": 29.8, "max": 30.0}
_BY_MODE = {
    "single_shot": {"total": 3, "passed": 2, "traces_s": _TRACES},
    "multi_turn": {"total": 1, "passed": 1, "traces_s": _TRACES, "runs_s": _RUNS},
}


def _doc_with_modes(model: str) -> dict:
    doc = _doc(model, True)
    doc["runs"][model]["summary"]["by_mode"] = _BY_MODE
    doc["runs"][model]["items"]["item-1"].update({"mode": "single_shot", "trace_latencies_s": [1.0, 2.0]})
    doc["comparison"][model]["by_mode"] = _BY_MODE
    return doc


def test_html_carries_the_mode_split_it_was_built_from():
    data = _embedded(build_html(_doc_with_modes("gpt-5")))

    assert data["runs"]["gpt-5"]["summary"]["by_mode"] == _BY_MODE
    assert data["comparison"]["gpt-5"]["by_mode"] == _BY_MODE
    item = data["runs"]["gpt-5"]["items"]["item-1"]
    assert (item["mode"], item["trace_latencies_s"]) == ("single_shot", [1.0, 2.0])


def test_redact_keeps_the_mode_split_and_latency():
    """Latency and the section an item falls in are facts about the run, not about our
    infrastructure -- the same line redaction already draws for per-item latency."""
    data = _embedded(build_html(_doc_with_modes("gpt-5"), redact=True))

    assert data["runs"]["Model A"]["summary"]["by_mode"] == _BY_MODE
    assert data["comparison"]["Model A"]["by_mode"] == _BY_MODE
    assert data["runs"]["Model A"]["items"]["item-1"]["trace_latencies_s"] == [1.0, 2.0]


def test_the_page_has_single_question_and_conversation_sections_read_from_the_report():
    """The report is a view over the JSON: the page names the sections and populations and reads
    the figures from `by_mode`. It holds no percentile arithmetic that could disagree with the
    console or the JSON."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "by_mode" in html
    for text in (
        "Single-question tests · response time",
        "Conversation tests · response time",
        "Per response",
        "Per conversation",
    ):
        assert text in html
    for label in ("Median", "P70", "P90", "P99"):
        assert label in html
    # The table renderers only lay out figures they are handed; the one place that computes any is `recompute`.
    renderers = html.split("// ---------- latency by mode")[1].split("function renderLatency")[0]
    assert "sort(" not in renderers
    assert "percentile(" not in renderers


def test_the_item_table_names_what_each_latency_column_measures():
    """One unlabelled "Latency" column mixed a whole-run average with the per-trace figures above it. The
    table now carries both populations under their own names, read from the item's recorded samples."""
    html = build_html(_doc_with_modes("gpt-5"))

    for text in (
        "Response time",
        "Time per attempt",
        "trace_latencies_s",
        "run_latencies_s",
        "'lt:' + l",
        "'lr:' + l",
    ):
        assert text in html
    assert "['latency', 'Latency']" not in html


def test_the_filters_sit_above_the_dashboard_and_drive_every_table():
    html = build_html(_doc_with_modes("gpt-5"))

    bar = html.index('id="filterbar"')
    for section in ('id="summary"', 'id="outcomes"', 'id="latency"', 'id="items"'):
        assert bar < html.index(section), f"the filter bar must come before {section}"
    # One render path feeds the result cards, the outcome table, the latency tables and the item table.
    render = html.split("function render() {")[1].split("function renderItems")[0]
    for call in ("renderSummary()", "renderOutcomes()", "renderLatency()", "renderItems()"):
        assert call in render


def test_a_filtered_view_recomputes_and_an_unfiltered_one_reads_the_report():
    """Unfiltered, the page shows the report's own figures so it cannot disagree with the console or the
    JSON; only a narrowed selection is recomputed, from the selected items' records."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "filtered ? recompute(l, ids) : reported(l)" in html
    assert "function recompute(label, ids)" in html
    assert "function reported(label)" in html


def test_an_item_is_judged_by_the_gate_verdict_not_pass_at_k_alone():
    """Under --gate power an item that passed some runs has pass_at_k True and gate_passed False; the
    report's counts follow the gate, so the page's status chips and recomputed counts must too."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "item.gate_passed ?? item.pass_at_k" in html
    assert "item.pass_at_k ? 'pass'" not in html


def test_kind_status_and_run_are_multi_selects_in_both_tiers():
    html = build_html(_doc_with_modes("gpt-5"))

    for facet in ("kind", "status", "runs"):
        assert f"multi('{facet}'" in html
    assert 'type="checkbox"' in html
    # The old single-value selects and the single "focused run" are gone.
    for old in ('<select id="kind"', '<select id="status"', '<select id="focus"', "$('#kind').value"):
        assert old not in html
    # The top bar and the Items section are built from the same controls.
    assert "controlsHtml('top'" in html
    assert "controlsHtml('items'" in html


def test_search_and_expression_belong_to_the_item_section_only():
    html = build_html(_doc_with_modes("gpt-5"))

    start = html.index('id="items-section"')
    for control in ('id="q"', 'id="expr"'):
        assert html.count(control) == 1
        assert html.index(control) > start, f"{control} must live in the Items section"
    # The dashboard's render path never reads the table's own filters.
    render = html.split("function render() {")[1].split("function renderItems")[0]
    for table_only in ("$('#q')", "$('#expr')", "I.kind", "I.status", "I.runs", "I.mode"):
        assert table_only not in render


def test_the_tables_filters_combine_with_the_top_ones_without_widening_them():
    """The table starts from the rows the top filters allow (`dashRows`) and only narrows them."""
    html = build_html(_doc_with_modes("gpt-5"))

    items = html.split("function itemRows(runList) {")[1].split("function activeSortKey")[0]
    assert "dashRows.filter(" in items
    assert "rows.filter(" not in items


def test_the_latency_tables_show_the_median_p70_p90_and_p99():
    """The tables carry the median, P70, P90 and P99 -- the same four figures the chart draws -- and no longer the
    fastest and slowest single response; P99 is the tail. The average and trimmed average stay in the JSON and the
    console. A filtered view still recomputes the full distribution, so its `by_mode` has the shape the report's own
    would."""
    html = build_html(_doc_with_modes("gpt-5"))

    table = html.split("function latencyTable(")[1].split("function modeSection")[0]
    # A run is the first three columns of the table -- when it ran, what it is called, the model -- then the four figures.
    assert "const heads = [...RUN_HEADS, ...LAT_SERIES.map((s) => [s.name, HEAD_HELP[s.name]])]" in table
    assert (
        "${runDateCell(l)}<td>${esc(givenNameOf(l))}${isLatest ? LATEST_PILL : ''}${flag}</td>${modelCell(l)}" in table
    )
    assert "const KEYS = LAT_SERIES.map((s) => s.key)" in table
    assert "'Fastest'" not in table and "'Slowest'" not in table
    chart = html.split("const LAT_SERIES = [")[1].split("function latencyChart")[0]
    assert "key: 'p50', name: 'Median'" in chart
    assert "key: 'p70', name: 'P70'" in chart
    assert "key: 'p90', name: 'P90'" in chart
    assert "key: 'p99', name: 'P99'" in chart
    # The run with no timings gets one dash per figure, however many columns there are.
    assert "dash.repeat(KEYS.length)" in table
    assert "trimmed_mean:" in html.split("function latencyStats(samples)")[1].split("function qualityOf")[0]


def test_each_latency_table_is_preceded_by_a_line_chart_of_the_same_four_figures():
    """The chart sits between the section's text and its table, draws one line per figure from the same `by_mode`
    numbers the table prints, and needs two runs with timings to have a line to draw."""
    html = build_html(_doc_with_modes("gpt-5"))

    table = html.split("function latencyTable(")[1].split("function modeSection")[0]
    assert "latencyChart({ mode, field, sample }) +" in table
    chart = html.split("function latencyChart(")[1].split("// Hover or focus on a run")[0]
    # Same source as the table, no arithmetic of its own.
    assert "modeOf(l, mode)" in chart and "[field]" in chart
    assert "sort(" not in chart and "percentile(" not in chart
    # Two runs with timings are needed for a line; fewer and the table says it all.
    assert "pts.filter((p) => p.st).length < 2) return ''" in chart
    # Always from zero, one polyline per figure, a legend, and the table as the text alternative.
    assert "const x = (i) =>" in chart and "y = (v) => M.t + innerH * (1 - v / yMax)" in chart
    assert "<polyline" in chart and "lclegend" in chart
    assert "The table below lists every figure." in chart
    # Drawn at the row's own width and redrawn when it changes, so the chart spans the row without stretching its text.
    assert "const W = latW" in chart
    assert "max-width" not in html.split(".latchart {")[1].split("}")[0]
    assert "new ResizeObserver" in html.split("function renderLatency")[1].split("// ---------- outcomes")[0]
    # Hover and keyboard focus show every figure of that run.
    assert 'tabindex="0"' in chart and "lctip" in chart
    assert "focusin" in html.split("function latHover")[1].split("function latencyTable")[0]


def test_the_latency_tables_mark_the_quickest_and_slowest_run_by_icon_as_well_as_colour():
    html = build_html(_doc_with_modes("gpt-5"))

    table = html.split("function latencyTable(")[1].split("function modeSection")[0]
    assert "quickest of the runs shown" in table
    assert "slowest of the runs shown" in table
    # A chevron carries the meaning too (down = least time, up = most), so the colour is never the only signal.
    assert "best: CHEVRON('down'), worst: CHEVRON('up')" in table
    assert "latestpill" in html


def test_html_uses_the_goodata_tokens_and_loads_no_web_font():
    html = build_html(_doc("gpt-5", True))

    for token in ("#14b2e2", "#dafe85", "#464e56", "#dde4eb", "#f5f8fa"):
        assert token in html, f"design token {token} missing"
    # The brand faces are named, never loaded: a viewer without them gets the system sans.
    assert "--font: Inter," in html
    assert '--font-display: "Funnel Display"' in html
    # Self-contained: a web font, import or remote stylesheet would break file:// and offline use.
    assert "@font-face" not in html
    assert "@import" not in html
    assert "url(" not in html


def test_the_masthead_names_the_report_and_an_explicit_title_wins():
    html = build_html(_doc("gpt-5", True), title="H200 regression check")

    assert "GoodData.AI</span> · Evaluation report" in html
    # --title wins; without one the page builds "Run history: <model> on <workspace>" from the runs.
    assert "DATA.title !== 'gd-eval report'" in html
    for kind in ("Run history", "Run comparison", "Run results"):
        assert kind in html
    assert _embedded(html)["title"] == "H200 regression check"


def test_results_open_on_three_headline_cards_that_say_where_the_value_came_from():
    """The report opens on pass rate, quality and time for the latest run. Each carries one change line in words
    ("down from 86% on Sep 28") rather than a signed number, coloured by whether that direction is good, with a
    chevron and screen-reader text so the colour is never the only signal."""
    html = build_html(_doc_with_modes("gpt-5"))

    cards = html.split("function renderSummary()")[1].split("function sparkHover")[0]
    for metric in ("Test cases passed", "Average quality score", "Median time per attempt"):
        assert metric in cards
    kpi = html.split("function kpiCard(")[1].split("function renderSummary")[0]
    for text in ("'best' : 'worst'", "'Better: ' : 'Worse: '", "CHEVRON(", "same as ", "from ${fmt(b.v)}"):
        assert text in kpi
    # The old results table, its picker and the separate comparison table are gone.
    for gone in ('id="comparison"', 'id="trend"', "renderComparison", "renderTrend", "cmp-a", 'class="results"'):
        assert gone not in html


def test_a_sparkline_appears_from_three_runs_and_a_click_picks_the_run_to_compare_with():
    """Two runs need no history chart; from three each card carries a sparkline of every run. Clicking a point
    compares the latest run with that one. A pick that a filter removed, or that became the latest run, is ignored
    rather than compared with itself."""
    html = build_html(_doc_with_modes("gpt-5"))

    kpi = html.split("function kpiCard(")[1].split("function renderSummary")[0]
    assert "pts.length >= 3" in kpi
    assert "function sparkPick(run)" in html
    base = html.split("function compareBase()")[1].split("// Median wall-clock")[0]
    assert "cmpPick !== last" in base
    assert "runsShown.includes(cmpPick)" in base


def test_a_key_under_the_cards_explains_the_dots_and_that_the_white_one_can_be_moved():
    """The white dot is the run the change lines compare the latest run with; it starts on the previous run and a
    click on another dot moves it. Nothing on the sparkline says so, so a key sits under the cards. It describes
    the dots the page draws, so it appears only when a sparkline does."""
    html = build_html(_doc_with_modes("gpt-5"))

    legend = html.split("function sparkLegend()")[1].split("function renderSummary")[0]
    for key in ("dotkey latest", "dotkey base", "dotkey other"):
        assert key in legend
    assert "the white dot, which starts on the previous run" in legend
    assert "Click any other dot to move the comparison to that run." in legend
    # The swatches carry no text of their own, so they are hidden from screen readers; the words beside them stay.
    assert legend.count('aria-hidden="true"') == 3
    # It follows the cards, and only when one of them drew a sparkline.
    summary = html.split("function renderSummary()")[1].split("function sparkHover")[0]
    assert "cards.includes('class=\"spark\"') ? sparkLegend() : ''" in summary
    assert summary.index("'</div>' + (cards.includes") > summary.index("<h2>Results</h2>")
    # The swatches match the chart: the white dot is the panel colour with a dark ring, as `circle.pt.picked` is.
    assert (
        ".dotkey.base { width: 8px; height: 8px; background: var(--panel); border: 1.5px solid var(--ink-strong); }"
        in html
    )
    assert (
        ".kpi .spark circle.pt.picked:not(.latest) { fill: var(--panel); stroke: var(--ink-strong); stroke-width: 1.5; }"
        in html
    )


def test_seconds_drop_a_redundant_decimal():
    html = build_html(_doc_with_modes("gpt-5"))

    assert r"v.toFixed(1).replace(/\.0$/, '')" in html


def test_the_item_table_says_what_changed_since_the_previous_run():
    html = build_html(_doc_with_modes("gpt-5"))

    assert "Since previous run" in html
    for change in ("Regressed", "Fixed", "Flaky", "New", "Removed", "Still failing", "Still passing"):
        assert change in html.split("const CHANGE_ORDER")[1].split("function sortVal")[0]
    # With several runs the table opens on the regressions; one run has nothing to compare, so it opens on status.
    assert "LABELS.length > 1 ? 'chg' : 's:' + LABELS[0]" in html
    # Newest first: the latest result, then what changed since the previous run, then earlier runs going back.
    assert "runList.slice(0, -1).reverse()" in html


def _run_page_js(html: str, definitions: list[str], expression: str):
    """Evaluate `expression` in Node against functions lifted verbatim out of the page's script, so the
    rules are exercised as written rather than asserted as text. There is no JS test runner in this package."""
    parts = []
    for name in definitions:
        found = re.search(
            rf"^(?:const {name} = [^\n]*;|const {name} = \[\n.*?^\];|const {name} = \[\[.*?\]\];|function {name}\(.*?^\}})$",
            html,
            re.M | re.S,
        )
        assert found, f"{name} not found in the page"
        parts.append(found.group(0))
    script = "\n".join(parts) + f"\nconsole.log(JSON.stringify({expression}));"
    done = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(done.stdout)


_needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="the page's script is run in Node")
_PAGE_STATUS = ["passedOf", "statusOf"]


_TIME_CARD_PAGE = "(() => {{ globalThis.runsShown = ['r']; globalThis.dashRows = {rows}; return medTimeHelp(); }})()"


@_needs_node
def test_the_time_card_says_which_formats_it_pools_and_why_it_differs_from_the_tables() -> None:
    """The card is the median of whole attempts over every format the page covers, so beside the per-format
    response tables it reads as a different number. Its tooltip says what it covers."""
    html = build_html(_doc_with_modes("gpt-5"))
    both = "[{mode: 'single_shot', per: {r: {run_latencies_s: [1]}}}, {mode: 'multi_turn', per: {r: {run_latencies_s: [2]}}}]"
    single = "[{mode: 'single_shot', per: {r: {run_latencies_s: [1]}}}, {mode: 'multi_turn', per: {}}]"

    pooled = _run_page_js(html, ["MODES", "MODE_NAME", "medTimeHelp"], _TIME_CARD_PAGE.format(rows=both))
    one_format = _run_page_js(html, ["MODES", "MODE_NAME", "medTimeHelp"], _TIME_CARD_PAGE.format(rows=single))

    assert "single-question and conversation test cases together" in pooled
    assert "matches neither latency table" in pooled
    assert "single-question test cases." in one_format
    assert "neither" not in one_format
    # Both say what an attempt is, so a reader can see why it runs longer than a response time.
    assert "grading included" in pooled and "grading included" in one_format
    # Only the time card carries the tooltip.
    cards = html.split("function renderSummary()")[1].split("function sparkHover")[0]
    assert cards.count("help:") == 1 and "help: medTimeHelp()" in cards


@_needs_node
def test_the_pass_rate_card_leaves_skipped_test_cases_out_like_the_console():
    """The console divides by the evaluated test cases, so the page must or the two disagree: 10 passed of 14 with
    2 skipped is 83% in the console, not 71%."""
    html = build_html(_doc_with_modes("gpt-5"))

    rates = _run_page_js(
        html,
        ["passRateOf"],
        "[passRateOf({total: 14, skipped: 2, passed: 10}), passRateOf({total: 2, skipped: 2, passed: 0}), "
        "passRateOf({total: 0, skipped: 0, passed: 0})]",
    )

    assert rates == [pytest.approx(10 / 12), None, None]
    # Both the reported and the recomputed figures carry `skipped`, which is what the card divides by.
    assert "get: (l) => passRateOf(figures[l])" in html
    assert "passed / items.length" not in html


def test_the_outcomes_section_sits_between_the_result_cards_and_latency_and_reads_the_same_figures():
    """The section answers "how did each test case end" the way the latency tables answer "how long": one row per
    run, newest first, latest in lime. It reads `figures` (the report's own summary, or a recomputation when
    filtered) and takes its pass rate from `passRateOf`, the function behind the first card."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert html.index('id="summary"') < html.index('id="outcomes"') < html.index('id="latency"')
    section = html.split("function outcomesTable()")[1].split("function renderOutcomes")[0]
    assert "passRateOf(figures[l])" in section
    assert ".reverse().join('')" in section  # newest run first, like the latency tables
    assert "LATEST_PILL" in section
    for outcome in ("Passed", "Failed", "Could not be graded", "Skipped"):
        assert f"'{outcome}'" in html.split("const OUTCOMES = [")[1].split("function outcomesTable")[0]
    assert "'Pass rate'" in section
    # The table lays out figures it is handed; nothing here counts items or sorts samples.
    assert "sort(" not in section
    assert "items.filter(" not in section


def test_the_outcome_names_match_the_result_filter():
    """The four outcomes are the four values of the Result filter, in the same words, so a reader can go from a
    count in the table to the test cases behind it."""
    html = build_html(_doc_with_modes("gpt-5"))

    filter_text = {
        t
        for _, t in re.findall(
            r"\{ value: '(\w+)', text: '([^']+)' \}", html.split("const STATUS_OPTIONS")[1].split("];")[0]
        )
    }
    outcome_names = set(re.findall(r"^  \['(?:passed|failed|errored|skipped)', '([^']+)'", html, re.M))
    assert outcome_names == {"Passed", "Failed", "Could not be graded", "Skipped"}
    assert outcome_names == filter_text


@_needs_node
def test_a_report_without_a_failed_count_gets_it_from_what_the_other_three_leave():
    """`failed` was added to the summary after the first reports were written; an older file still shows four
    outcomes that add up to its total."""
    html = build_html(_doc_with_modes("gpt-5"))

    def reported(summary, comparison):
        data = {"comparison": {"r": comparison}, "runs": {"r": {"summary": summary}}}
        return _run_page_js(html, ["reported"], f"(globalThis.DATA = {json.dumps(data)}, reported('r'))")

    # Written by gd-eval today: the report's own count wins.
    current = reported({"total": 10, "passed": 6, "failed": 2, "errored": 1, "skipped": 1}, {})
    assert (current["passed"], current["failed"], current["errored"], current["skipped"]) == (6, 2, 1, 1)
    # Written before `failed` existed: it is what remains.
    older = reported({"total": 10, "passed": 6, "errored": 1, "skipped": 1}, {})
    assert older["failed"] == 2
    # Never negative, even if the other counts overlap (an item that passed and then errored is in both).
    assert reported({"total": 4, "passed": 3, "errored": 2}, {})["failed"] == 0


@_needs_node
def test_a_filtered_view_counts_failed_as_graded_and_not_passed():
    """Under a filter the outcomes are recounted from the selected items, by the JSON's own definition of `failed`:
    not passed, not skipped, no error. The four then add up to the selection."""
    html = build_html(_doc_with_modes("gpt-5"))
    items = {
        "a": {"gate_passed": True},
        "b": {"gate_passed": False},
        # Under --gate power: some attempts passed (pass_at_k) but the gate did not, so it failed.
        "c": {"pass_at_k": True, "gate_passed": False},
        "d": {"gate_passed": False, "error": "JudgeResponseError: no run of this item could be graded"},
        "e": {"skipped": True},
    }

    figures = _run_page_js(
        html,
        ["passedOf", "mean", "r3", "percentile", "latencyStats", "qualityOf", "MODES", "recompute"],
        f"(globalThis.DATA = {{runs: {{r: {{items: {json.dumps(items)}}}}}}}, recompute('r', {json.dumps(list(items))}))",
    )

    assert {k: figures[k] for k in ("total", "passed", "failed", "errored", "skipped")} == {
        "total": 5,
        "passed": 1,
        "failed": 2,
        "errored": 1,
        "skipped": 1,
    }


@_needs_node
def test_the_outcome_table_lists_the_runs_newest_first_with_a_pass_rate_that_leaves_skipped_out():
    html = build_html(_doc_with_modes("gpt-5"))
    figures = {
        "Sep 28": {"total": 20, "passed": 14, "failed": 4, "errored": 1, "skipped": 1},
        "Oct 5": {"total": 20, "passed": 16, "failed": 3, "errored": 1, "skipped": 0},
        "Oct 12": {"total": 20, "passed": 15, "failed": 4, "errored": 0, "skipped": 1},
    }
    stubs = (
        "globalThis.figures = " + json.dumps(figures) + ", globalThis.runsShown = " + json.dumps(list(figures)) + ", "
        "globalThis.roleOf = (l) => l, globalThis.esc = (s) => String(s), globalThis.suiteChange = () => '', "
        "globalThis.caution = (h) => '[!' + h + ']', globalThis.CHEVRON = (d) => '<' + d + '>', "
        "globalThis.runDateCell = (l) => '<td>date ' + l + '</td>', globalThis.givenNameOf = (l) => 'name ' + l, "
        "globalThis.modelCell = (l) => '<td>model ' + l + '</td>', globalThis.LATEST_PILL = ' LATEST'"
    )
    page = _run_page_js(html, ["passRateOf", "OUTCOMES", "RUN_HEADS", "outcomesTable"], f"({stubs}, outcomesTable())")

    # Newest first.
    assert page.index("Oct 12") < page.index("Oct 5") < page.index("Sep 28")
    rows = {}
    for m in re.finditer(r"<tr[^>]*><td>date (.*?)</td>(.*?)</tr>", page):
        rows[m.group(1)] = m.group(2)
    # The run name, the model, four outcomes and the pass rate (the run date is captured apart).
    assert rows["Oct 12"].count("<td") == 7
    assert "name Oct 12" in rows["Oct 12"] and "model Oct 12" in rows["Oct 12"]
    # The run is identified by three columns, when it ran, what it is called and the model, in place of a single "Run".
    assert page.index(">Run date</th>") < page.index(">Run name</th>") < page.index(">Model</th>")
    assert page.index(">Model</th>") < page.index(">Passed</th>")
    assert ">Run</th>" not in page
    assert "LATEST" in rows["Oct 12"] and "LATEST" not in rows["Oct 5"]
    # 15 of the 19 evaluated is 79%, not 15 of 20 (75%): the skipped one never ran.
    assert "79%" in rows["Oct 12"]
    assert "80%" in rows["Oct 5"]  # 16 of 20
    assert "74%" in rows["Sep 28"]  # 14 of 19
    # The best run is marked up, the worst down, and the key says so.
    assert 'class="ext best"><up>80%' in rows["Oct 5"]
    assert 'class="ext worst"><down>74%' in rows["Sep 28"]
    assert "highest pass rate" in page and "lowest pass rate" in page
    # A run over a different number of evaluated test cases than the one before carries a caution; the first run has
    # nothing before it.
    assert "[!" in rows["Oct 5"] and "[!" in rows["Oct 12"]
    assert "[!" not in rows["Sep 28"]


@_needs_node
def test_the_outcome_table_marks_nothing_when_every_run_reads_the_same():
    html = build_html(_doc_with_modes("gpt-5"))
    same = {"total": 10, "passed": 8, "failed": 2, "errored": 0, "skipped": 0}
    stubs = (
        f"globalThis.figures = {json.dumps({'a': same, 'b': same})}, globalThis.runsShown = ['a', 'b'], "
        "globalThis.roleOf = (l) => l, globalThis.esc = (s) => String(s), globalThis.suiteChange = () => '', "
        "globalThis.caution = (h) => '[!' + h + ']', globalThis.CHEVRON = (d) => '<' + d + '>', "
        "globalThis.runDateCell = (l) => '<td>date ' + l + '</td>', globalThis.givenNameOf = (l) => 'name ' + l, "
        "globalThis.modelCell = (l) => '<td>model ' + l + '</td>', globalThis.LATEST_PILL = ' LATEST'"
    )

    page = _run_page_js(html, ["passRateOf", "OUTCOMES", "RUN_HEADS", "outcomesTable"], f"({stubs}, outcomesTable())")

    assert "80%" in page
    assert 'class="ext' not in page
    assert "[!" not in page  # same number of test cases: nothing to caution about


@_needs_node
def test_the_run_date_cell_says_when_the_run_started_and_falls_back_to_the_date_its_file_is_named_for(monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    html = build_html(_doc_with_modes("gpt-5"))
    runs = {
        "a": {"summary": {"started_at": "2026-10-14T14:30:21.412873+00:00"}},
        "2026-09-28": {"summary": {}},  # written before started_at existed: the file is named for its day
        "notes": {"summary": {"started_at": None}},  # a report that was never timed
    }
    definitions = ["MONTHS", "esc", "startedAt", "runStamp", "humanDate", "humanDateTime", "runDateText", "runDateCell"]

    cells = _run_page_js(
        html,
        definitions,
        f"(globalThis.DATA = {json.dumps({'runs': runs})}, {json.dumps(list(runs))}.map(runDateCell))",
    )

    # The day and the time, in the viewer's time zone, with the report's own UTC stamp on hover.
    assert re.fullmatch(r'<td title="2026-10-14T14:30:21.412873\+00:00">Oct 14(, 2026)?, 14:30</td>', cells[0])
    # Only the day is known for an older report, so no time is invented.
    assert re.fullmatch(r"<td>Sep 28(, 2026)?</td>", cells[1])
    assert cells[2] == "<td>–</td>"


@_needs_node
def test_the_run_name_is_the_name_the_run_was_given_not_a_styled_date():
    html = build_html(_doc_with_modes("gpt-5"))

    names = _run_page_js(
        html,
        ["sourceOf", "givenNameOf"],
        "(globalThis.MODEL_LABEL = {'2026-09-28 · p/m': 'm'}, globalThis.MULTI_MODEL = false, "
        "[givenNameOf('nightly-baseline'), givenNameOf('2026-09-28 · p/m'), "
        "(globalThis.MULTI_MODEL = true, givenNameOf('2026-09-28 · p/m'))])",
    )

    # roleOf would show a date-named run as "Sep 28"; the name column keeps what the run was called. The model has a
    # column of its own beside it, so a report holding several models does not repeat it in the name.
    assert names == ["nightly-baseline", "2026-09-28", "2026-09-28"]


@_needs_node
def test_a_run_column_heading_stacks_the_run_date_over_the_run_name_and_leaves_the_model_out(monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    html = build_html(_doc_with_modes("gpt-5"))
    label = "2026-10-14 · p/m"
    definitions = [
        *["MONTHS", "esc", "startedAt", "runStamp", "humanDate", "humanDateTime", "runDateText"],
        *["sourceOf", "givenNameOf", "runHeadHtml"],
    ]
    stubs = (
        f"globalThis.DATA = {json.dumps({'runs': {label: {'summary': {'started_at': '2026-10-14T14:30:21Z'}}}})}, "
        "globalThis.MODEL_LABEL = {'2026-10-14 · p/m': 'm'}, globalThis.roleOf = (l) => 'role ' + l"
    )

    heads = _run_page_js(
        html,
        definitions,
        f"({stubs}, [(globalThis.VIEW = 'date', runHeadHtml({json.dumps(label)})), "
        f"(globalThis.VIEW = 'model', runHeadHtml({json.dumps(label)}))])",
    )

    # By date: the run date, then the run name, each in a block of its own so they sit on separate lines.
    assert re.fullmatch(
        r'<span class="runhead" title="2026-10-14 · p/m"><span>Oct 14(, 2026)?, 14:30</span><span>2026-10-14</span></span>',
        heads[0],
    )
    # By model the columns are the models themselves, so they keep the model's name.
    assert heads[1] == "role 2026-10-14 · p/m"
    # The test case table heads every run column with it, the latest run first.
    assert "html: runHeadHtml(runList[runList.length - 1]) + LATEST_PILL" in html
    assert "html: runHeadHtml(l)" in html
    assert ".runhead > span { display: block; white-space: nowrap; }" in html


def test_the_model_outcomes_table_adds_the_median_latency_and_lists_what_each_term_means():
    html = build_html(_doc_with_modes("gpt-5"))

    section = html.split("function modelOutcomesHtml()")[1].split("function ")[0]
    assert "['Median latency', MEDIAN_HELP]" in section
    assert "medTimeOf(l)" in section
    # One line per term rather than one run-on sentence.
    assert '<ul class="blurb legend">' in section
    for term in ("passed", "failed", "could not be graded", "skipped", "Median latency"):
        assert f"<b>{term}</b>" in section


_ITEM_RESULT = {"pass": {"gate_passed": True}, "fail": {"gate_passed": False}, "skip": {"skipped": True}}


def _changes(html: str, runs: dict[str, str | None]) -> str:
    """The change label for a test case whose result in each run is pass, fail, skip or None (not in that run)."""
    row = {"per": {label: _ITEM_RESULT[result] for label, result in runs.items() if result is not None}}
    return _run_page_js(html, [*_PAGE_STATUS, "changeOf"], f"changeOf({json.dumps(row)}, {json.dumps(list(runs))})")


@_needs_node
@pytest.mark.parametrize(
    ("runs", "label"),
    [
        # Skipped in the latest run: the earlier runs alone would call this Regressed, beside a SKIP cell.
        ({"a": "pass", "b": "fail", "c": "skip"}, ""),
        ({"a": "fail", "b": "pass", "c": "skip"}, ""),
        ({"a": "pass", "b": "pass", "c": "skip"}, ""),
        # Skipped in the latest run and in no earlier one: not New, the SKIP cell is all there is to say.
        ({"a": None, "b": "skip"}, ""),
        ({"a": None, "b": None, "c": "skip"}, ""),
        # A skip in the middle is looked through: the latest run still decides the label.
        ({"a": "pass", "b": "skip", "c": "fail"}, "Regressed"),
        ({"a": "pass", "b": "fail"}, "Regressed"),
        ({"a": "fail", "b": "pass"}, "Fixed"),
        ({"a": "pass", "b": "pass"}, "Still passing"),
        ({"a": "fail", "b": "fail"}, "Still failing"),
        ({"a": "fail", "b": "pass", "c": "fail", "d": "pass"}, "Flaky"),
        # Absent from the previous run but present before it: back, not new.
        ({"a": "fail", "b": None, "c": "pass"}, "Fixed"),
        ({"a": "pass", "b": None, "c": "fail"}, "Regressed"),
        ({"a": "pass", "b": None, "c": "pass"}, "Still passing"),
        ({"a": None, "b": "pass"}, "New"),
        ({"a": None, "b": None, "c": "fail"}, "New"),
        ({"a": "pass", "b": None}, "Removed"),
        ({"a": "pass", "b": "pass", "c": None}, "Removed"),
        # One run has nothing to compare with.
        ({"a": "pass"}, ""),
    ],
)
def test_a_change_label_describes_the_latest_run_against_the_whole_history(runs, label):
    assert _changes(build_html(_doc_with_modes("gpt-5")), runs) == label


def test_the_run_setup_tooltip_names_what_is_the_same_and_what_differs():
    """Results from different setups are not directly comparable, so the page says which setup facts changed
    between runs instead of leaving the reader to infer it from a number."""
    html = build_html(_doc_with_modes("gpt-5"))

    for text in ("Run setup", "Same in every run", "Differs between runs", "Attempts per test case", "Pass rule"):
        assert text in html
    # A field the report does not carry (a redacted workspace, say) is not listed as an empty row.
    assert "x.vals.some((v) => v !== '\\u2013')" in html


def test_a_filter_popup_stages_its_changes_until_apply():
    """The kind, status and run filters follow GoodData's attribute filter: search, All, values with an Only
    shortcut and a count, then Cancel or Apply. Nothing takes effect until Apply."""
    html = build_html(_doc_with_modes("gpt-5"))

    popup = html.split("function makeMulti(")[1].split("const T = {")[0]
    for part in ('class="search"', 'class="allrow"', 'class="only"', 'class="cancel"', 'class="apply"'):
        assert part in popup
    assert "FILTER_TITLE" in popup
    # The selection moves only in `apply`; the checkboxes edit a draft.
    assert popup.count("m.sel.add(") == 1


def test_the_expression_filter_is_folded_away_and_the_page_has_a_print_stylesheet():
    html = build_html(_doc_with_modes("gpt-5"))

    adv = html.index('<details class="adv">')
    assert adv < html.index('id="expr"') < html.index("</details>", adv)
    assert "@media print" in html
    print_css = html.split("@media print")[1].split("</style>")[0]
    for hidden in ("#filterbar", "#drawer"):
        assert hidden in print_css


def test_the_template_carries_no_sample_data():
    """The design was drafted against illustrative data. None of its model names, workspaces or flags may
    survive into the template, or every report (a redacted one included) would carry them."""
    html = build_html(_doc("some-model", True))

    for sample in ("gpt-5", "Foundry", "ecommerce", "illustrative", "ILLUSTRATIVE"):
        assert sample not in html


def test_a_redacted_report_leaves_no_empty_setup_rows():
    html = build_html(_doc("gpt-5", True), redact=True)

    # Workspace and provider are blanked by redaction; the page drops a row it has no value for.
    assert "x.vals.some((v) => v !== '\\u2013')" in html
    assert _embedded(html)["runs"]["Model A"]["workspace_id"] == ""


def test_building_the_html_does_not_invent_a_mode_split_for_an_older_report():
    """Files written before gd-eval split latency by mode carry no `by_mode`. The page says so;
    nothing here backfills a figure the run never measured."""
    data = _embedded(build_html(_doc("gpt-5", True)))

    assert "by_mode" not in data["runs"]["gpt-5"]["summary"]
    assert "by_mode" not in data["comparison"]["gpt-5"]


# --- View by: model or date -------------------------------------------------------------------------------------


def test_view_by_sits_above_the_filters_with_a_choice_of_date_or_model():
    html = build_html(_doc_with_modes("gpt-5"))

    assert html.index('id="filterbar"') < html.index('id="viewby"') < html.index('aria-label="Page filters"')
    select = html.split('<select id="viewby">')[1].split("</select>")[0]
    assert select.index('<option value="date">Date</option>') < select.index('<option value="model">Model</option>')
    assert "By date" not in select and "By model" not in select
    assert 'for="viewby">View by</label>' in html
    # One run has nothing to switch between, so the row hides itself rather than offering two identical views.
    assert "$('#viewrow').hidden = ALL_LABELS.length < 2" in html


def test_the_page_always_opens_by_date():
    """Even a report that compares several models, each seen once, opens on the Date view; Model is one choice away."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "\nsetView('date');\n" in html
    assert "defaultView" not in html


_RUN_ORDER = ["startedAt", "runStamp", "byTime"]


@_needs_node
def test_runs_are_ordered_by_their_start_time_not_by_the_order_the_files_were_given_in():
    """The page reads "last run" as "latest", so the order has to come from the clock: files passed newest first, or
    in any order a shell glob gives them, must still draw the oldest on the left of every chart and the latest on top
    of every table."""
    html = build_html(_doc_with_modes("gpt-5"))
    data = {
        "runs": {
            "c · p/m": {"summary": {"started_at": "2026-10-14T14:30:00.412873+00:00"}},
            "a · p/m": {"summary": {"started_at": "2026-10-06T09:15:00Z"}},
            "d · p/m": {"summary": {"started_at": "2026-10-14T14:31:00.007+00:00"}},
            "b · p/m": {"summary": {"started_at": "2026-10-08T11:40:00Z"}},
        }
    }

    order = _run_page_js(html, _RUN_ORDER, f"(globalThis.DATA = {json.dumps(data)}, byTime(Object.keys(DATA.runs)))")

    assert order == ["a · p/m", "b · p/m", "c · p/m", "d · p/m"]


@_needs_node
def test_runs_that_started_together_keep_the_order_they_were_given_in():
    html = build_html(_doc_with_modes("gpt-5"))
    data = {
        "runs": {
            "y": {"summary": {"started_at": "2026-10-14T14:30:00Z"}},
            "x": {"summary": {"started_at": "2026-10-14T14:30:00Z"}},
        }
    }

    order = _run_page_js(html, _RUN_ORDER, f"(globalThis.DATA = {json.dumps(data)}, byTime(Object.keys(DATA.runs)))")

    assert order == ["y", "x"]


@_needs_node
def test_a_run_without_a_start_time_is_placed_by_the_date_its_file_is_named_for():
    """Reports written before `started_at` existed are usually kept as one file per day, named for it."""
    html = build_html(_doc_with_modes("gpt-5"))
    data = {"runs": {"2026-10-12 · p/m": {}, "2026-09-28 · p/m": {}, "2026-10-05": {}}}

    order = _run_page_js(html, _RUN_ORDER, f"(globalThis.DATA = {json.dumps(data)}, byTime(Object.keys(DATA.runs)))")

    assert order == ["2026-09-28 · p/m", "2026-10-05", "2026-10-12 · p/m"]


@_needs_node
def test_a_report_with_an_unplaceable_run_keeps_the_order_it_was_given_in():
    """Sorting only the runs that can be placed would put the others at an arbitrary spot, which reads as a claim."""
    html = build_html(_doc_with_modes("gpt-5"))
    data = {
        "runs": {
            "b · p/m": {"summary": {"started_at": "2026-10-14T14:30:00Z"}},
            "notes.json · p/m": {"summary": {"started_at": None}},  # a report that was never timed
            "a · p/m": {"summary": {"started_at": "2026-10-06T09:15:00Z"}},
        }
    }

    order = _run_page_js(html, _RUN_ORDER, f"(globalThis.DATA = {json.dumps(data)}, byTime(Object.keys(DATA.runs)))")

    assert order == ["b · p/m", "notes.json · p/m", "a · p/m"]


def test_the_page_builds_its_run_list_through_the_timestamp_order():
    html = build_html(_doc_with_modes("gpt-5"))

    assert "const ALL_LABELS = byTime(Object.keys(DATA.runs));" in html


@_needs_node
def test_by_model_compares_each_models_latest_run():
    """The page lists its runs oldest first (by start time), so the last run of a model is its latest. The models
    keep the order they first appear in."""
    html = build_html(_doc_with_modes("gpt-5"))
    keys = {"d1 · a": "m1", "d1 · b": "m2", "d2 · a": "m1", "d2 · b": "m2", "d3 · c": "m3"}

    latest = _run_page_js(
        html, ["latestPerKey"], f"latestPerKey({json.dumps(list(keys))}, (l) => ({json.dumps(keys)})[l])"
    )

    assert latest == ["d2 · a", "d2 · b", "d3 · c"]


@_needs_node
def test_a_model_is_read_from_the_run_not_from_its_file_name():
    html = build_html(_doc_with_modes("gpt-5"))
    data = {
        "runs": {"2026-09-28 · p/m": {"model": "m"}, "m.json · p/m": {"model": "m"}, "x · q/m": {"model": "m"}},
        "comparison": {
            "2026-09-28 · p/m": {"provider_name": "p"},
            "m.json · p/m": {"provider_name": "p"},
            "x · q/m": {"provider_name": "q"},
        },
    }

    keys = _run_page_js(
        html,
        ["modelOfRun", "providerOfRun", "modelKeyOf"],
        f"(globalThis.DATA = {json.dumps(data)}, Object.keys(DATA.runs).map(modelKeyOf))",
    )

    # The same model id behind two providers is two models; the same model on two dates is one.
    assert keys == ["p/m", "p/m", "q/m"]


@_needs_node
def test_models_are_ranked_by_the_consoles_winner_rule():
    """Pass rate, then quality, then the quicker average: the order the console names its winner by."""
    html = build_html(_doc_with_modes("gpt-5"))
    figures = [
        {"n": "slow", "total": 10, "skipped": 0, "passed": 8, "avg_quality_score": 0.9, "avg_latency_s": 9},
        {"n": "best", "total": 10, "skipped": 0, "passed": 9, "avg_quality_score": 0.5, "avg_latency_s": 30},
        {"n": "good-quality", "total": 10, "skipped": 0, "passed": 8, "avg_quality_score": 0.95, "avg_latency_s": 30},
        {"n": "quick", "total": 10, "skipped": 0, "passed": 8, "avg_quality_score": 0.9, "avg_latency_s": 3},
        # A skipped test case never ran, so 8 of 8 evaluated beats 9 of 10.
        {
            "n": "fewer-skipped-out",
            "total": 10,
            "skipped": 2,
            "passed": 8,
            "avg_quality_score": 0.1,
            "avg_latency_s": 99,
        },
    ]

    ranked = _run_page_js(html, ["passRateOf", "byStanding"], f"{json.dumps(figures)}.sort(byStanding).map((f) => f.n)")

    assert ranked == ["fewer-skipped-out", "best", "good-quality", "quick", "slow"]


@_needs_node
@pytest.mark.parametrize(
    ("statuses", "label"),
    [
        (["pass", "pass", "pass"], "All pass"),
        (["fail", "fail"], "All fail"),
        (["pass", "fail", "pass"], "Mixed"),
        # Only graded verdicts count: a skip, an ungraded error or an absent model says nothing about a model.
        (["pass", "skip", "none"], ""),
        (["pass", "err", "pass"], "All pass"),
        (["fail", "err", "pass"], "Mixed"),
        (["pass"], ""),
        ([], ""),
    ],
)
def test_across_models_says_whether_the_models_agree_on_a_test_case(statuses, label):
    html = build_html(_doc_with_modes("gpt-5"))

    assert _run_page_js(html, ["agreementOf"], f"agreementOf({json.dumps(statuses)})") == label


def test_the_test_case_table_opens_on_the_disagreements_when_viewed_by_model():
    html = build_html(_doc_with_modes("gpt-5"))

    assert "AGREE_ORDER = { Mixed: 0" in html
    assert "'Across models'" in html
    # By model the models are peers in ranked order: no "latest run" lead column, no "Since previous run" column.
    assert "(multi && byDate ? [runList[runList.length - 1]] : [])" in html
    assert "(multi && !byDate ? (() => { const a = agreementOf(" in html
    assert "sortKey = LABELS.length < 2 ? 's:' + LABELS[0] : VIEW === 'model' ? 'agree' : 'chg'" in html


@_needs_node
@pytest.mark.parametrize(("top", "step"), [(36.5, 10), (0.8, 0.2), (120, 50), (4.4, 1), (0, 0.2)])
def test_axis_steps_are_round_numbers(top, step):
    html = build_html(_doc_with_modes("gpt-5"))

    assert _run_page_js(html, ["niceStep"], f"niceStep({top}, 5)") == pytest.approx(step)


def test_by_model_has_a_section_for_each_chart_between_outcomes_and_latency():
    html = build_html(_doc_with_modes("gpt-5"))

    order = [html.index(f'id="{s}"') for s in ("outcomes", "tradeoff", "categories", "consistency", "latency")]
    assert order == sorted(order)
    # They start hidden and a layout that has no use for one empties it, so nothing leaves a gap.
    for section in ("tradeoff", "categories", "consistency"):
        assert f'<section id="{section}" hidden></section>' in html
    set_section = html.split("function setSection(")[1].split("function renderModelSections")[0]
    assert "el.hidden = !html" in set_section
    sections = html.split("function renderModelSections() {")[1].split("// ---------- by model: results")[0]
    for call in ("tradeoffHtml()", "categoryHtml()", "consistencyHtml()"):
        assert call in sections
    assert "on ? " in sections and ": ''" in sections  # the date view gets an empty string for each


def test_by_model_opens_on_one_results_table_instead_of_leader_cards():
    html = build_html(_doc_with_modes("gpt-5"))

    # The three leader cards are gone; the model view leaves their section empty (and so hidden) rather than drawing them.
    assert "leaderCard" not in html and "renderModelSummary" not in html
    summary = html.split("function renderSummary()")[1].split("function sparkHover")[0]
    assert "if (VIEW === 'model') return setSection('summary', '')" in summary
    # What the date view calls Outcomes is, by model, the Results section; the date view keeps its own two.
    by_model = html.split("function modelOutcomesHtml()")[1].split("// ---------- by model: quality against speed")[0]
    assert "'<h2>Results</h2>'" in by_model and "Outcomes</h2>" not in by_model
    by_date = html.split("function renderOutcomes()")[1].split("// ---------- per-item latency")[0]
    assert "'<h2>Outcomes</h2>'" in by_date
    assert "'<h2>Results</h2><div class=\"trendgrid\">'" in summary


def test_the_model_charts_read_the_same_figures_as_the_cards_and_tables():
    """Nothing here is a second source of truth: the speed-quality plot plots the pass rate and the median time per
    attempt, the outcome bar is the outcome table's own counts, and the latency bars are the table's own percentiles."""
    html = build_html(_doc_with_modes("gpt-5"))

    tradeoff = html.split("function tradeoffHtml()")[1].split("// Drawn at the section's width")[0]
    assert "x: medTimeOf(l), y: passRateOf(figures[l])" in tradeoff
    # Two models are the least a comparison can use; with fewer there is no plot.
    assert "if (pts.length < 2) return ''" in tradeoff
    # Time runs from zero, so the distances between models are honest.
    assert "const X = (v) => M.l + innerW * (v / xMax)" in tradeoff
    outcomes = html.split("function modelOutcomesHtml()")[1].split("// ---------- by model: quality against speed")[0]
    assert "f.passed" in outcomes and "f.failed" in outcomes and "f.errored" in outcomes
    assert "passRateOf(figures[l])" in outcomes
    latency = html.split("function modelLatencyTable(")[1].split("// First paint")[0]
    assert "modeOf(l, mode)" in latency and "LAT_SERIES" in latency
    # The date view's table hands over to it, and keeps nothing of its own from the model view.
    assert "if (VIEW === 'model') return modelLatencyTable({ mode, field, sample });" in html


def test_the_category_heat_map_leaves_skipped_test_cases_out_and_shows_the_figure_in_every_cell():
    html = build_html(_doc_with_modes("gpt-5"))

    categories = html.split("function categoryHtml()")[1].split("// ---------- by model: consistency")[0]
    assert ".filter((it) => it && !it.skipped)" in categories
    # The shade is never the only signal: the share and the counts are printed in the cell, and the best model in a
    # row is marked with a chevron as well as the text.
    assert 'class="n"' in categories and "CHEVRON('up')" in categories
    # With one category there is nothing to break down.
    assert "if (cats.length < 2) return ''" in categories


def test_the_consistency_chart_needs_a_report_that_recorded_repeated_attempts():
    html = build_html(_doc_with_modes("gpt-5"))

    consistency = html.split("function consistencyHtml()")[1].split("// ---------- by model: response time")[0]
    assert "typeof it.pass_power_k === 'boolean' && (it.runs || 0) > 1" in consistency
    assert "if (!st.some(([, s]) => s.repeated)) return ''" in consistency
    # pass@K and pass^K are the two bars; the count of test cases between them is the number a reader acts on.
    assert "it.pass_at_k" in consistency and "it.pass_power_k === true" in consistency
    assert "Passed only some attempts" in consistency


def test_switching_view_drops_selections_made_against_the_other_layout():
    """A run picked in the date view means nothing in the model view, and the other way round, so the switch clears
    them, closes the drawer (it may show a run that is no longer a column) and draws everything again."""
    html = build_html(_doc_with_modes("gpt-5"))

    switch = html.split("function setView(v) {")[1].split("$('#viewby').addEventListener")[0]
    for step in (
        "T.runs.set(LABELS.map(",
        "T.runs.sig = I.runs.sig = null",
        "cmpPick = null; selected = null; drawerRun = null",
        "$('#drawer').classList.remove('open')",
        "renderMasthead()",
        "render()",
    ):
        assert step in switch
    assert "$('#viewby').addEventListener('input', () => setView($('#viewby').value))" in html
    # The run filter is the model filter by model.
    assert "noun === 'runs' && VIEW === 'model' ? 'Model'" in html


def test_a_report_with_several_models_says_so_where_the_date_view_could_mislead():
    """Two models on two dates read as "Oct 5, Oct 5, Oct 12, Oct 12" by date, with neighbouring runs of different
    models compared as if one changed into the other. The names carry the model and the hint points at Model."""
    html = build_html(_doc_with_modes("gpt-5"))

    assert "MULTI_MODEL && l.includes(' · ')" in html
    assert "use Model to compare them" in html
    # The setup tooltip does not flag the model as a difference when the model is what is being compared.
    assert "compared: VIEW === 'model' && (k === 'Model' || k === 'Provider')" in html
    assert "'Same for every model'" in html and "'Differs between models'" in html


_TIMELINE_FNS = ["esc", "bold", "secs", "CHEVRON", "unwrapJson", "fmt", "timelineHtml", "reasoningHtml"]


def _timeline_item() -> dict:
    return {
        "best_run_latency_s": 12.0,
        "reasoning": [
            "**Plan**\n\nwork out the metric",
            "**Check**\n\nverify the numbers",
            "a paragraph no step points at",
        ],
        "detail": {
            "latency_breakdown": [
                {"seq": 0, "kind": "reasoning", "name": "thinking", "index": 0, "duration_s": 2.0},
                {"seq": 1, "kind": "tool", "name": "search_objects", "index": 0, "duration_s": 3.0},
                {"seq": 2, "kind": "reasoning", "name": "thinking", "index": 1, "duration_s": 1.0},
            ],
            "tool_calls": [
                {"index": 0, "name": "search_objects", "arguments": {"query": "revenue"}, "result": '{"results": []}'}
            ],
        },
    }


@_needs_node
def test_every_timeline_step_opens_in_place_and_starts_shut():
    """Each step carries its own record under its own row, hidden until opened, instead of one shared box below the
    list. The chevron is a real button (keyboard-reachable) that says what it controls and whether that is open."""
    html = build_html(_doc("gpt-5", True))

    out = _run_page_js(html, _TIMELINE_FNS, f"timelineHtml({json.dumps(_timeline_item())})")

    assert out.count('class="chev"') == 3
    assert out.count('aria-expanded="false"') == 3 + 1  # the three steps and the expand-all control
    assert out.count('class="body"') == 3 and out.count(" hidden>") == 3
    controls = re.findall(r'aria-controls="([^"]+)"', out)
    assert len(set(controls)) == 3
    assert all(f'id="{c}"' in out for c in controls)
    # The reasoning step opens to its own paragraph, the tool step to what it was given and what came back.
    assert "work out the metric" in out and "verify the numbers" in out
    assert '<div class="sub">arguments</div>' in out and "&quot;query&quot;: &quot;revenue&quot;" in out
    assert '<div class="sub">result</div>' in out and "&quot;results&quot;: []" in out
    assert "tl-detail" not in out and "data-text" not in out


@_needs_node
def test_reasoning_renders_markdown_bold_instead_of_showing_the_asterisks():
    """Reasoning paragraphs open with a markdown **title**. The page shows that as bold text, on the timeline step and
    in the leftover Reasoning section alike, and never lets anything but its own <strong> through as markup."""
    html = build_html(_doc("gpt-5", True))
    item = _timeline_item()

    on_step = _run_page_js(html, _TIMELINE_FNS, f"timelineHtml({json.dumps(item)})")
    assert "<strong>Plan</strong>\n\nwork out the metric" in on_step
    assert "<strong>Check</strong>" in on_step and "**" not in on_step

    item["reasoning"][2] = "**Leftover** <b>not markup</b>"
    leftover = _run_page_js(html, _TIMELINE_FNS, f"reasoningHtml({json.dumps(item)})")
    assert "<strong>Leftover</strong>" in leftover
    assert "&lt;b&gt;not markup&lt;/b&gt;" in leftover and "<b>" not in leftover

    # An unpaired marker, or one split across paragraphs, stays as written.
    stray = _run_page_js(html, ["esc", "bold"], 'bold("a ** b\\n\\n**c")')
    assert "<strong>" not in stray


@_needs_node
def test_the_timeline_has_one_control_to_open_or_shut_every_step():
    html = build_html(_doc("gpt-5", True))

    out = _run_page_js(html, _TIMELINE_FNS, f"timelineHtml({json.dumps(_timeline_item())})")

    assert out.count('class="tlall"') == 1 and "Expand all" in out
    # The label only reads "Collapse all" once every step is open, so it always names what a click would do.
    wiring = html.split("function wireTimeline(root) {")[1].split("\n}\n")[0]
    assert "steps.some(shut)" in wiring and "every ? 'Collapse all' : 'Expand all'" in wiring
    assert "wireTimeline(d);" in html


@_needs_node
def test_reasoning_is_not_repeated_below_a_timeline_that_already_shows_it():
    """The drawer used to print every reasoning paragraph in full under the timeline. They now sit on the reasoning
    steps, so that section only catches what the timeline cannot show."""
    html = build_html(_doc("gpt-5", True))
    item = _timeline_item()

    leftover = _run_page_js(html, _TIMELINE_FNS, f"reasoningHtml({json.dumps(item)})")
    assert "a paragraph no step points at" in leftover and "#2" in leftover
    assert "work out the metric" not in leftover and "verify the numbers" not in leftover

    item["reasoning"] = item["reasoning"][:2]
    assert _run_page_js(html, _TIMELINE_FNS, f"reasoningHtml({json.dumps(item)})") == ""

    # No timeline to put them on: nothing is lost, all of it is listed.
    del item["detail"]["latency_breakdown"]
    item["reasoning"] = _timeline_item()["reasoning"]
    everything = _run_page_js(html, _TIMELINE_FNS, f"reasoningHtml({json.dumps(item)})")
    assert "work out the metric" in everything and "a paragraph no step points at" in everything
