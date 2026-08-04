# (C) 2026 GoodData Corporation
import pytest
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


def test_build_run_context_without_effort_is_unchanged():
    """Runs that do not request an effort keep their existing name and metadata."""
    base, metadata = build_run_context(**_COMMON)
    assert base == "ds_2026-07-10_00-00-00_m"
    assert "reasoning_effort" not in metadata


def test_build_run_context_effort_suffixes_the_run_name():
    """Two runs differing only by effort must not share a name, or the report merges them."""
    low, low_metadata = build_run_context(**_COMMON, reasoning_effort="LOW")
    medium, _ = build_run_context(**_COMMON, reasoning_effort="MEDIUM")
    assert low == "ds_2026-07-10_00-00-00_m_effort-low"
    assert low != medium
    assert low_metadata["reasoning_effort"] == "LOW"


def test_build_run_context_effort_does_not_displace_model_version():
    _, metadata = build_run_context(**_COMMON, reasoning_effort="HIGH")
    assert metadata["model_version"] == "m"
    assert metadata["reasoning_effort"] == "HIGH"


def test_build_run_context_normalizes_effort_casing():
    """Name suffix and metadata must agree with the canonical value that was sent."""
    base, metadata = build_run_context(**_COMMON, reasoning_effort="low")
    assert base.endswith("_effort-low")
    assert metadata["reasoning_effort"] == "LOW"


def test_build_run_context_blank_effort_is_unset():
    base, metadata = build_run_context(**_COMMON, reasoning_effort="  ")
    assert base == "ds_2026-07-10_00-00-00_m"
    assert "reasoning_effort" not in metadata


def test_build_run_context_rejects_invalid_effort():
    with pytest.raises(ValueError, match="Invalid reasoning effort"):
        build_run_context(**_COMMON, reasoning_effort="turbo")
