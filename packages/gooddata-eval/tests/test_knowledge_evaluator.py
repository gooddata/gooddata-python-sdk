# (C) 2026 GoodData Corporation
import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.evaluators.knowledge import (
    AgenticKnowledgeEvaluator,
    judge_input,
    parse_sources_cited,
)
from gooddata_eval.core.models import ChatResult, DatasetItem, KnowledgeInput, ToolCallEvent

_Q = "Who must approve a 30 % discount?"


def _make_evaluator() -> AgenticKnowledgeEvaluator:
    with patch("openai.OpenAI"), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        return AgenticKnowledgeEvaluator()


def _judges(ev: AgenticKnowledgeEvaluator, positive: bool = True, violation: bool = False) -> MagicMock:
    """Script both judges; returns the positive judge's mock."""
    positive_score = MagicMock(return_value=(positive, "ok"))
    ev._positive_judge.score = positive_score
    ev._violation_judge.score = MagicMock(return_value=(violation, "ok"))
    return positive_score


def _item(expected: Any = None, turns: list[str] | None = None, question: str = _Q) -> DatasetItem:
    return DatasetItem(
        id="k1",
        dataset_name="d",
        test_kind="agentic_knowledge",
        question=question,
        expected_output=expected if expected is not None else {},
        knowledge_input=KnowledgeInput(turns=turns) if turns else None,
    )


def _row(title: str, source: str = "this workspace", filename: str = "") -> dict:
    return {"document_id": title.lower(), "filename": filename, "title": title, "content": "...", "source": source}


def _tool(name: str, rows: list[dict]) -> ToolCallEvent:
    """A `search_knowledge` call returning `rows`."""
    return ToolCallEvent(function_name=name, function_arguments="{}", result=json.dumps({"results": rows}))


def _chunks(title: str | None, source: str = "this workspace", filename: str = "doc.pdf") -> ToolCallEvent:
    """A `get_knowledge_chunks` call in gen-ai's real shape: document fields top-level, chunks untitled."""
    result = {
        "filename": filename,
        "title": title,
        "source": source,
        "chunks": [{"chunk_index": 2, "total_chunks": 5, "content": "...", "page_numbers": [3], "scopes": []}],
    }
    return ToolCallEvent(
        function_name="get_knowledge_chunks", function_arguments='{"document_id": "d1"}', result=json.dumps(result)
    )


def _turn(text: str, *tools: ToolCallEvent) -> ChatResult:
    return ChatResult(text_response=text, tool_call_events=list(tools))


_SEARCH_DISCOUNT = _tool("search_knowledge", [_row("Discount Policy", "the parent workspace")])


# ── retrieval checks ────────────────────────────────────────────────────────


def test_expected_document_found_passes_and_records_diagnostics() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy"], "must_include": ["Names the regional sales manager."]}),
        [_turn("The regional sales manager approves it.", _SEARCH_DISCOUNT)],
    )
    assert res.passed is True
    assert res.detail["knowledge_searched"] is True
    assert res.detail["expected_documents_found"] is True
    assert res.detail["documents_retrieved"] == ["Discount Policy"]
    assert res.detail["turn_count"] == 1
    assert "forbidden_documents_absent" not in res.detail
    assert "expected_source_found" not in res.detail


def test_title_match_is_case_insensitive_and_trimmed() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({"expected_documents": ["  discount POLICY "]}), [_turn("Answer.", _SEARCH_DISCOUNT)])
    assert res.detail["expected_documents_found"] is True


def test_a_row_without_title_matches_on_its_filename() -> None:
    ev = _make_evaluator()
    _judges(ev)
    tool = _tool("search_knowledge", [_row("", filename="discount_policy.md")])
    res = ev.evaluate(_item({"expected_documents": ["discount_policy.md"]}), [_turn("Answer.", tool)])
    assert res.detail["expected_documents_found"] is True
    assert res.detail["documents_retrieved"] == ["discount_policy.md"]


