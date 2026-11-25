# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import copy
import json
from collections.abc import Callable
from types import EllipsisType
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic._alert_update import (
    AlertUpdateEvaluation,
    AutomationApi,
    evaluate_update,
    setup_entity,
    targets_alert,
    update_expectation,
    update_sim_user_prompt,
)
from gooddata_eval.core.agentic.alert_skill import (
    ALERT_CONDITIONAL_SCORES,
    AlertRunResult,
    _failed_checks,
    _update_calls,
    generate_simulated_update_response,
    run_agentic_alert_skill,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.models import ChatResult, LoopExit, ToolCallEvent

# Changes the stored alert in place, the way the agent's update did.
Edit = Callable[[dict], None]

_CATEGORY_FILTER = {
    "positiveAttributeFilter": {
        "label": {"identifier": {"id": "product_category", "type": "label"}},
        "in": {"values": ["Clothing"]},
    }
}
_LAST_MONTH = {
    "relativeDateFilter": {
        "dataset": {"identifier": {"id": "date", "type": "dataset"}},
        "granularity": "MONTH",
        "from": -1,
        "to": -1,
    }
}
_NET_SALES = {
    "localIdentifier": "net_sales",
    "definition": {"measure": {"item": {"identifier": {"id": "net_sales", "type": "metric"}}}},
}

# Trimmed from a stored alert the agent created on the eval fixture (probe 2026-11-25).
_COMPARISON_SETUP = {
    "attributes": {
        "title": "Net Sales floor u1",
        "state": "ACTIVE",
        "externalRecipients": [{"email": "ops@example.com"}],
        "metadata": {"visibleFilters": [{"localIdentifier": "genai_vf1", "title": "Product category"}]},
        "alert": {
            "execution": {
                "measures": [_NET_SALES],
                "filters": [
                    {
                        "positiveAttributeFilter": {
                            **_CATEGORY_FILTER["positiveAttributeFilter"],
                            "localIdentifier": "genai_vf1",
                        }
                    },
                    {"relativeDateFilter": {**_LAST_MONTH["relativeDateFilter"], "localIdentifier": "genai_vf2"}},
                ],
                "attributes": [],
            },
            "condition": {
                "comparison": {
                    "operator": "LESS_THAN",
                    "left": {"localIdentifier": "net_sales", "format": "$#,##0", "title": "Net Sales"},
                    "right": {"value": 50000.0},
                }
            },
            "trigger": "ALWAYS",
        },
    },
    "relationships": {"analyticalDashboard": {"data": {"id": "dash-overview", "type": "analyticalDashboard"}}},
}
_ANOMALY_SETUP = {
    "attributes": {
        "title": "Sales anomaly u4",
        "state": "ACTIVE",
        "alert": {
            "execution": {"measures": [_NET_SALES], "filters": [], "attributes": []},
            "condition": {
                "anomaly": {
                    "measure": {"localIdentifier": "net_sales", "format": "$#,##0", "title": "Net Sales"},
                    "sensitivity": "MEDIUM",
                    "granularity": "DAY",
                    "dataset": {"identifier": {"id": "date", "type": "dataset"}},
                }
            },
            "trigger": "ALWAYS",
        },
    },
}
_RELATIVE_SETUP = {
    "attributes": {
        "title": "Sales MoM r1",
        "alert": {
            "execution": {"measures": [_NET_SALES], "filters": [_LAST_MONTH], "attributes": []},
            "condition": {
                "relative": {
                    "operator": "INCREASES_BY",
                    "measure": {"operator": "CHANGE", "left": {"localIdentifier": "net_sales", "title": "Net Sales"}},
                    "threshold": {"value": 0.1},
                }
            },
            "trigger": "ALWAYS",
        },
    },
}


def _item(setup: dict, **change: object) -> dict:
    return {"Mode": "update", "Setup alert": setup, "Expected change": change}


def _stored(setup: dict, edit: Edit | None = None) -> dict:
    """The alert as the API returns it after the run created it, optionally changed by ``edit``."""
    entity = copy.deepcopy(setup)
    entity.setdefault("relationships", {})
    entity["attributes"]["createdAt"] = "2026-11-25 07:00"
    entity["attributes"]["description"] = "Alert when net_sales LESS_THAN 50000.0"
    entity["relationships"]["recipients"] = {"data": [{"id": "user-1", "type": "user"}]}
    entity["relationships"]["notificationChannel"] = {"data": {"id": "defaultSmtp", "type": "notificationChannel"}}
    if edit is not None:
        edit(entity)
        entity["attributes"]["modifiedAt"] = "2026-11-25 07:01"
    return entity


def _evaluate(
    item: dict, edit: Edit | EllipsisType | None, *, update_called: bool = True, alert_created: bool = False
) -> tuple[AlertUpdateEvaluation, list[dict]]:
    """Score ``edit`` applied to the setup alert; ``...`` means the alert no longer exists."""
    expectation = update_expectation(item)
    assert expectation is not None
    before = _stored(expectation.setup_alert)
    after = None if isinstance(edit, EllipsisType) else _stored(expectation.setup_alert, edit)
    return evaluate_update(
        expectation, before=before, after=after, update_called=update_called, alert_created=alert_created
    )


def _set(path: str, value: object) -> Edit:
    def edit(entity: dict) -> None:
        *parents, last = path.split(".")
        node = entity
        for key in parents:
            node = node[key] if not key.isdigit() else node[int(key)]
        node[last] = value

    return edit


# --- expectation ---------------------------------------------------------------------------------


def test_an_item_without_mode_is_not_an_update_item() -> None:
    assert update_expectation({"operator": "LESS_THAN", "threshold": 1}) is None


def test_the_expectation_reads_display_keys_aliases_and_display_values() -> None:
    expectation = update_expectation(
        {
            "mode": "Update",
            "setup_alert": _COMPARISON_SETUP,
            "expected_change": {"Trigger": "One time", "dashboard": "d2"},
        }
    )
    assert expectation is not None
    assert expectation.title == "Net Sales floor u1"
    assert expectation.condition_kind == "comparison"
    assert expectation.expected_change == {"trigger": "ONCE", "dashboard_id": "d2"}


def _without_title() -> dict:
    setup = copy.deepcopy(_COMPARISON_SETUP)
    del setup["attributes"]["title"]
    return setup


def _two_conditions() -> dict:
    setup = copy.deepcopy(_ANOMALY_SETUP)
    setup["attributes"]["alert"]["condition"]["comparison"] = {"operator": "LESS_THAN"}
    return setup


def _condition(condition: dict) -> dict:
    setup = copy.deepcopy(_COMPARISON_SETUP)
    setup["attributes"]["alert"]["condition"] = condition
    return setup


def _with_attributes(**attributes: object) -> dict:
    setup = copy.deepcopy(_COMPARISON_SETUP)
    setup["attributes"] = {**setup["attributes"], **attributes}
    return setup


@pytest.mark.parametrize(
    ("item", "message"),
    [
        ({"mode": "edit", "setup_alert": _COMPARISON_SETUP, "expected_change": {"threshold": 1}}, "mode must be"),
        ({**_item(_COMPARISON_SETUP, threshold=1), "Threshold": 1}, "takes only"),
        (_item(_COMPARISON_SETUP, cron="0 0 * * *"), "not a field update mode checks"),
        (_item(_COMPARISON_SETUP), "at least one field"),
        (_item(_ANOMALY_SETUP, threshold=1), "applies only to comparison and relative alerts"),
        (_item(_COMPARISON_SETUP, sensitivity="LOW"), "applies only to anomaly alerts"),
        (_item(_COMPARISON_SETUP, threshold="60k"), "must be a finite number"),
        (_item(_COMPARISON_SETUP, threshold=True), "must be a finite number"),
        (_item(_COMPARISON_SETUP, operator="INCREASES_BY"), "operator must be one of"),
        (_item(_COMPARISON_SETUP, trigger="WEEKLY"), "trigger must be one of"),
        (_item(_COMPARISON_SETUP, trigger_interval="WEEK"), "needs the ONCE_PER_INTERVAL trigger"),
        (_item(_COMPARISON_SETUP, filters={"positiveAttributeFilter": {}}), "list of non-empty filter objects"),
        (_item(_COMPARISON_SETUP, filters=[_LAST_MONTH, {}]), "list of non-empty filter objects"),
        (_item(_COMPARISON_SETUP, threshold=float("nan")), "must be a finite number"),
        (_item(_COMPARISON_SETUP, threshold=10**309), "must be a finite number"),
        ({"Mode": None, "Setup alert": _COMPARISON_SETUP, "Expected change": {"threshold": 1}}, "mode must be"),
        (_item(_COMPARISON_SETUP, title="A", name="B"), "names title twice"),
        ({"mode": "update", "expected_change": {"threshold": 1}}, "must be an automation entity object"),
        (_item(_without_title(), threshold=1), "title is required"),
        (_item(_two_conditions(), sensitivity="LOW"), "exactly one alert condition"),
        (_item({"attributes": _COMPARISON_SETUP["attributes"], "links": {}}, threshold=1), "only attributes and"),
        (_item(_condition({"comparision": {"operator": "LESS_THAN"}}), title="T"), "condition must be one of"),
        (_item(_condition({"comparison": "LESS_THAN 50000"}), title="T"), "comparison must be an object"),
        (_item(["not", "an", "entity"], title="T"), "must be an automation entity object"),
        (_item(_with_attributes(alert=None), title="T"), "attributes.alert is required"),
        (_item({**_COMPARISON_SETUP, "relationships": ["metrics"]}, title="T"), "relationships must be an object"),
        (_item({**_COMPARISON_SETUP, "relationships": []}, title="T"), "relationships must be an object"),
        (_item(_COMPARISON_SETUP, title=" "), "title must be a non-empty string"),
    ],
)
def test_a_malformed_update_item_raises_before_any_request(item: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        update_expectation(item)


def test_trigger_interval_is_accepted_together_with_the_once_per_interval_trigger() -> None:
    expectation = update_expectation(_item(_COMPARISON_SETUP, trigger="ONCE_PER_INTERVAL", trigger_interval="week"))
    assert expectation is not None
    assert expectation.expected_change == {"trigger": "ONCE_PER_INTERVAL", "trigger_interval": "WEEK"}


def test_the_setup_is_sent_to_the_current_user_over_the_org_channel_unless_the_item_names_them() -> None:
    expectation = update_expectation(_item(_COMPARISON_SETUP, threshold=60000))
    assert expectation is not None
    entity = setup_entity(expectation, current_user_id="user-1", channel_id="defaultSmtp")
    assert entity["relationships"]["recipients"] == {"data": [{"id": "user-1", "type": "user"}]}
    assert entity["relationships"]["notificationChannel"] == {
        "data": {"id": "defaultSmtp", "type": "notificationChannel"}
    }
    assert entity["relationships"]["analyticalDashboard"] == _COMPARISON_SETUP["relationships"]["analyticalDashboard"]

    named = copy.deepcopy(_COMPARISON_SETUP)
    named["relationships"]["recipients"] = {"data": [{"id": "someone", "type": "user"}]}
    named["relationships"]["notificationChannel"] = {"data": {"id": "smtp-2", "type": "notificationChannel"}}
    expectation = update_expectation(_item(named, threshold=60000))
    assert expectation is not None
    entity = setup_entity(expectation, current_user_id="user-1", channel_id="defaultSmtp")
    assert entity["relationships"]["recipients"]["data"][0]["id"] == "someone"
    assert entity["relationships"]["notificationChannel"]["data"]["id"] == "smtp-2"


# --- scoring -------------------------------------------------------------------------------------


def test_a_threshold_update_that_changes_only_the_threshold_passes() -> None:
    evaluation, changes = _evaluate(
        _item(_COMPARISON_SETUP, threshold=60000), _set("attributes.alert.condition.comparison.right.value", 60000.0)
    )
    assert evaluation.checks() == dict.fromkeys(evaluation.checks(), True)
    assert changes == []


def test_an_anomaly_update_that_wipes_the_metric_title_and_format_is_not_preserved() -> None:
    # GDAI-2894: update_metric_alert rebuilt the anomaly measure with an empty title and format.
    def wipe(entity: dict) -> None:
        anomaly = entity["attributes"]["alert"]["condition"]["anomaly"]
        anomaly["sensitivity"] = "LOW"
        anomaly["measure"].update(title="", format="")

    evaluation, changes = _evaluate(_item(_ANOMALY_SETUP, sensitivity="LOW"), wipe)
    assert evaluation.alert_update_correct is True
    assert evaluation.alert_update_preserved is False
    assert [c["path"] for c in changes] == [
        "attributes.alert.condition.anomaly.measure.format",
        "attributes.alert.condition.anomaly.measure.title",
    ]
    assert changes[1] == {
        "path": "attributes.alert.condition.anomaly.measure.title",
        "before": "Net Sales",
        "after": "",
    }


def test_a_filter_update_may_rewrite_the_filter_metadata_but_must_keep_the_other_filter() -> None:
    furniture = {
        "positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "in": {"values": ["Furniture"]}}
    }

    def swap(entity: dict) -> None:
        entity["attributes"]["alert"]["execution"]["filters"][0] = {
            "positiveAttributeFilter": {**furniture["positiveAttributeFilter"], "localIdentifier": "genai_vf1"}
        }
        entity["attributes"]["metadata"]["visibleFilters"][0]["title"] = "Category"
        entity["relationships"]["labels"] = {"data": [{"id": "product_category", "type": "label"}]}

    item = _item(_COMPARISON_SETUP, filters=[_LAST_MONTH, furniture])
    evaluation, changes = _evaluate(item, swap)
    assert evaluation.alert_update_correct is True
    assert evaluation.alert_update_preserved is True
    assert changes == []

    def drop_the_date(entity: dict) -> None:
        swap(entity)
        del entity["attributes"]["alert"]["execution"]["filters"][1]

    evaluation, _ = _evaluate(item, drop_the_date)
    assert evaluation.alert_update_correct is False


def test_the_selected_elements_of_a_filter_match_in_any_order() -> None:
    def both(values: list[str]) -> dict:
        return {"positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "in": {"values": values}}}

    item = _item(_COMPARISON_SETUP, filters=[both(["Clothing", "Furniture"]), _LAST_MONTH])
    stored = [{**both(["Furniture", "Clothing"]), "localIdentifier": "genai_vf1"}, _LAST_MONTH]
    evaluation, _ = _evaluate(item, _set("attributes.alert.execution.filters", stored))
    assert evaluation.alert_update_correct is True

    evaluation, _ = _evaluate(item, _set("attributes.alert.execution.filters", [both(["Furniture"]), _LAST_MONTH]))
    assert evaluation.alert_update_correct is False


def test_metadata_added_by_a_filter_update_is_compared_field_by_field() -> None:
    bare = copy.deepcopy(_COMPARISON_SETUP)
    del bare["attributes"]["metadata"]
    furniture = {
        "positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "in": {"values": ["Furniture"]}}
    }

    def with_metadata(widget: bool) -> Edit:
        def edit(entity: dict) -> None:
            entity["attributes"]["alert"]["execution"]["filters"] = [furniture, _LAST_MONTH]
            entity["attributes"]["metadata"] = {"visibleFilters": [{"localIdentifier": "genai_vf1"}]}
            if widget:
                entity["attributes"]["metadata"]["widget"] = "widget-net-sales"

        return edit

    item = _item(bare, filters=[furniture, _LAST_MONTH])
    evaluation, changes = _evaluate(item, with_metadata(widget=False))
    assert evaluation.strict_pass is True
    assert changes == []
    _, changes = _evaluate(item, with_metadata(widget=True))
    assert changes == [{"path": "attributes.metadata.widget", "before": None, "after": "widget-net-sales"}]


def test_other_lists_in_a_filter_keep_their_order_and_dropped_metadata_is_reported_by_field() -> None:
    top = {"rankingFilter": {"attributes": [{"localIdentifier": "a"}, {"localIdentifier": "b"}], "value": 3}}
    flipped = {"rankingFilter": {"attributes": [{"localIdentifier": "b"}, {"localIdentifier": "a"}], "value": 3}}
    item = _item(_COMPARISON_SETUP, filters=[top])
    evaluation, _ = _evaluate(item, _set("attributes.alert.execution.filters", [top]))
    assert evaluation.alert_update_correct is True
    evaluation, _ = _evaluate(item, _set("attributes.alert.execution.filters", [flipped]))
    assert evaluation.alert_update_correct is False

    def raise_and_drop_metadata(entity: dict) -> None:
        _RAISE(entity)
        entity["attributes"]["metadata"] = None

    _, changes = _evaluate(_item(_COMPARISON_SETUP, threshold=60000), raise_and_drop_metadata)
    assert [c["path"] for c in changes] == ["attributes.metadata.visibleFilters"]


def test_a_filter_update_does_not_own_the_widget_the_alert_was_set_on() -> None:
    def swap_and_drop_the_widget(entity: dict) -> None:
        entity["attributes"]["alert"]["execution"]["filters"][0]["positiveAttributeFilter"]["in"]["values"] = [
            "Furniture"
        ]
        entity["attributes"]["metadata"]["filters"] = ["genai_vf2"]
        del entity["attributes"]["metadata"]["widget"]

    furniture = {
        "positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "in": {"values": ["Furniture"]}}
    }
    setup = copy.deepcopy(_COMPARISON_SETUP)
    setup["attributes"]["metadata"]["widget"] = "widget-net-sales"
    evaluation, changes = _evaluate(_item(setup, filters=[furniture, _LAST_MONTH]), swap_and_drop_the_widget)
    assert evaluation.alert_update_correct is True
    assert evaluation.alert_update_preserved is False
    assert changes == [{"path": "attributes.metadata.widget", "before": "widget-net-sales", "after": None}]


def test_an_unasked_change_elsewhere_fails_preserved_but_bookkeeping_does_not() -> None:
    def also_move(entity: dict) -> None:
        entity["attributes"]["alert"]["condition"]["comparison"]["right"]["value"] = 60000
        entity["attributes"]["description"] = "Alert when net_sales LESS_THAN 60000"
        entity["relationships"]["analyticalDashboard"]["data"]["id"] = "dash-products"

    evaluation, changes = _evaluate(_item(_COMPARISON_SETUP, threshold=60000), also_move)
    assert evaluation.alert_update_correct is True
    assert evaluation.alert_update_preserved is False
    assert [c["path"] for c in changes] == ["relationships.analyticalDashboard.data.id"]


def test_a_trigger_change_may_clear_the_interval_and_a_relative_threshold_is_read_from_its_own_place() -> None:
    weekly = copy.deepcopy(_COMPARISON_SETUP)
    weekly["attributes"]["alert"].update(trigger="ONCE_PER_INTERVAL", interval="WEEK")

    def to_once(entity: dict) -> None:
        entity["attributes"]["alert"]["trigger"] = "ONCE"
        del entity["attributes"]["alert"]["interval"]

    evaluation, _ = _evaluate(_item(weekly, trigger="ONCE"), to_once)
    assert evaluation.strict_pass is True

    evaluation, _ = _evaluate(
        _item(_RELATIVE_SETUP, threshold=0.15), _set("attributes.alert.condition.relative.threshold.value", 0.15)
    )
    assert evaluation.strict_pass is True


def test_a_trigger_that_stays_once_per_interval_must_keep_the_interval() -> None:
    weekly = copy.deepcopy(_COMPARISON_SETUP)
    weekly["attributes"]["alert"].update(trigger="ONCE_PER_INTERVAL", interval="WEEK")
    evaluation, changes = _evaluate(
        _item(weekly, trigger="ONCE_PER_INTERVAL"), _set("attributes.alert.interval", "DAY")
    )
    assert evaluation.alert_update_preserved is False
    assert changes == [{"path": "attributes.alert.interval", "before": "WEEK", "after": "DAY"}]


def test_a_trigger_that_enters_once_per_interval_may_set_an_interval() -> None:
    def to_daily(entity: dict) -> None:
        entity["attributes"]["alert"].update(trigger="ONCE_PER_INTERVAL", interval="DAY")

    evaluation, _ = _evaluate(_item(_COMPARISON_SETUP, trigger="ONCE_PER_INTERVAL"), to_daily)
    assert evaluation.strict_pass is True


def test_an_operator_and_a_dashboard_change_are_read_from_the_stored_alert() -> None:
    def move(entity: dict) -> None:
        entity["attributes"]["alert"]["condition"]["comparison"]["operator"] = "LESS_THAN_OR_EQUAL_TO"
        entity["relationships"]["analyticalDashboard"]["data"]["id"] = "dash-products"

    item = _item(_COMPARISON_SETUP, operator="less_than_or_equal_to", dashboard="dash-products")
    evaluation, _ = _evaluate(item, move)
    assert evaluation.strict_pass is True

    def unlink(entity: dict) -> None:
        move(entity)
        entity["relationships"]["analyticalDashboard"] = "dash-products"

    evaluation, _ = _evaluate(item, unlink)
    assert evaluation.alert_update_correct is False


def test_a_filter_list_with_a_filter_nobody_asked_for_is_not_the_expected_one() -> None:
    def replace_the_date(entity: dict) -> None:
        entity["attributes"]["alert"]["execution"]["filters"][1] = {"relativeDateFilter": {"granularity": "YEAR"}}

    evaluation, _ = _evaluate(_item(_COMPARISON_SETUP, filters=[_CATEGORY_FILTER, _LAST_MONTH]), replace_the_date)
    assert evaluation.alert_update_correct is False


@pytest.mark.parametrize("stored_order", [("a", "b"), ("b", "a")])
def test_an_expected_filter_that_fits_several_stored_ones_does_not_take_the_one_another_needs(
    stored_order: tuple[str, str],
) -> None:
    def with_id(local_id: str) -> dict:
        return {"positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "localIdentifier": local_id}}

    stored = [with_id(f"genai_vf_{x}") for x in stored_order]
    item = _item(_COMPARISON_SETUP, filters=[_CATEGORY_FILTER, with_id("genai_vf_a")])
    evaluation, _ = _evaluate(item, _set("attributes.alert.execution.filters", stored))
    assert evaluation.alert_update_correct is True


def test_an_alert_that_no_longer_exists_fails_every_check_but_the_call() -> None:
    evaluation, changes = _evaluate(_item(_COMPARISON_SETUP, threshold=60000), ...)
    assert evaluation.checks() == {
        "alert_update_called": True,
        "alert_update_correct": False,
        "alert_update_preserved": False,
        "alert_not_recreated": False,
    }
    assert changes == []


def test_without_a_successful_update_call_only_that_check_is_named() -> None:
    evaluation, _ = _evaluate(_item(_COMPARISON_SETUP, threshold=60000), None, update_called=False)
    assert evaluation.alert_update_correct is False
    assert evaluation.alert_update_preserved is False
    run = MagicMock(eval=evaluation)
    assert _failed_checks(run) == [{"name": "alert_update_called"}]


def test_a_created_alert_fails_not_recreated() -> None:
    evaluation, _ = _evaluate(
        _item(_COMPARISON_SETUP, threshold=60000),
        _set("attributes.alert.condition.comparison.right.value", 60000),
        alert_created=True,
    )
    assert evaluation.alert_not_recreated is False


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ({"automation_id": "a1", "threshold": 1}, True),
        ({"automation_ids": ["a1"], "state": "pause"}, True),
        ({"automation_ids": "a1", "state": "pause"}, True),
        ({"automation_id": "a2"}, False),
        ({"automation_ids": ["a2"]}, False),
        ({"automation_ids": '["a0", "a1"]'}, True),
        ({"automation_ids": '["a2"]'}, False),
        ({"automation_ids": "[a1"}, False),
    ],
)
def test_an_update_call_targets_the_alert_by_id_or_id_list(args: dict, expected: bool) -> None:
    assert targets_alert(args, "a1") is expected


def _event(tool: str, arguments: str, result: str | None) -> ToolCallEvent:
    return ToolCallEvent.model_validate({"functionName": tool, "functionArguments": arguments, "result": result})


def test_an_update_call_without_object_arguments_or_without_a_result_is_not_a_successful_update() -> None:
    ok = '{"data": {"id": "a1"}}'
    events = [
        _event("update_metric_alert", '["a1"]', ok),
        _event("update_metric_alert", '{"automation_id": "a1", "threshold": 2}', None),
    ]
    args, updated = _update_calls(events, "a1")
    assert updated is False
    assert args == [
        {"tool": "update_metric_alert", "arguments": ["a1"]},
        {"tool": "update_metric_alert", "automation_id": "a1", "threshold": 2},
    ]
    _, updated = _update_calls([*events, _event("update_metric_alert", '{"automation_id": "a1"}', ok)], "a1")
    assert updated is True


def test_the_update_scores_are_conditional_scores() -> None:
    assert set(AlertUpdateEvaluation(True, True, True, True).checks()) <= set(ALERT_CONDITIONAL_SCORES)


# --- runner --------------------------------------------------------------------------------------


def _call(tool: str, args: dict, result: str | None = '{"data": {"id": "eval-1"}}') -> dict:
    return {"functionName": tool, "functionArguments": json.dumps(args), "result": result}


def _turn(*calls: dict, text: str = "Done.") -> ChatResult:
    return ChatResult.model_validate({"text_response": text, "toolCallEvents": list(calls)})


_STATE_ERROR = (
    '{"data": {"isError": true, "error": {"text": "1 validation error for ArrayParameter\\nvalue\\n  Value error"}}}'
)


def _fakes(
    item: dict,
    *turns: ChatResult | ChatError,
    edit: Edit | None = None,
    stale: tuple[str, ...] = (),
    readable: bool = True,
) -> tuple[MagicMock, MagicMock]:
    """A fake automation API holding the setup alert before the question and after it, and a chat client."""
    expectation = update_expectation(item)
    assert expectation is not None
    api = MagicMock()
    api.create.return_value = "eval-1"
    api.ids_titled.return_value = list(stale)
    api.first_channel_id.return_value = "defaultSmtp"
    before = _stored(expectation.setup_alert) if readable else None
    api.get.side_effect = [before, _stored(expectation.setup_alert, edit)]
    client = MagicMock()
    client.send_message.side_effect = list(turns)
    client.create_conversation.return_value = "conv-new"
    return api, client


def _run(
    item: dict,
    *turns: ChatResult | ChatError,
    edit: Edit | None = None,
    max_iterations: int = 3,
    stale: tuple[str, ...] = (),
    fakes: tuple[MagicMock, MagicMock] | None = None,
    conversation_id: str | None = "conv-1",
    sim_error: Exception | None = None,
    user_id: str | None = "user-1",
    delete_metric: MagicMock | None = None,
    automation_ids: list[set[str] | None] | None = None,
) -> tuple[AlertRunResult, MagicMock, MagicMock, MagicMock]:
    """Run an update item over these agent turns against a fake automation API.

    Returns the run, the fake API, the chat client mock and the simulated user mock.
    """
    api, client = fakes or _fakes(item, *turns, edit=edit, stale=stale)
    sim_reply = {"side_effect": sim_error} if sim_error else {"return_value": "Yes, please apply that change."}
    with (
        patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.alert_skill.AutomationApi", return_value=api),
        patch("gooddata_eval.core.agentic.alert_skill._resolve_current_user_id", return_value=user_id),
        patch("gooddata_eval.core.agentic.alert_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.alert_skill._delete_metric", delete_metric or MagicMock()),
        patch("gooddata_eval.core.agentic.alert_skill._automation_ids", side_effect=automation_ids or [None, None]),
        patch("gooddata_eval.core.agentic.alert_skill.generate_simulated_update_response", **sim_reply) as sim,
    ):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question='Raise the threshold of my "Net Sales floor u1" alert to $60,000.',
            expected_output=item,
            k=1,
            max_iterations=max_iterations,
            initial_conversation_id=conversation_id,
        )
    return summary.best, api, client, sim


_RAISE = _set("attributes.alert.condition.comparison.right.value", 60000.0)


def test_an_update_in_the_first_turn_is_scored_and_the_setup_alert_is_deleted() -> None:
    run, api, client, sim = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        _turn(
            _call("list_automations", {}), _call("update_metric_alert", {"automation_id": "eval-1", "threshold": 60000})
        ),
        edit=_RAISE,
        stale=("eval-update-left-over",),
    )
    assert run.eval.strict_pass is True
    assert run.exit_reason == LoopExit.SUCCESS
    assert run.actual_alert_arguments == {
        "update_calls": [{"tool": "update_metric_alert", "automation_id": "eval-1", "threshold": 60000}],
        "unexpected_changes": [],
    }
    created = api.create.call_args.args[0]
    assert created["relationships"]["recipients"] == {"data": [{"id": "user-1", "type": "user"}]}
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-update-left-over", "eval-1"]
    assert api.delete.call_args_list[0].kwargs == {"strict": True}
    assert client.send_message.call_count == 1
    sim.assert_not_called()


