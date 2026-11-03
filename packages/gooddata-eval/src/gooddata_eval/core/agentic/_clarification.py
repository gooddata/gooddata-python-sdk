# (C) 2026 GoodData Corporation. All rights reserved.
"""Whether a conversation turn's first reply asked the clarifying question its fixture expects."""

from __future__ import annotations

import re
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field

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