def test_a_missing_document_fails_without_the_judge_deciding_it() -> None:
    """Retrieval failure: the answer may read right, the item still fails on retrieval."""
    ev = _make_evaluator()
    _judges(ev, positive=True)
    res = ev.evaluate(
        _item({"expected_documents": ["Customer Glossary"], "must_include": ["x"]}),
        [_turn("Answer.", _SEARCH_DISCOUNT)],
    )
    assert res.passed is False
    assert res.detail["expected_documents_found"] is False
    assert res.detail["include_0"] is True


def test_a_document_found_only_in_get_knowledge_chunks_counts() -> None:
    ev = _make_evaluator()
    _judges(ev)
    chunks = _chunks("Customer Glossary")
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy", "Customer Glossary"]}),
        [_turn("Answer.", _SEARCH_DISCOUNT, chunks)],
    )
    assert res.detail["expected_documents_found"] is True


def test_a_forbidden_document_found_only_in_get_knowledge_chunks_fails() -> None:
    ev = _make_evaluator()
    _judges(ev)
    chunks = _chunks("Old Discount Policy 2023")
    res = ev.evaluate(
        _item({"forbidden_documents": ["old discount policy 2023"]}),
        [_turn("Answer.", _SEARCH_DISCOUNT, chunks)],
    )
    assert res.passed is False
    assert res.detail["forbidden_documents_absent"] is False
    assert res.detail["documents_retrieved"] == ["Discount Policy", "Old Discount Policy 2023"]


def test_a_chunks_result_without_title_matches_on_its_filename() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(
        _item({"forbidden_documents": ["old_policy.pdf"]}),
        [_turn("Answer.", _SEARCH_DISCOUNT, _chunks(None, filename="old_policy.pdf"))],
    )
    assert res.detail["forbidden_documents_absent"] is False


def test_a_chunks_result_for_a_document_not_found_adds_no_document() -> None:
    """gen-ai answers an unknown or out-of-scope id with an empty filename, no title, source "unknown"."""
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({}), [_turn("Answer.", _SEARCH_DISCOUNT, _chunks(None, source="unknown", filename=""))])
    assert res.detail["documents_retrieved"] == ["Discount Policy"]


def test_expected_source_found_only_in_a_chunks_result() -> None:
    ev = _make_evaluator()
    _judges(ev)
    search = _tool("search_knowledge", [_row("Customer Glossary", "this workspace")])
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy"], "expected_source": "an ancestor workspace"}),
        [_turn("Answer.", search, _chunks("Discount Policy", source="an ancestor workspace"))],
    )
    assert res.detail["expected_documents_found"] is True
    assert res.detail["expected_source_found"] is True


def test_documents_from_an_earlier_turn_count() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy"]}, turns=[_Q, "And for 45 %?"]),
        [_turn("Regional manager.", _SEARCH_DISCOUNT), _turn("Not allowed.")],
    )
    assert res.detail["knowledge_searched"] is True
    assert res.detail["expected_documents_found"] is True
    assert res.detail["turn_count"] == 2


def test_no_search_fails_when_a_search_is_expected() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({}), [_turn("Answer.", _chunks("Discount Policy"))])
    assert res.detail["knowledge_searched"] is False
    assert res.passed is False


def test_expect_search_false_drops_the_check() -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(_item({"expect_search": False}), [_turn("Answer.")])
    assert "knowledge_searched" not in res.detail
    assert res.passed is True


@pytest.mark.parametrize(
    ("source", "expected"),
    [("the parent workspace", True), ("  The Parent Workspace ", True), ("this workspace", False)],
)
def test_expected_source_must_label_an_expected_document(source: str, expected: bool) -> None:
    ev = _make_evaluator()
    _judges(ev)
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy"], "expected_source": source}),
        [_turn("Answer.", _SEARCH_DISCOUNT)],
    )
    assert res.detail["expected_source_found"] is expected


