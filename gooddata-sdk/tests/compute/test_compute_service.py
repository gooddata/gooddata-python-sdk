# (C) 2025 GoodData Corporation
from pathlib import Path

from gooddata_sdk import CatalogWorkspace
from gooddata_sdk.sdk import GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


def _setup_test_workspace(sdk: GoodDataSdk, test_workspace_id: str, path: Path) -> None:
    """Helper function to set up test workspace with required models.

    Args:
        sdk: GoodData SDK instance
        test_workspace_id: ID of the test workspace
        path: Path to the directory containing model files
    """
    # Check if workspace already exists
    try:
        sdk.catalog_workspace.get_workspace(test_workspace_id)
    except Exception:
        workspace = CatalogWorkspace(workspace_id=test_workspace_id, name=test_workspace_id)
        sdk.catalog_workspace.create_or_update(workspace)

    # Load LDM from disk and put it to the workspace
    ldm_from_disk = sdk.catalog_workspace_content.load_ldm_from_disk(path)
    sdk.catalog_workspace_content.put_declarative_ldm(test_workspace_id, ldm_from_disk, standalone_copy=True)

    # Load Analytics Model from disk and put it to the workspace
    am_from_disk = sdk.catalog_workspace_content.load_analytics_model_from_disk(path)
    sdk.catalog_workspace_content.put_declarative_analytics_model(test_workspace_id, am_from_disk)


@gd_vcr.use_cassette(str(_fixtures_dir / "ai_search.yaml"))
def test_search_ai(test_config):
    """Test AI search with minimal required parameters."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai_search"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        result = sdk.compute.search_ai(test_workspace_id, "What is the total revenue?")
        assert len(result.results) == 3
    finally:
        # Clean up workspace and all related content
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "ai_search_full_params.yaml"))
def test_search_ai_full_params(test_config):
    """Test AI search with all available parameters."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai_search"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)

        # Test search_ai with all parameters
        result = sdk.compute.search_ai(
            workspace_id=test_workspace_id,
            question="What is the total revenue?",
            deep_search=True,
            limit=2,
            object_types=["metric", "attribute", "fact"],
            relevant_score_threshold=0.5,
            title_to_descriptor_ratio=0.7,
        )

        # Verify the results
        assert result is not None
        assert hasattr(result, "results")
        assert len(result.results) <= 2
    finally:
        # Clean up workspace and all related content
        sdk.catalog_workspace.delete_workspace(test_workspace_id)
