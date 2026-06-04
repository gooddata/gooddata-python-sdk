# (C) 2026 GoodData Corporation
from unittest.mock import MagicMock

import pytest
from gooddata_eval.core.workspace import (
    ActiveLlmProvider,
    ModelResolutionError,
    WorkspaceModelController,
    _resolve_provider_ref,
    active_provider_content,
    resolve_model,
    select_provider_and_model,
)


def test_active_provider_content_shape():
    assert active_provider_content("prov_1", "gpt-5.2") == {
        "id": "prov_1",
        "type": "llmProvider",
        "defaultModelId": "gpt-5.2",
    }


def test_resolve_model_defaults_to_workspace_model():
    active = ActiveLlmProvider(provider_id="prov_1", default_model_id="gpt-5.2")
    assert resolve_model(requested=None, active=active) == ("prov_1", "gpt-5.2")


def test_resolve_model_uses_requested_with_existing_provider():
    active = ActiveLlmProvider(provider_id="prov_1", default_model_id="gpt-5.2")
    assert resolve_model(requested="gpt-4o", active=active) == ("prov_1", "gpt-4o")


def test_resolve_model_raises_when_no_active_provider():
    with pytest.raises(ModelResolutionError):
        resolve_model(requested=None, active=None)


_MAP = {"prov_1": ["gpt-5.2"], "prov_2": ["gpt-5.4-mini"]}


def test_select_prefers_active_provider_when_it_offers_model():
    active = ActiveLlmProvider("prov_1", "gpt-5.2")
    assert select_provider_and_model("gpt-5.2", None, active, _MAP) == ("prov_1", "gpt-5.2")


def test_select_switches_to_only_provider_that_offers_model():
    active = ActiveLlmProvider("prov_1", "gpt-5.2")
    assert select_provider_and_model("gpt-5.4-mini", None, active, _MAP) == ("prov_2", "gpt-5.4-mini")


def test_select_raises_when_model_on_multiple_providers():
    with pytest.raises(ModelResolutionError, match="multiple providers"):
        select_provider_and_model("m", None, None, {"a": ["m"], "b": ["m"]})


def test_select_raises_when_model_unknown_everywhere():
    active = ActiveLlmProvider("prov_1", "gpt-5.2")
    with pytest.raises(ModelResolutionError, match="not offered by any"):
        select_provider_and_model("gpt-9", None, active, _MAP)


def test_select_explicit_provider_validates_model():
    with pytest.raises(ModelResolutionError, match="not offered by provider"):
        select_provider_and_model("gpt-5.2", "prov_2", None, _MAP)


def test_select_explicit_provider_ok():
    assert select_provider_and_model("gpt-5.4-mini", "prov_2", None, _MAP) == ("prov_2", "gpt-5.4-mini")


def test_select_unknown_provider_raises():
    with pytest.raises(ModelResolutionError, match="not found"):
        select_provider_and_model("gpt-5.2", "ghost", None, _MAP)


def test_select_default_uses_active_when_no_model_or_provider():
    active = ActiveLlmProvider("prov_1", "gpt-5.2")
    assert select_provider_and_model(None, None, active, {}) == ("prov_1", "gpt-5.2")


_INFO = {
    "prov_1": {"name": "OpenAI Provider", "models": ["gpt-5.2"]},
    "prov_2": {"name": "Azure Provider", "models": ["gpt-5.4-mini"]},
}


def test_resolve_provider_ref_by_exact_id():
    assert _resolve_provider_ref("prov_1", _INFO) == "prov_1"


def test_resolve_provider_ref_by_exact_name():
    assert _resolve_provider_ref("OpenAI Provider", _INFO) == "prov_1"


def test_resolve_provider_ref_by_name_case_insensitive():
    assert _resolve_provider_ref("openai provider", _INFO) == "prov_1"


def test_resolve_provider_ref_not_found_shows_names():
    with pytest.raises(ModelResolutionError, match="OpenAI Provider"):
        _resolve_provider_ref("ghost", _INFO)


def test_resolve_provider_ref_ambiguous_name():
    info = {
        "p1": {"name": "Shared Name", "models": []},
        "p2": {"name": "Shared Name", "models": []},
    }
    with pytest.raises(ModelResolutionError, match="Multiple"):
        _resolve_provider_ref("Shared Name", info)


def test_workspace_controller_restore_calls_activate():
    ctrl = WorkspaceModelController.__new__(WorkspaceModelController)
    ctrl._workspace_id = "ws"
    ctrl._host = "https://h"
    ctrl._headers = {}
    ctrl._sdk = MagicMock()

    activated = []
    ctrl.activate = lambda pid, mid: activated.append((pid, mid))

    original = ActiveLlmProvider(provider_id="orig-prov", default_model_id="gpt-5.2")
    ctrl.restore(original)
    assert activated == [("orig-prov", "gpt-5.2")]


def test_workspace_controller_restore_skips_when_none():
    ctrl = WorkspaceModelController.__new__(WorkspaceModelController)
    activated = []
    ctrl.activate = lambda pid, mid: activated.append((pid, mid))
    ctrl.restore(None)
    assert activated == []
