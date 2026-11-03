# (C) 2026 GoodData Corporation. All rights reserved.
"""Whether a conversation turn's first reply asked the clarifying question its fixture expects."""

from __future__ import annotations

import re
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field, model_validator

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
_GENERIC_ANSWERS = frozenset(
    {"yes", "no", "ok", "okay", "cancel", "confirm", "continue", "proceed", "skip", "not now", "go ahead"}
)
_ENTITY_KINDS = tuple(sorted({kind for kinds in _REF_ENTITIES.values() for kind in kinds}))
_PAGE_SIZE = 1000
# A shorter skipped option, such as "No" or "Q1", also occurs in text that assumes nothing, so it
# never counts as named.
_MIN_NAMED_OPTION_CHARS = 3


class FirstReply(BaseModel):
    """What the turn's first assistant reply asked, read before any simulated-user answer."""

    asked: bool
    form: ClarificationForm | None = None
    question_count: int = 0
    option_refs: list[str] = Field(default_factory=list)


def read_first_reply(chat_result: ChatResult, *, asked_in_text: bool) -> FirstReply:
    """The reply's clarifying questions; a ``clarifyingQuestions`` part makes it a questionnaire.

    ``asked_in_text`` is the caller's reading of the prose, for a question without a part.
    """
    parts = [p for p in chat_result.unhandled_parts or [] if p.get("type") == "clarifyingQuestions"]
    questions = [q for p in parts for q in p.get("questions") or []]
    options = [str(o.get("text") or "") for q in questions for o in (q.get("control") or {}).get("options") or []]
    refs = [f"{kind}/{obj_id}" for text in options for kind, obj_id in _REF_RE.findall(text)]
    if parts:
        return FirstReply(asked=True, form="questionnaire", question_count=len(questions), option_refs=refs)
    return FirstReply(asked=asked_in_text, form="text" if asked_in_text else None)


def fetch_object_refs(
    host: str, token: str, workspace_id: str, *, transport: httpx.BaseTransport | None = None
) -> set[str]:
    """Every ``<entity kind>/<id>`` the workspace holds, inherited objects included.

    The entity API sends a ``next`` link on every page, an empty one too, so a short page ends the listing.
    A kind the server does not know (404) has no objects. A body that is not an entity page raises ``ValueError``.
    """
    found: set[str] = set()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    with httpx.Client(timeout=60, headers=headers, transport=transport) as client:
        for kind in _ENTITY_KINDS:
            url = f"{host.rstrip('/')}/api/v1/entities/workspaces/{workspace_id}/{kind}"
            page = 0
            while True:
                response = client.get(url, params={"size": _PAGE_SIZE, "page": page})
                if response.status_code == httpx.codes.NOT_FOUND:
                    break
                response.raise_for_status()
                body: Any = response.json()
                data = body.get("data") if isinstance(body, dict) else None
                if not isinstance(data, list):
                    raise ValueError(f"{kind} page {page} is not an entity page")
                found.update(f"{kind}/{obj['id']}" for obj in data if isinstance(obj, dict) and obj.get("id"))
                if len(data) < _PAGE_SIZE:
                    break
                page += 1
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


def clarification_mismatches(
    reply: FirstReply,
    *,
    expects_clarification: bool,
    expected_form: ClarificationForm | None,
    max_questions: int | None,
    known_refs: set[str] | None,
    reads_questionnaire: bool = False,
) -> list[str]:
    """How the first reply differs from the expected clarification; empty when it matches.

    ``known_refs`` is None when the fixture does not ask for grounded options.
    Options without a ``{type/id}`` reference are not checked for grounding.
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
    if known_refs is not None:
        missing = ungrounded_refs(reply.option_refs, known_refs)
        if missing:
            out.append(f"options name objects the workspace does not have: {missing}")
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


def _entity_refs(ref: str) -> set[str]:
    ref_type, _, obj_id = ref.partition("/")
    return {f"{kind}/{obj_id}" for kind in _REF_ENTITIES.get(ref_type, ())}


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
