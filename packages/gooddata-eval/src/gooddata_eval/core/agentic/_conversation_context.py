# (C) 2026 GoodData Corporation. All rights reserved.
"""What the conversation evaluator needs to judge context, not just output presence.

Three questions get asked of every assistant reply that did not produce the turn's
expected output:

1. What kind of reply is it -- a confirmation request ("Should I create this metric?"),
   a question to the user, or a turn that ended without doing anything (a stall)?
2. For a question: did the assistant ask for something the conversation had already
   established? That is the lost-context signal, graded by a binary LLM judge.
3. What does the simulated user say back? In ``context`` mode it never sees the turn's
   expected output -- only the fixture's set answers and the conversation itself -- so a
   lost context can no longer be repaired silently by a user who knows the answer key.

Only information that is IN the conversation counts. A question about something the
assistant could have looked up in the workspace, but that nobody mentioned, is graded as
legitimate: whether the assistant should have looked it up is a separate check.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from typing import Literal

from gooddata_eval.core.config import judge_model
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge, _message_content
from gooddata_eval.core.models import ChatResult

ReplyKind = Literal["confirmation", "question", "no_action"]

NUDGE_MESSAGE = "Please go ahead and do it."
CONFIRMATION_REPLY = "Yes, go ahead."
# Asked to pick from a list (which dashboard to bind an alert to), a real user picks one.
NO_ANSWER_REPLY = "Use your best judgement and go ahead. If you need me to pick from a list, take the first option."

# Part of the metric and alert skills' designed flow, not a clarification.
_CONFIRMATION_RE = re.compile(
    r"\b(?:should|shall|may|can)\s+i\s+(?:go\s+ahead|proceed|create|save|update|apply|add|set\s+(?:it|this)\s+up)"
    r"|\bdo\s+you\s+want\s+me\s+to\s+(?:go\s+ahead|proceed|create|save|update|apply)"
    r"|\bwould\s+you\s+like\s+me\s+to\s+(?:go\s+ahead|proceed|create|save|update|apply)"
    r"|\bplease\s+confirm\b|\bconfirm\s+(?:if|whether|that)\b",
    re.IGNORECASE,
)

# Checked after _CONFIRMATION_RE, so "please confirm" stays a confirmation.
_REQUEST_RE = re.compile(
    r"\bplease\s+(?:select|choose|pick|specify|provide|tell\s+me|let\s+me\s+know|clarify|share)\b"
    r"|\breply\s+with\b|\b(?:select|choose|pick)\s+(?:one|a|an|the)\b",
    re.IGNORECASE,
)

_MESSAGE_CHARS = 800
_TRANSCRIPT_MESSAGES = 40


def has_structured_question(chat_result: ChatResult) -> bool:
    """gen-ai's own signal that the reply is a question: a ``clarifyingQuestions`` part."""
    return any(part.get("type") == "clarifyingQuestions" for part in chat_result.unhandled_parts or [])


def classify_reply(chat_result: ChatResult, rendered_text: str) -> ReplyKind:
    """Kind of a reply that did not produce the expected output.

    The structured ``clarifyingQuestions`` part is authoritative when present. Without it
    the text decides: a confirmation phrase or an alert proposal is a confirmation, a
    question mark is a question, and anything else -- including an empty reply -- is a turn
    that stopped without acting.
    """
    if has_structured_question(chat_result):
        return "question"
    if chat_result.alert_proposals:
        return "confirmation"
    text = (rendered_text or "").strip()
    if not text:
        return "no_action"
    if _CONFIRMATION_RE.search(text):
        return "confirmation"
    if "?" in text or _REQUEST_RE.search(text):
        return "question"
    return "no_action"


@dataclass
class TranscriptEntry:
    role: Literal["user", "assistant"]
    text: str