def test_a_failed_state_call_followed_by_a_retry_counts_as_called() -> None:
    def pause(entity: dict) -> None:
        entity["attributes"]["state"] = "PAUSED"

    run, _, client, sim = _run(
        _item(_COMPARISON_SETUP, state="PAUSED"),
        _turn(
            _call("update_alert_state", {"automation_ids": "eval-1", "state": "pause"}, _STATE_ERROR),
            text="The alert could not be paused. Should I try again?",
        ),
        _turn(
            _call(
                "update_alert_state",
                {"automation_ids": ["eval-1"], "state": "pause"},
                '{"data": {"paused_ids": ["eval-1"]}}',
            ),
        ),
        edit=pause,
    )
    # The failed call alone does not end the run as a success: the agent gets the next turn and retries.
    assert client.send_message.call_count == 2
    assert sim.call_count == 1
    assert run.eval.strict_pass is True


def test_the_simulated_user_confirms_and_the_update_in_the_next_turn_counts() -> None:
    run, _, client, sim = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        _turn(text="Should I raise the threshold of Net Sales floor u1 to 60,000?"),
        _turn(_call("update_metric_alert", {"automation_id": "eval-1", "threshold": 60000})),
        edit=_RAISE,
    )
    assert run.eval.strict_pass is True
    assert run.turns_used == 2
    assert sim.call_count == 1
    assert client.send_message.call_args_list[1].args == ("conv-1", "Yes, please apply that change.")