def test_expected_source_on_another_document_does_not_count() -> None:
    ev = _make_evaluator()
    _judges(ev)
    tool = _tool(
        "search_knowledge", [_row("Discount Policy", "this workspace"), _row("Glossary", "the parent workspace")]
    )
    res = ev.evaluate(
        _item({"expected_documents": ["Discount Policy"], "expected_source": "the parent workspace"}),
        [_turn("Answer.", tool)],
    )
    assert res.detail["expected_source_found"] is False


def test_an_unreadable_tool_result_is_ignored() -> None:
    ev = _make_evaluator()
    _judges(ev)
    bad = ToolCallEvent(function_name="search_knowledge", function_arguments="{}", result="not json")
    res = ev.evaluate(_item({"expected_documents": ["Discount Policy"]}), [_turn("Answer.", bad)])
    assert res.detail["expected_documents_found"] is False
    assert res.detail["documents_retrieved"] == []


def test_an_empty_last_answer_fails_without_a_judge_call() -> None:
    ev = _make_evaluator()
    positive = _judges(ev)
    res = ev.evaluate(
        _item({"must_include": ["x"]}, turns=[_Q, "Why?"]), [_turn("Answer.", _SEARCH_DISCOUNT), _turn("")]
    )
    assert res.passed is False
    assert res.detail["answered"] is False
    positive.assert_not_called()


# ── Sources section ─────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("answer", "titles"),
    [
        (
            "A 30 % discount needs the regional manager.\n\n---\n**Sources**\n"
            "- *Discount Policy* (discount_policy.pdf), pp. 1-2 — from *the parent workspace*\n"
            "- *Customer Glossary* (`glossary.md`) — from *this workspace*",
            ["Discount Policy", "Customer Glossary"],
        ),
        ("Text.\n\n### Sources\n\n- **Discount Policy** (parent)\n", ["Discount Policy"]),
        ("Text.\n\nSources:\n- Discount Policy (parent)\nThanks.", ["Discount Policy"]),
        ("No sources here.", []),
        ("**Sources**\n- *Old*\n\nMore text.\n\n**Sources**\n- *New* (x)", ["New"]),
    ],
)
def test_parse_sources_cited(answer: str, titles: list[str]) -> None:
    assert parse_sources_cited(answer) == titles


def test_sources_cited_are_diagnostics_and_never_gate() -> None:
    """A list, not bools: quality_score counts bools, and a cited source decides nothing."""
    ev = _make_evaluator()
    _judges(ev)
    answer = "Regional manager.\n\n---\n**Sources**\n- *Some Other Doc* (other.pdf), p. 4 — from *this workspace*"
    res = ev.evaluate(_item({"expected_documents": ["Discount Policy"]}), [_turn(answer, _SEARCH_DISCOUNT)])
    assert res.passed is True
    assert res.detail["sources_cited"] == ["Some Other Doc"]
    assert not any(isinstance(res.detail[key], bool) for key in ("sources_cited", "documents_retrieved", "turn_count"))


# ── judge input ─────────────────────────────────────────────────────────────


def test_judge_reads_the_conversation_and_grades_the_last_answer() -> None:
    ev = _make_evaluator()
    positive = _judges(ev)
    turns = [_Q, "And who approves 45 %?"]
    ev.evaluate(
        _item({"must_include": ["Says 45 % is not allowed."]}, turns=turns),
        [_turn("The regional sales manager.", _SEARCH_DISCOUNT), _turn("Discounts above 40 % are not allowed.")],
    )
    kwargs = positive.call_args.kwargs
    assert _Q in kwargs["input"]
    assert "The regional sales manager." in kwargs["input"]
    assert kwargs["input"].index("The regional sales manager.") < kwargs["input"].index("And who approves 45 %?")
    assert kwargs["actual_output"] == "Discounts above 40 % are not allowed."


def test_single_turn_judge_input_is_the_question() -> None:
    assert judge_input([_Q], ["answer"]) == _Q


