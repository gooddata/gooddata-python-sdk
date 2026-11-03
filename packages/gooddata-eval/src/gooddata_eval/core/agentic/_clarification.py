# (C) 2026 GoodData Corporation. All rights reserved.
"""Whether a conversation turn's first reply asked the clarifying question its fixture expects."""

from __future__ import annotations

import functools
import re
from collections.abc import Callable
from typing import Any, Literal

from gooddata_api_client.exceptions import ApiException, NotFoundException
from gooddata_sdk import GoodDataSdk
from gooddata_sdk.utils import load_all_entities
from pydantic import BaseModel, Field, model_validator
from urllib3.exceptions import HTTPError

from gooddata_eval.core._retry import RETRYABLE_STATUS_CODES, retry_transient
from gooddata_eval.core.models import ChatResult

ClarificationForm = Literal["questionnaire", "text"]

_REF_RE = re.compile(r"\{([A-Za-z_]+)/([^{}]+)\}")
# The entity kinds a `{type/id}` option reference can name. An attribute and its label are
# spelled either way by the agent, so each accepts the other. A date dataset is a dataset.
_REF_ENTITIES: dict[str, tuple[str, ...]] = {
    "metric": ("metrics",),
    "fact": ("facts",),
    "dataset": ("datasets",),
    "date": ("datasets",),
    "attribute": ("attributes", "labels"),
    "date_attribute": ("attributes", "labels"),
    "label": ("labels", "attributes"),
    "parameter": ("parameters",),
    "dashboard": ("analyticalDashboards",),
    "analyticalDashboard": ("analyticalDashboards",),
    "visualization": ("visualizationObjects",),
    "visualizationObject": ("visualizationObjects",),
    "insight": ("visualizationObjects",),
}
# Reference types gen-ai writes that no entity listing holds, so grounding cannot check them.
_UNLISTED_REF_TYPES = frozenset({"computed_attribute", "filter_context", "document", "report"})
_ENTITY_KINDS = tuple(sorted({kind for kinds in _REF_ENTITIES.values() for kind in kinds}))
_PAGE_SIZE = 1000
# The EntitiesApi listing of each entity kind.
_LIST_METHODS: dict[str, str] = {
    "analyticalDashboards": "get_all_entities_analytical_dashboards",
    "attributes": "get_all_entities_attributes",
    "datasets": "get_all_entities_datasets",
    "facts": "get_all_entities_facts",
    "labels": "get_all_entities_labels",
    "metrics": "get_all_entities_metrics",
    "parameters": "get_all_entities_parameters",
    "visualizationObjects": "get_all_entities_visualization_objects",
}
# A shorter skipped option, such as "No" or "Q1", also occurs in text that assumes nothing, so it
# never counts as named.
_MIN_NAMED_OPTION_CHARS = 3


OptionTitleKind = Literal["metric", "attribute", "fact", "dataset", "dashboard", "visualization"]
_TITLE_ENTITIES: dict[str, str] = {
    "metric": "metrics",
    "attribute": "attributes",
    "fact": "facts",
    "dataset": "datasets",
    "dashboard": "analyticalDashboards",
    "visualization": "visualizationObjects",
}
# What may follow a title in an option that adds context, as two charts with one title need.
_TITLE_CONTEXT_SEPARATORS = (" (", " [", " - ", " – ", " — ", ": ", ", ")
_GENERIC_ANSWERS = frozenset(
    {"yes", "no", "ok", "okay", "cancel", "confirm", "continue", "proceed", "skip", "not now", "go ahead"}
)
# How an option may spell a chart type whose `local:<type>` id is not a word of its own.
_CHART_TYPE_WORDS: dict[str, tuple[str, ...]] = {
    "combo2": ("combo",),
    "pushpin": ("geo", "map", "pushpin"),
    "heatmap": ("heatmap", "heat map"),
    "treemap": ("treemap", "tree map"),
    "dependencywheel": ("dependency wheel",),
}


class QuestionOptions(BaseModel):
    """One question's options: the ``type/id`` references they name, and the options that name none."""

    refs: list[str] = Field(default_factory=list)
    plain: list[str] = Field(default_factory=list)