def test_a_new_alert_instead_of_an_update_fails_and_is_deleted_too() -> None:
    run, api, *_ = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        _turn(_call("create_metric_alert", {"operator": "LESS_THAN", "threshold": 60000}, '{"id": "new-alert"}')),
        max_iterations=1,
    )
    assert run.eval.alert_update_called is False
    assert run.eval.alert_not_recreated is False
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-1", "new-alert"]


# --- automation API ------------------------------------------------------------------------------


def _api(handler: Callable[[httpx.Request], httpx.Response]) -> AutomationApi:
    return AutomationApi("http://host/", "tok", "ws1", transport=httpx.MockTransport(handler))


def test_the_api_creates_the_setup_alert_under_a_fresh_id_and_reads_it_back() -> None:
    sent: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer tok"
        if request.method == "POST":
            sent.append(json.loads(request.content))
            return httpx.Response(201, json={})
        if request.url.path.endswith("/missing"):
            return httpx.Response(404)
        data = {"id": "x", "attributes": {"title": "T"}, "relationships": {"metrics": {}}, "links": {}}
        return httpx.Response(200, json={"data": data})

    api = _api(handler)
    alert_id = api.create({"attributes": {"title": "T"}, "relationships": {}})
    assert alert_id.startswith("eval-update-")
    assert sent == [{"data": {"id": alert_id, "type": "automation", "attributes": {"title": "T"}, "relationships": {}}}]
    assert api.get(alert_id) == {"attributes": {"title": "T"}, "relationships": {"metrics": {}}}
    assert api.get("missing") is None
    api.close()