def clip(text: str, limit: int = _MESSAGE_CHARS) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def summarize_visualizations(chat_result: ChatResult) -> str:
    """One line per chart the reply showed: what it plotted and how it was filtered.

    Charts carry most of what a conversation establishes ("the Apparel filter", "by
    quarter"), and they are invisible in the text part. The judge needs them to know what
    was already settled.
    """
    vizzes = chat_result.created_visualizations
    objects = getattr(vizzes, "objects", None) or []
    lines = []
    for viz in objects:
        fields = [getattr(f, "using", f) for f in (viz.query.fields or {}).values()]
        filters = [
            {k: v for k, v in f.items() if k in ("type", "using", "state", "from", "to", "top", "bottom")}
            for f in (viz.query.filter_by or {}).values()
            if isinstance(f, dict)
        ]
        lines.append(f"[chart {viz.type or ''}: fields={fields} filters={filters}]")
    return " ".join(lines)


def render_transcript(entries: list[TranscriptEntry]) -> str:
    recent = entries[-_TRANSCRIPT_MESSAGES:]
    return "\n".join(f"{e.role.upper()}: {clip(e.text)}" for e in recent)


_JUDGE_SYSTEM = """\
You grade one question that an analytics assistant asked its user. You get:
- CONVERSATION BEFORE: everything said before the user's latest message (may be empty),
- LATEST MESSAGE: what the user just asked,
- QUESTION: the assistant's reply, in which it asks the user something instead of doing it.

Decide whether the information the QUESTION asks for already appears in CONVERSATION BEFORE:
stated by the user, or determined by an assistant answer -- for example which metric was meant,
which filters apply, which item came out weakest or biggest, what a chart showed, which object
was created.

Rules:
- The LATEST MESSAGE does not count. A reference in it ("it", "that second one", "those
  brands") only points at something that must appear in CONVERSATION BEFORE.
- If CONVERSATION BEFORE is empty, the answer is false.
- Information that exists in the workspace but was never mentioned in the conversation does not
  count.
- Do not judge whether asking was useful, necessary or well phrased.

Examples:
- BEFORE: user "Net sales by country." / assistant "Here is net sales by country." LATEST: "Add
  order count to it." QUESTION: "Which chart should I add order count to?" -> true (the chart
  just made).
- BEFORE: user "Top 10 products by revenue." / assistant "Here are the top 10 products."
  LATEST: "Remove the limit." QUESTION: "Which limit do you mean?" -> true (the top 10).
- BEFORE: (empty) LATEST: "Show revenue by month." QUESTION: "Which revenue metric: gross or
  net?" -> false (nothing earlier says which).

Return a JSON object with exactly two keys:
  "already_in_conversation": true or false
  "reasoning": one sentence naming the information and where it appears, or that it does not
"""

_JUDGE_USER = "CONVERSATION BEFORE:\n{history}\n\nLATEST MESSAGE:\n{latest}\n\nQUESTION:\n{question}"


def judge_prompt(history: str, latest: str, question: str) -> str:
    """The user prompt the clarification judge reads, also recorded for auditing."""
    return _JUDGE_USER.format(history=history or "(empty)", latest=latest, question=question)


@dataclass(frozen=True)
class ClarificationVerdict:
    lost_context: bool | None  # None when the judge could not be run or gave no verdict
    reasoning: str
    error: str | None = None


class _ClarificationLLM(LLMJudge):
    """``LLMJudge``'s client, temperature handling and retry, with this judge's own prompt and
    verdict key. The key names the question asked, so a 0/1 cannot be read the wrong way round."""

    def __init__(self, model: str | None = None) -> None:
        super().__init__([], model=model)
        self._system_prompt = _JUDGE_SYSTEM

    def already_in_conversation(self, prompt: str) -> tuple[bool, str]:
        messages = [{"role": "system", "content": self._system_prompt}, {"role": "user", "content": prompt}]
        raw = None
        for _attempt in range(2):
            raw = _message_content(self._create_completion(messages))
            if isinstance(raw, str) and raw.strip():
                break
        if not (isinstance(raw, str) and raw.strip()):
            raise JudgeResponseError(f"clarification judge {self.model!r} returned an empty body twice")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JudgeResponseError(f"clarification judge returned unparseable JSON: {raw!r}") from exc
        value = data.get("already_in_conversation") if isinstance(data, dict) else None
        if not isinstance(value, bool):
            raise JudgeResponseError(f"clarification judge returned no boolean verdict: {raw!r}")
        return value, str(data.get("reasoning", ""))