class FirstReply(BaseModel):
    """What the turn's first assistant reply asked, read before any simulated-user answer."""

    asked: bool
    form: ClarificationForm | None = None
    questions: list[QuestionOptions] = Field(default_factory=list)

    @property
    def question_count(self) -> int:
        return len(self.questions)

    @property
    def option_refs(self) -> list[str]:
        return [ref for q in self.questions for ref in q.refs]

    @property
    def plain_options(self) -> list[str]:
        return [option for q in self.questions for option in q.plain]

    @property
    def has_options(self) -> bool:
        return any(q.refs or q.plain for q in self.questions)


def read_first_reply(chat_result: ChatResult, *, asked_in_text: bool) -> FirstReply:
    """The reply's clarifying questions; a ``clarifyingQuestions`` part makes it a questionnaire.

    ``asked_in_text`` is the caller's reading of the prose, for a question without a part.
    """
    parts = [p for p in chat_result.unhandled_parts or [] if p.get("type") == "clarifyingQuestions"]
    if not parts:
        return FirstReply(asked=asked_in_text, form="text" if asked_in_text else None)
    questions = []
    for question in (q for p in parts for q in p.get("questions") or []):
        options = _options(question)
        questions.append(
            QuestionOptions(
                refs=[f"{kind}/{obj_id}" for text in options for kind, obj_id in _REF_RE.findall(text)],
                plain=[text for text in options if not _REF_RE.search(text)],
            )
        )
    return FirstReply(asked=True, form="questionnaire", questions=questions)


class WorkspaceObjects(BaseModel):
    """The workspace's objects as the option checks read them: ``<entity kind>/<id>`` and their titles."""

    refs: set[str] = Field(default_factory=set)
    # `<entity kind>/<id>` -> the title, casefolded with whitespace collapsed.
    titles: dict[str, str] = Field(default_factory=dict)
    # `visualizationObjects/<id>` -> the chart type, `local:donut` read as `donut`.
    chart_types: dict[str, str] = Field(default_factory=dict)

    def titles_of(self, entity_kind: str) -> set[str]:
        return {title for ref, title in self.titles.items() if ref.startswith(f"{entity_kind}/")}


def _title_key(text: str) -> str:
    return " ".join(text.casefold().split())


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, ApiException):
        return exc.status in RETRYABLE_STATUS_CODES
    return isinstance(exc, HTTPError)


def _page_with_retry(list_page: Callable[..., Any], **page: int) -> Any:
    return retry_transient(lambda: list_page(**page), is_retryable=_is_transient)


def fetch_workspace_objects(sdk: GoodDataSdk, workspace_id: str) -> WorkspaceObjects:
    """Every ``<entity kind>/<id>`` and title the workspace holds, inherited objects included.

    A page that fails with a transient error is retried as a chat message is. A kind the server does
    not know (404) has no objects. Any other failure of the entity API is raised.
    """
    found = WorkspaceObjects()
    api = sdk._client.entities_api
    for kind in _ENTITY_KINDS:
        list_page = functools.partial(getattr(api, _LIST_METHODS[kind]), workspace_id, _check_return_type=False)
        try:
            data = load_all_entities(functools.partial(_page_with_retry, list_page), page_size=_PAGE_SIZE).data
        except NotFoundException:
            continue
        for obj in data:
            if not isinstance(obj, dict) or not obj.get("id"):
                continue
            ref = f"{kind}/{obj['id']}"
            found.refs.add(ref)
            raw_attributes = obj.get("attributes")
            attributes: dict[str, Any] = raw_attributes if isinstance(raw_attributes, dict) else {}
            title = attributes.get("title")
            if isinstance(title, str) and title:
                found.titles[ref] = _title_key(title)
            raw_content = attributes.get("content")
            content: dict[str, Any] = raw_content if isinstance(raw_content, dict) else {}
            chart_url = str(content.get("visualizationUrl") or "")
            if chart_url.startswith("local:"):
                found.chart_types[ref] = chart_url.removeprefix("local:")
    return found


def ungrounded_refs(refs: list[str], known: set[str]) -> list[str]:
    """The references that name no object of the workspace, or a kind it has none of.

    A type of ``_UNLISTED_REF_TYPES`` is left unchecked.
    """
    missing: list[str] = []
    for ref in refs:
        ref_type, _, obj_id = ref.partition("/")
        if ref_type in _UNLISTED_REF_TYPES:
            continue
        kinds = _REF_ENTITIES.get(ref_type, ())
        if not any(f"{kind}/{obj_id}" in known for kind in kinds):
            missing.append(ref)
    return missing