def test_the_api_finds_alerts_by_title_across_pages_and_picks_the_lowest_channel_id() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if "notificationChannels" in request.url.path:
            return httpx.Response(200, json={"data": [{"id": "smtp-b"}, {"id": "smtp-a"}]})
        page = int(request.url.params["page"])
        titles = ["Other"] * 249 + ["T"] if page == 0 else ["T"]
        return httpx.Response(
            200, json={"data": [{"id": f"p{page}-{i}", "attributes": {"title": t}} for i, t in enumerate(titles)]}
        )

    api = _api(handler)
    assert api.ids_titled("T") == ["p0-249", "p1-0"]
    assert api.first_channel_id() == "smtp-a"


def test_the_lowest_channel_id_is_taken_across_pages() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params["page"])
        ids = [f"smtp-{i:03d}" for i in range(1, 251)] if page == 0 else ["smtp-000"]
        return httpx.Response(200, json={"data": [{"id": i} for i in ids]})

    assert _api(handler).first_channel_id() == "smtp-000"


def test_a_strict_delete_raises_a_failure_but_not_a_missing_alert() -> None:
    statuses = iter([404, 500])
    api = _api(lambda request: httpx.Response(next(statuses)))
    api.delete("gone", strict=True)
    with pytest.raises(httpx.HTTPStatusError):
        api.delete("broken", strict=True)


