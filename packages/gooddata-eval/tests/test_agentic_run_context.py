# (C) 2026 GoodData Corporation
from gooddata_eval.core.agentic._langfuse import build_run_context

# model_version_override short-circuits get_model_version (no workspace API call).
_COMMON = {
    "host": "h",
    "token": "t",
    "workspace_id": "w",
    "dataset_name": "ds",
    "run_timestamp": "2026-07-10_00-00-00",
    "model_version_override": "m",
}


def test_build_run_context_includes_caller_extra_keys():
    base, metadata = build_run_context(
        **_COMMON, run_metadata_extra={"testing_framework": "tavern-e2e", "github_run_id": "run-123"}
    )
    assert base == "ds_2026-07-10_00-00-00_m"
    assert metadata["testing_framework"] == "tavern-e2e"
    assert metadata["github_run_id"] == "run-123"
    assert metadata["model_version"] == "m"


def test_build_run_context_extra_cannot_override_model_version():
    _, metadata = build_run_context(**_COMMON, run_metadata_extra={"model_version": "hack"})
    assert metadata["model_version"] == "m"  # SDK-derived value wins


def test_build_run_context_without_extra_has_only_model_version():
    _, metadata = build_run_context(**_COMMON)
    assert metadata == {"model_version": "m"}