def _is_titled(option: str, titles: set[str]) -> bool:
    key = _title_key(option)
    return key in titles or any(key.startswith(title + sep) for title in titles for sep in _TITLE_CONTEXT_SEPARATORS)


def untitled_options(options: list[str], objects: WorkspaceObjects, kind: OptionTitleKind) -> list[str]:
    """The options that are not the title of a ``kind`` object, alone or followed by added context."""
    titles = objects.titles_of(_TITLE_ENTITIES[kind])
    return [option for option in options if not _is_titled(option, titles)]


def _off_in_scope(
    questions: list[QuestionOptions], off_of: Callable[[QuestionOptions], tuple[int, list[str]]]
) -> list[str]:
    """The options an option check fails, read only from the questions the check is about.

    ``off_of`` gives a question's count of options the check reads and the ones it fails. A questionnaire
    can ask about more than one thing, such as a metric next to a channel: a question with at least one
    option the check accepts is about it, and a question with none is about something else and left out.
    When no question is about it, every option the check read fails.
    """
    checked = [off_of(q) for q in questions]
    about = [off for read, off in checked if len(off) < read]
    return [option for off in (about or [off for _, off in checked]) for option in off]


def untitled_question_options(reply: FirstReply, objects: WorkspaceObjects, kind: OptionTitleKind) -> list[str]:
    """The plain-text options that are not the title of a ``kind`` object, in the questions about that kind."""
    return _off_in_scope(reply.questions, lambda q: (len(q.plain), untitled_options(q.plain, objects, kind)))


def _entity_refs(ref: str) -> set[str]:
    ref_type, _, obj_id = ref.partition("/")
    return {f"{kind}/{obj_id}" for kind in _REF_ENTITIES.get(ref_type, ())}


def is_object_ref(ref: str) -> bool:
    """Whether ``ref`` is ``type/id`` with a type an option reference can name."""
    ref_type, sep, obj_id = ref.partition("/")
    return bool(sep and obj_id) and ref_type in _REF_ENTITIES


def _names_chart_type(option: str, chart_type: str) -> bool:
    key = _title_key(option)
    return any(re.search(rf"\b{re.escape(word)}\b", key) for word in _CHART_TYPE_WORDS.get(chart_type, (chart_type,)))


def off_candidate_options(reply: FirstReply, objects: WorkspaceObjects, candidates: list[str]) -> list[str]:
    """The options that name none of ``candidates``, in the questions that offer at least one of them.

    An option names a candidate by reference, by its title plus context, or by its chart type when
    no other candidate has that type: "Donut chart" tells two same-titled charts apart only then.
    A chart type does not count in an option that starts with the title of an object outside the candidates.
    """
    wanted = set().union(*(_entity_refs(c) for c in candidates))
    titles = {objects.titles[ref] for ref in wanted if ref in objects.titles}
    kinds = {ref.partition("/")[0] for ref in wanted}
    other_titles = {
        title for ref, title in objects.titles.items() if ref not in wanted and ref.partition("/")[0] in kinds
    } - titles
    types = [objects.chart_types[ref] for ref in wanted if ref in objects.chart_types]
    unique_types = {chart_type for chart_type in types if types.count(chart_type) == 1}

    def names_a_candidate_type(option: str) -> bool:
        return any(_names_chart_type(option, t) for t in unique_types) and not _is_titled(option, other_titles)

    def off_of(question: QuestionOptions) -> tuple[int, list[str]]:
        off = [ref for ref in question.refs if not (_entity_refs(ref) & wanted)]
        off += [
            option for option in question.plain if not _is_titled(option, titles) and not names_a_candidate_type(option)
        ]
        return len(question.refs) + len(question.plain), off

    return _off_in_scope(reply.questions, off_of)