def test_a_delete_ignores_a_missing_alert_and_logs_a_failure(capsys: pytest.CaptureFixture[str]) -> None:
    statuses = iter([404, 500])
    api = _api(lambda request: httpx.Response(next(statuses)))
    api.delete("gone")
    api.delete("broken")
    assert "Failed to delete alert broken" in capsys.readouterr().out


def test_a_broken_stream_after_a_successful_update_still_scores_it() -> None:
    partial = _turn(_call("update_metric_alert", {"automation_id": "eval-1", "threshold": 60000}))
    run, api, *_ = _run(
        _item(_COMPARISON_SETUP, threshold=60000), ChatError("stream broke", partial_result=partial), edit=_RAISE
    )
    assert run.eval.strict_pass is True
    assert run.exit_reason != LoopExit.SUCCESS
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-1"]


def test_a_silent_turn_ends_the_run_without_asking_the_simulated_user() -> None:
    run, _, client, sim = _run(_item(_COMPARISON_SETUP, threshold=60000), _turn(text=""))
    assert run.exit_reason == LoopExit.AGENT_SILENT
    assert run.eval.alert_update_called is False
    assert client.send_message.call_count == 1
    sim.assert_not_called()


def test_a_run_in_its_own_conversation_deletes_it_and_the_metric_the_agent_created() -> None:
    delete_metric = MagicMock()
    run, _, client, _ = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        _turn(
            _call("create_metric", {"title": "Net Sales copy"}, '{"data": {"metric_id": "m-new"}}'),
            _call("update_metric_alert", {"automation_id": "eval-1", "threshold": 60000}),
        ),
        edit=_RAISE,
        conversation_id=None,
        delete_metric=delete_metric,
    )
    assert run.conversation_id == "conv-new"
    client.delete_conversation.assert_called_once_with("conv-new")
    assert delete_metric.call_args.args[1:] == ("ws1", "m-new")


