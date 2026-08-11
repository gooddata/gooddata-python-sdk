# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from gooddata_eval.core.agentic._langfuse import find_traces_per_conversation


def test_find_traces_per_conversation_is_none_for_a_conversation_with_no_trace():
    # find_traces_per_conversation's return dict is seeded with dict.fromkeys(conversation_ids)
    # (every value starts None) and only overwritten for ids where a trace was actually found --
    # callers (kda_skill.py and every other agentic skill) must treat a missing conversation as
    # None, not assume every key maps to a real trace object.
    found_trace = MagicMock(latency=12.0)

    def _fetch(langfuse, cid, window_start, window_end, pad):
        return [found_trace] if cid == "conv-found" else []

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", side_effect=_fetch),
        patch("gooddata_eval.core.agentic._langfuse.time.sleep"),
    ):
        result = find_traces_per_conversation(MagicMock(), ["conv-found", "conv-missing"], datetime.now(timezone.utc))

    assert result["conv-found"] is found_trace
    assert result["conv-missing"] is None
