# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import os
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.metric_skill import (
    AgenticMetricSummary,
    MetricRunResult,
    SimulatedResponseError,
    _delete_metric,
    _expected_metric_ids,
    _normalize_maql,
    generate_simulated_response,
    run_agentic_metric_skill,
)
from gooddata_eval.core.chat.sse_client import ChatError
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
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch(
            "gooddata_eval.core.agentic.metric_skill.generate_simulated_response",
            return_value="Go ahead and create it.",
        ) as mock_sim,
    ):
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
    mock_sim.assert_called_once_with("I will work on that.", {"maql": "SELECT {metric/foo}"})


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


def test_generate_simulated_response_without_an_api_key():
    with (
        patch.dict(sys.modules, {"openai": MagicMock()}),
        patch.dict(os.environ, {}, clear=True),
        pytest.raises(SimulatedResponseError, match="OPENAI_API_KEY"),
    ):
        generate_simulated_response("Which brand field?", {"maql": "SELECT {metric/foo}"})


def test_generate_simulated_response_without_the_openai_package():
    with (
        patch.dict(sys.modules, {"openai": None}),
        pytest.raises(SimulatedResponseError, match="openai package is required"),
    ):
        generate_simulated_response("Which brand field?", {"maql": "SELECT {metric/foo}"})


def test_run_agentic_metric_skill_fails_the_run_when_the_simulated_reply_cannot_be_generated():
    exc = SimulatedResponseError("OPENAI_API_KEY environment variable is not set")
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Which brand field should I count?",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.generate_simulated_response", side_effect=exc) as mock_sim,
    ):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=3,
        )

    assert summary.pass_at_k is False
    assert summary.best.metric_created is False
    assert summary.best.total_turns == 1.0
    mock_client.close.assert_called_once()
    mock_sim.assert_called_once_with("Which brand field should I count?", {"maql": "SELECT {metric/foo}"})


def _metric_ns(metric_id):
    return SimpleNamespace(id=metric_id)


def _brand_expected(created_new=True):
    return {
        "maql": "SELECT COUNT({label/product_brand})",
        "title": "Unique Product Brand Count",
        "metric_id": "unique_product_brand_count",
        "created_new": created_new,
    }


def test_expected_metric_ids_covers_the_fixture_id_and_its_title_slug():
    assert _expected_metric_ids([_brand_expected()]) == {"unique_product_brand_count"}
    assert _expected_metric_ids([{"title": "MoM Net Sales Growth"}]) == {"mom_net_sales_growth"}


def test_run_agentic_metric_skill_clears_a_stale_metric_before_the_run():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _create_metric_chat_result()
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        # Before the run a leftover of the expected metric is still there; after it, nothing extra.
        mock_sdk.catalog_workspace_content.get_metrics_catalog.side_effect = [
            [_metric_ns("unique_product_brand_count"), _metric_ns("net_sales")],
            [],
        ]
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output=_brand_expected(),
            k=1,
            max_iterations=1,
        )

    deleted = [c.args for c in mock_sdk._client.entities_api.delete_entity_metrics.call_args_list]
    # The leftover goes first, then the metric this run created. A baseline metric is untouched.
    assert deleted == [("ws1", "unique_product_brand_count"), ("ws1", "foo_metric")]


def test_run_agentic_metric_skill_keeps_an_existing_metric_the_fixture_expects_to_be_reused():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = ChatResult.model_validate(
        {"textResponse": "Reused it.", "toolCallEvents": [], "reasoningStepCount": 1}
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        mock_sdk.catalog_workspace_content.get_metrics_catalog.return_value = [_metric_ns("unique_product_brand_count")]
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output=_brand_expected(created_new=False),
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_not_called()


def test_run_agentic_metric_skill_deletes_the_metric_a_dead_stream_left_behind():
    """The create_metric result never reaches the client when the SSE stream dies, but the
    metric exists server-side — the partial result is what makes it findable."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = ChatError(
        "SSE stream error: peer closed connection",
        partial_result=_create_metric_chat_result(),
    )
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(ChatError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        mock_sdk.catalog_workspace_content.get_metrics_catalog.return_value = []
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output=_brand_expected(),
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_sweeps_a_metric_no_tool_call_ever_reported():
    """Nothing at all came back from the stream, so the id is unknown — the metric is found by
    the identity the fixture expects."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = ChatError("SSE stream error: peer closed connection")
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(ChatError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        mock_sdk.catalog_workspace_content.get_metrics_catalog.side_effect = [
            [],
            [_metric_ns("unique_product_brand_count")],
        ]
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output=_brand_expected(),
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "unique_product_brand_count")