def test_a_failed_simulated_reply_ends_only_that_run() -> None:
    run, *_ = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        _turn(text="Should I raise it to 60,000?"),
        sim_error=RuntimeError("openai down"),
    )
    assert run.exit_reason == LoopExit.SIMULATED_USER_FAILED
    assert run.eval.alert_update_called is False


def test_a_setup_alert_that_cannot_be_read_back_raises_and_is_deleted() -> None:
    item = _item(_COMPARISON_SETUP, threshold=60000)
    api, client = _fakes(item, readable=False)
    with pytest.raises(RuntimeError, match="cannot be read back"):
        _run(item, fakes=(api, client))
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-1"]
    client.close.assert_called_once()
    api.close.assert_called_once()


def test_an_update_item_needs_the_token_owner() -> None:
    with pytest.raises(RuntimeError, match="user id could not be resolved"):
        _run(_item(_COMPARISON_SETUP, threshold=60000), user_id=None)


def test_the_simulated_update_reply_asks_gpt_with_the_alert_title() -> None:
    expectation = update_expectation(_item(_COMPARISON_SETUP, threshold=60000))
    assert expectation is not None
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Yes, please apply that change."))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        reply = generate_simulated_update_response("Apply it?", expectation, [], "Raise it to 60,000.")
    assert reply == "Yes, please apply that change."
    prompt = fake_openai.return_value.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert prompt == update_sim_user_prompt("Raise it to 60,000.", "Net Sales floor u1")
    assert 'titled "Net Sales floor u1"' in prompt