def clarification_mismatches(
    reply: FirstReply,
    *,
    expects_clarification: bool,
    expected_form: ClarificationForm | None,
    max_questions: int | None,
    objects: WorkspaceObjects | None,
    grounded: bool,
    titled_as: OptionTitleKind | None,
    candidates: list[str] | None = None,
    reads_questionnaire: bool = False,
) -> list[str]:
    """How the first reply differs from the expected clarification; empty when it matches.

    ``grounded`` checks the ``{type/id}`` options of every question; ``titled_as`` checks the plain-text
    ones against that kind's titles; ``candidates`` requires every option to name one of those objects.
    The last two read only the questions they are about (see ``_off_in_scope``). All three are skipped
    when ``objects`` is None: the caller reports the turn ungraded then.
    ``reads_questionnaire`` fails a prose question, which has no options for these checks to read.
    """
    if not expects_clarification:
        return [f"asked a clarifying question ({reply.form}) the request does not need"] if reply.asked else []
    if not reply.asked:
        return ["expected a clarifying question, but the first reply asked none"]
    out: list[str] = []
    if expected_form is not None and reply.form != expected_form:
        out.append(f"clarification form: expected {expected_form}, got {reply.form}")
    elif reads_questionnaire and reply.form != "questionnaire":
        out.append(f"the turn checks a questionnaire, but the first reply asked as {reply.form}")
    if max_questions is not None and reply.question_count > max_questions:
        out.append(f"asked {reply.question_count} questions, at most {max_questions} expected")
    if objects is not None and grounded:
        missing = ungrounded_refs(reply.option_refs, objects.refs)
        if missing:
            out.append(f"options name objects the workspace does not have: {missing}")
    if objects is not None and titled_as is not None:
        untitled = untitled_question_options(reply, objects, titled_as)
        if untitled:
            out.append(f"options are not the title of a {titled_as} of the workspace: {untitled}")
    if objects is not None and candidates:
        off = off_candidate_options(reply, objects, candidates)
        if off:
            out.append(f"options name none of {candidates}: {off}")
    return out


class ClarifyingPick(BaseModel):
    """An option the fixture picks in a questionnaire.

    ``option`` is a ``type/id`` reference the option names, or the option's whole text. A list names
    the spellings of one option, since the agent writes it as a reference or as plain text.
    ``question`` limits the pick to that position; without it, the first question offering the
    option takes it.
    """

    option: str | list[str]
    question: int | None = Field(default=None, ge=0)

    @property
    def spellings(self) -> list[str]:
        return [self.option] if isinstance(self.option, str) else list(self.option)

    @property
    def label(self) -> str:
        return " | ".join(self.spellings)

    @model_validator(mode="after")
    def _names_an_option(self) -> ClarifyingPick:
        if not self.spellings or not all(s.strip() for s in self.spellings):
            raise ValueError("option needs at least one non-empty spelling")
        return self


class ClarifyingAnswers(BaseModel):
    """The ``clarifyingAnswers`` for one questionnaire, and what they left out."""

    answers: list[dict] = Field(default_factory=list)
    skipped: list[dict] = Field(default_factory=list)
    matched_picks: list[str] = Field(default_factory=list)

    def render(self) -> str:
        """The text gen-ai builds for the model from these answers: every question, a skipped one as Skipped."""
        sections = [(a["questionIndex"], a["questionText"], a["answer"]["optionText"]) for a in self.answers]
        sections += [(s["index"], s["text"], "Skipped") for s in self.skipped]
        return "\n\n".join(f"**{text}**\n\n{answer}" for _, text, answer in sorted(sections, key=lambda s: s[0]))


def _all_questions(chat_result: ChatResult) -> list[dict]:
    parts = [p for p in chat_result.unhandled_parts or [] if p.get("type") == "clarifyingQuestions"]
    return [q for p in parts for q in p.get("questions") or []]


def _questions(chat_result: ChatResult) -> list[dict]:
    """The questions of the item the answers name, numbered as gen-ai numbers them: across that item's parts."""
    item_id = chat_result.clarifying_questions_item_id
    parts = [
        p
        for p in chat_result.unhandled_parts or []
        if p.get("type") == "clarifyingQuestions" and p.get("itemId") in (None, item_id)
    ]
    return [q for p in parts for q in p.get("questions") or []]


def _options(question: dict) -> list[str]:
    return [str(o.get("text") or "") for o in (question.get("control") or {}).get("options") or []]


def _plain(text: str) -> str:
    return " ".join(_REF_RE.sub(" ", text).lower().split())


def _same_object(ref: str, other: str) -> bool:
    return ref == other or bool(_entity_refs(ref) & _entity_refs(other))


