# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.metric_skill import (
    AgenticMetricSummary,
    MetricRunResult,
    _delete_metric,
    _normalize_maql,
    run_agentic_metric_skill,
)
from gooddata_eval.core.models import ChatResult


def test_normalize_maql_strips_whitespace():
    assert _normalize_maql("  SELECT  { metric/foo }  ") == "SELECT {metric/foo}"


def test_normalize_maql_removes_select_wrapper():
    assert _normalize_maql("(SELECT {metric/abc})") == "{metric/abc}"


def test_metric_run_result_fields():
    r = MetricRunResult(
        conversation_id="c1",
        metric_result={"maql": "SELECT {metric/x}"},
        metric_created=True,
        actual_maql="SELECT {metric/x}",
        maql_correct=True,
        total_turns=1.0,
    )
    assert r.metric_created is True
    assert r.maql_correct is True


def test_agentic_metric_summary_pass_at_k():
    r = MetricRunResult("c1", {"maql": "x"}, True, "x", True, 1.0)
    s = AgenticMetricSummary(run_results=[r], pass_at_k=True, pass_power_k=True, best=r)
    assert s.pass_at_k is True


def test_run_agentic_metric_skill_creates_conversation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )

    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is True
    assert summary.best.metric_created is True
    mock_client.close.assert_called_once()


def test_run_agentic_metric_skill_closes_client_on_no_result():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I will work on that.",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=2,
        )
    mock_client.close.assert_called_once()
    assert summary.pass_at_k is False
    assert summary.best.metric_created is False


def test_run_agentic_metric_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_metric_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    # Runs 1 and 2 always create fresh; run 0 uses existing-conv
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_delete_metric_uses_sdk_entities_api():
    sdk = MagicMock()
    _delete_metric(sdk, "ws1", "foo_metric")
    sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_delete_metric_swallows_failures():
    sdk = MagicMock()
    sdk._client.entities_api.delete_entity_metrics.side_effect = RuntimeError("500")
    # Cleanup is best-effort — a failed delete is logged, never propagated.
    _delete_metric(sdk, "ws1", "foo_metric")


def _create_metric_chat_result(metric_id: str = "foo_metric"):
    return ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": f'{{"data": {{"maql": "SELECT {{metric/foo}}", "metric_id": "{metric_id}"}}}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )


def test_run_agentic_metric_skill_deletes_created_metric():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _create_metric_chat_result()
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    # The metric the run created is deleted on the way out, by its exact id, via the SDK.
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_deletes_metric_even_when_teardown_fails():
    # A metric is created, then conversation teardown raises; the created metric must still
    # have been cleaned up (its deletion happens inside the per-run finally, before teardown).
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _create_metric_chat_result()
    mock_client.delete_conversation.side_effect = RuntimeError("teardown boom")

    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(RuntimeError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")
