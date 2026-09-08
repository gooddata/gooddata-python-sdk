# (C) 2026 GoodData Corporation
"""Render a chat turn's non-text parts into the prose an evaluator can read."""

import json

from gooddata_eval.core.models import ChatResult

_MAX_UNHANDLED_PART_CHARS = 2000


def render_search_results(part: dict) -> str:
    """Render one ``searchResults`` part as the list of objects it resolved."""
    objects = part.get("objects") or []
    if not objects:
        return ""
    lines = []
    for obj in objects:
        title = str(obj.get("title") or "").strip()
        obj_id = str(obj.get("id") or "").strip()
        obj_type = str(obj.get("type") or "").strip()
        label = f"{title} ({obj_type}/{obj_id})" if obj_id else title
        description = str(obj.get("description") or "").strip()
        lines.append(f"- {label}: {description}" if description else f"- {label}")
    requested = str(part.get("requestedObjectType") or "object").strip()
    return f"Search results ({len(objects)} {requested}):\n" + "\n".join(lines)


def render_unhandled_part(part: dict) -> str:
    """Best-effort rendering of a part gd-eval does not model, truncated to a sane size."""
    ptype = str(part.get("type") or "unknown")
    body = json.dumps({k: v for k, v in part.items() if k != "type"}, ensure_ascii=False)
    if len(body) > _MAX_UNHANDLED_PART_CHARS:
        body = body[:_MAX_UNHANDLED_PART_CHARS] + "… (truncated)"
    return f"[{ptype}]\n{body}"


def render_answer_text(result: ChatResult) -> str:
    """Everything the agent said this turn: prose plus the content-bearing parts.

    Alert proposals are excluded -- ``agentic.alert_skill.render_alert_proposal`` renders
    those, and importing it here would close a cycle. Returns "" for a turn that produced
    nothing, so callers can keep using falsiness as their "the agent is stuck" signal.
    """
    chunks = [(result.text_response or "").strip()]
    chunks += [render_search_results(part) for part in result.search_results]
    chunks += [render_unhandled_part(part) for part in result.unhandled_parts]
    return "\n\n".join(chunk for chunk in chunks if chunk)