def test_the_simulated_update_reply_needs_openai_and_its_key() -> None:
    expectation = update_expectation(_item(_COMPARISON_SETUP, threshold=60000))
    assert expectation is not None
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", None),
        pytest.raises(RuntimeError, match="openai package is required"),
    ):
        generate_simulated_update_response("Apply it?", expectation, [], "Raise it.")
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", MagicMock()),
        patch.dict("os.environ", {"OPENAI_API_KEY": ""}),
        pytest.raises(OSError, match="OPENAI_API_KEY"),
    ):
        generate_simulated_update_response("Apply it?", expectation, [], "Raise it.")


def test_a_failed_create_deletes_the_generated_id_and_raises_the_original_error() -> None:
    posted: list[str] = []
    deleted: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            posted.append(json.loads(request.content)["data"]["id"])
            return httpx.Response(502)
        deleted.append(request.url.path.rsplit("/", 1)[-1])
        return httpx.Response(500)

    api = _api(handler)
    # The cleanup DELETE fails too; the POST's error is the one raised.
    with pytest.raises(httpx.HTTPStatusError, match="502"):
        api.create({"attributes": {"title": "T"}, "relationships": {}})
    assert len(posted) == 1
    assert deleted == posted


def test_an_alert_created_without_a_result_in_a_broken_stream_is_found_by_its_named_id_and_deleted() -> None:
    partial = _turn(_call("create_metric_alert", {"automation_id": "net-sales-below", "threshold": 60000}, None))
    run, api, *_ = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        ChatError("stream broke", partial_result=partial),
        automation_ids=[{"other-alert"}, {"other-alert", "eval-1", "net-sales-below"}],
    )
    assert run.eval.alert_update_called is False
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-1", "net-sales-below"]