def test_earlier_turns_and_answers_are_trimmed_for_the_judge() -> None:
    text = judge_input(["q" * 5000, "THE-LAST-QUESTION"], ["x" * 5000, "THE-LAST-ANSWER"])
    assert "x" * 1500 in text
    assert "x" * 1501 not in text
    assert "q" * 1500 in text
    assert "q" * 1501 not in text
    assert "THE-LAST-QUESTION" in text
    # The last answer is the ACTUAL OUTPUT, not part of the INPUT.
    assert "THE-LAST-ANSWER" not in text


def test_the_last_answer_keeps_its_sources_section() -> None:
    ev = _make_evaluator()
    positive = _judges(ev)
    answer = "Regional manager.\n\n---\n**Sources**\n- *Discount Policy* (`policy.pdf`) — from *the parent workspace*"
    ev.evaluate(_item({"must_include": ["x"]}), [_turn(answer, _SEARCH_DISCOUNT)])
    assert positive.call_args.kwargs["actual_output"] == answer


def test_a_violation_is_inverted() -> None:
    ev = _make_evaluator()
    _judges(ev, violation=True)
    res = ev.evaluate(_item({"must_not_include": ["Says the CFO must approve."]}), [_turn("CFO.", _SEARCH_DISCOUNT)])
    assert res.detail["exclude_0"] is False
    assert res.passed is False


# ── validation ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("expected", "message"),
    [
        ({"expected_document": ["x"]}, "unknown expected_output key"),
        ({"expect_search": "yes"}, "expect_search must be true or false"),
        ({"expected_documents": "Discount Policy"}, "expected_documents must be a JSON array"),
        ({"forbidden_documents": [""]}, "forbidden_documents must be a JSON array of non-empty strings"),
        ({"must_include": [1]}, "must_include must be a JSON array"),
        ({"expected_documents": ["x"], "expected_source": ""}, "expected_source must be a non-empty string"),
        ({"expected_source": "the parent workspace"}, "needs expected_documents"),
        ({"expected_documents": ["x"], "expected_source": "parent"}, "expected_source must be one of"),
        ({"expected_documents": ["x"], "expected_source": "unknown"}, "expected_source must be one of"),
        ("Names the manager.", "expected_output must be a JSON object"),
    ],
)
def test_validate_rejects_a_bad_expected_output(expected: Any, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        AgenticKnowledgeEvaluator.validate(_item(expected))


def test_validate_rejects_turns_that_do_not_start_with_the_question() -> None:
    with pytest.raises(ValueError, match=r"turns\[0\] must equal the question"):
        AgenticKnowledgeEvaluator.validate(_item({}, turns=["Something else", "Then?"]))


def test_validate_rejects_a_blank_question() -> None:
    with pytest.raises(ValueError, match="question must be a non-empty string"):
        AgenticKnowledgeEvaluator.validate(_item({}, question="  "))


@pytest.mark.parametrize("label", ["this workspace", "The Parent Workspace", "an ancestor workspace", "ai hub"])
def test_validate_accepts_every_gen_ai_source_label(label: str) -> None:
    AgenticKnowledgeEvaluator.validate(_item({"expected_documents": ["x"], "expected_source": label}))


def test_validate_accepts_a_full_expected_output() -> None:
    AgenticKnowledgeEvaluator.validate(
        _item(
            {
                "expect_search": True,
                "expected_documents": ["Discount Policy"],
                "forbidden_documents": ["Old Policy"],
                "expected_source": "the parent workspace",
                "must_include": ["a"],
                "must_not_include": ["b"],
                "rubric": ["c"],
            },
            turns=[_Q, "And 45 %?"],
        )
    )


def test_validate_accepts_the_test_kind_routing_key() -> None:
    # langfuse_source routes on expectedOutput.test_kind and keeps it in expected_output.
    AgenticKnowledgeEvaluator.validate(_item({"test_kind": "agentic_knowledge", "expected_documents": ["x"]}))