def option_matches(option_text: str, wanted: str) -> bool:
    """Whether an option is the one a pick names, by its ``{type/id}`` reference or its whole text.

    A reference matches the spellings grounding accepts for the same object, such as ``attribute/x`` and ``label/x``.
    """
    ref = wanted.strip().strip("{}")
    if "/" in ref and any(_same_object(ref, f"{kind}/{obj_id}") for kind, obj_id in _REF_RE.findall(option_text)):
        return True
    return option_text.strip().lower() == wanted.strip().lower()


def build_clarifying_answers(chat_result: ChatResult, picks: list[ClarifyingPick]) -> ClarifyingAnswers:
    """Answer the reply's questionnaire with the picks; a question no pick matches is skipped."""
    questions = _questions(chat_result)
    out = ClarifyingAnswers()
    answered: set[int] = set()
    for pick in picks:
        for qi, question in enumerate(questions):
            if qi in answered or (pick.question is not None and pick.question != qi):
                continue
            oi = next(
                (
                    i
                    for i, text in enumerate(_options(question))
                    if any(option_matches(text, spelling) for spelling in pick.spellings)
                ),
                None,
            )
            if oi is None:
                continue
            answered.add(qi)
            out.matched_picks.append(pick.label)
            out.answers.append(
                {
                    "questionIndex": qi,
                    "questionText": question.get("text") or "",
                    "answer": {"type": "singleChoice", "optionIndex": oi, "optionText": _options(question)[oi]},
                }
            )
            break
    out.answers.sort(key=lambda a: a["questionIndex"])
    out.skipped = [
        {"index": qi, "text": q.get("text") or "", "options": _options(q)}
        for qi, q in enumerate(questions)
        if qi not in answered
    ]
    return out


def _names_option(text: str, option: str) -> bool:
    """Whether ``text`` names the option: one of its references whole, or its words as whole words."""
    refs_in_text = [f"{kind}/{obj_id}" for kind, obj_id in _REF_RE.findall(text)]
    for kind, obj_id in _REF_RE.findall(option):
        if any(_same_object(f"{kind}/{obj_id}", ref) for ref in refs_in_text):
            return True
    label = _plain(option)
    return (
        len(label) >= _MIN_NAMED_OPTION_CHARS
        and re.search(rf"(?<!\w){re.escape(label)}(?!\w)", _plain(text)) is not None
    )


def _same_question(question: dict, skipped: dict) -> bool:
    """Whether ``question`` asks ``skipped`` again: the same text, or the same options that name something.

    Options such as Yes and No fit any question, a confirmation too, so they count only with the same text.
    """
    if _plain(question.get("text") or "") == _plain(skipped["text"]):
        return True
    options = sorted(_options(question))
    specific = any(_plain(option).strip(".!") not in _GENERIC_ANSWERS for option in options)
    return specific and options == sorted(skipped["options"])


def after_answers_mismatches(
    *,
    unmatched_picks: list[str],
    skipped: list[dict],
    replies_after: list[tuple[str, ChatResult, bool]],
    states_skipped_assumption: bool,
    skipped_questions_not_reasked: bool,
    expects_confirmation_after_answers: bool,
) -> list[str]:
    """How the turn after its structured answers differs from the fixture; empty when it matches.

    ``replies_after`` holds each later reply with its kind (``output`` or a ``classify_reply`` kind) and
    whether it answers a ``clarifyingAnswers`` message directly.

    ``states_skipped_assumption`` stands in for "the agent says what it assumed": it passes when any reply
    after the answers names an option of each skipped question. It cannot tell an assumption from a
    mention, and it does not need the assumption in the final reply, since a reply that asks for
    confirmation usually states it.
    """
    out = [f"no questionnaire offered the picked option {pick!r}" for pick in unmatched_picks]
    if states_skipped_assumption:
        texts = [reply.text_response or "" for _, reply, _ in replies_after]
        out.extend(
            f"no reply after the answers names an option of the skipped question {question['text']!r}"
            for question in skipped
            if not any(_names_option(text, option) for text in texts for option in question["options"])
        )
    if skipped_questions_not_reasked:
        for question in skipped:
            asked_again = any(
                _same_question(later, question) for _, reply, _ in replies_after for later in _all_questions(reply)
            )
            if asked_again:
                out.append(f"asked the skipped question {question['text']!r} again")
    if expects_confirmation_after_answers and any(kind == "output" and follows for kind, _, follows in replies_after):
        out.append("acted on the answers in the same reply, without waiting for confirmation")
    return out