class ClarificationJudge:
    """Binary judge: did the assistant ask for something the conversation already established?

    Temperature 0 and a JSON verdict, on ``LLMJudge``'s client. Verdicts are cached per prompt,
    so a conversation that repeats the same question does not pay for it twice.
    """

    def __init__(self, model: str | None = None) -> None:
        self._model = model
        self._llm: _ClarificationLLM | None = None
        self._cache: dict[str, ClarificationVerdict] = {}
        self._warned = False

    @property
    def model_name(self) -> str:
        """The judge model, without building a client (which needs an API key)."""
        return self._llm.model if self._llm is not None else (self._model or judge_model())

    def judge(self, history: str, latest: str, question: str) -> ClarificationVerdict:
        prompt = judge_prompt(history, latest, question)
        key = hashlib.sha256(prompt.encode()).hexdigest()
        if key in self._cache:
            return self._cache[key]
        try:
            if self._llm is None:
                self._llm = _ClarificationLLM(self._model)
            try:
                found, reasoning = self._llm.already_in_conversation(prompt)
                verdict = ClarificationVerdict(lost_context=found, reasoning=reasoning)
            except JudgeResponseError as exc:
                verdict = ClarificationVerdict(lost_context=None, reasoning="", error=str(exc))
        except Exception as exc:  # noqa: BLE001 -- a grading fault must not fail the agent's conversation
            if not self._warned:
                print(f"[JUDGE] clarifications left unjudged: {exc}")
                self._warned = True
            verdict = ClarificationVerdict(lost_context=None, reasoning="", error=str(exc))
        self._cache[key] = verdict
        return verdict


_SIM_USER_MODEL = "gpt-4o"


def _chat(prompt_system: str, prompt_user: str) -> str | None:
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError:
        return None
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        response = OpenAI(api_key=api_key).chat.completions.create(
            model=_SIM_USER_MODEL,
            messages=[{"role": "system", "content": prompt_system}, {"role": "user", "content": prompt_user}],
            temperature=0,
            max_tokens=200,
        )
    except Exception as exc:
        print(f"[SIM-USER] reply failed: {exc}")
        return None
    content = response.choices[0].message.content if response.choices else None
    return content.strip() if content else None


def reply_from_facts(transcript: str, question: str, facts: list[str]) -> str:
    """A legitimate question the fixture has no unused set answer for.

    The reply may use only the fixture's facts for this turn -- never the expected output --
    and falls back to "use your best judgement" when the facts do not cover the question.
    """
    if not facts:
        return NO_ANSWER_REPLY
    reply = _chat(
        "You play a business user talking to an analytics assistant. Answer its question briefly, "
        "using ONLY the facts listed below. Never invent requirements. If the facts do not answer "
        f"the question, reply exactly: {NO_ANSWER_REPLY}",
        f"Conversation so far:\n{transcript}\n\nThe assistant now asks:\n{question}\n\n"
        "Facts you know:\n" + "\n".join(f"- {f}" for f in facts),
    )
    return reply or NO_ANSWER_REPLY


def reply_restating(transcript: str, question: str) -> str:
    """The assistant asked for something the conversation already established.

    The turn is already failed; restating keeps the rest of the conversation measurable,
    which is what a real user would do too.
    """
    reply = _chat(
        "You play a business user talking to an analytics assistant. The assistant just asked for "
        "something that was already said or found earlier in the conversation. Reply briefly, "
        "starting with 'As I said earlier,' and repeat only that information, taken from the "
        "conversation. Do not add anything new.",
        f"Conversation so far:\n{transcript}\n\nThe assistant now asks:\n{question}",
    )
    return reply or "As I said earlier in this conversation — please use what we already established."