def test_a_named_id_is_not_deleted_without_a_listing_before_the_run() -> None:
    partial = _turn(_call("create_metric_alert", {"automation_id": "other-alert"}, None))
    _, api, *_ = _run(
        _item(_COMPARISON_SETUP, threshold=60000),
        ChatError("stream broke", partial_result=partial),
        automation_ids=[None, {"other-alert", "eval-1"}],
    )
    assert [c.args[0] for c in api.delete.call_args_list] == ["eval-1"]


@pytest.mark.parametrize(
    ("body", "call"),
    [
        (["not", "an", "object"], lambda api: api.get("eval-1")),
        ({"data": None}, lambda api: api.get("eval-1")),
        ({"data": {"id": "eval-1"}}, lambda api: api.ids_titled("T")),
        ({"data": [{"title": "no id"}]}, lambda api: api.first_channel_id()),
        ({"data": {"id": "eval-1", "attributes": ["bad"]}}, lambda api: api.get("eval-1")),
        ({"data": {"id": "eval-1", "attributes": {}, "relationships": ["bad"]}}, lambda api: api.get("eval-1")),
    ],
)
def test_a_malformed_api_response_raises_at_the_boundary(body: object, call: Callable[[AutomationApi], object]) -> None:
    api = _api(lambda request: httpx.Response(200, json=body))
    with pytest.raises(ValueError, match="JSON object|no data|no attributes"):
        call(api)


def test_a_same_titled_alert_no_evaluation_created_stops_the_item_without_deleting_it() -> None:
    item = _item(_COMPARISON_SETUP, threshold=60000)
    api, client = _fakes(item, stale=("users-own-alert", "eval-update-left-over"))
    with pytest.raises(RuntimeError, match="that no evaluation created: \\['users-own-alert'\\]"):
        _run(item, fakes=(api, client))
    api.delete.assert_not_called()
    api.create.assert_not_called()


def test_a_stale_setup_alert_that_cannot_be_deleted_stops_the_run_before_a_second_one_is_created() -> None:
    item = _item(_COMPARISON_SETUP, threshold=60000)
    api, client = _fakes(item, stale=("eval-update-left-over",))
    api.delete.side_effect = RuntimeError("500 Internal Server Error")
    with pytest.raises(RuntimeError, match="500"):
        _run(item, fakes=(api, client))
    api.create.assert_not_called()


def test_an_update_whose_result_is_not_an_object_is_not_a_successful_update() -> None:
    _, updated = _update_calls([_event("update_metric_alert", '{"automation_id": "a1"}', "false")], "a1")
    assert updated is False


def test_overlapping_filters_are_matched_without_trying_every_order() -> None:
    many = [
        {"positiveAttributeFilter": {**_CATEGORY_FILTER["positiveAttributeFilter"], "localIdentifier": f"vf{i}"}}
        for i in range(12)
    ]
    expected = [_CATEGORY_FILTER] * 11 + [_LAST_MONTH]
    evaluation, _ = _evaluate(
        _item(_COMPARISON_SETUP, filters=expected), _set("attributes.alert.execution.filters", many)
    )
    assert evaluation.alert_update_correct is False
