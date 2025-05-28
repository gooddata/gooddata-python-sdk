# (C) 2025 GoodData Corporation
from pathlib import Path

from gooddata_pandas import DataFrameFactory
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


@gd_vcr.use_cassette(str(_fixtures_dir / "dataframe_for_created_visualization.yaml"))
def test_dataframe_for_created_visualization(test_config):
    # To recreate the cassette, a complete local GoodData environment with gen_ai service is required.
    # The gen_ai service cannot be included in the already available single docker image due to size constraints.
    # Since in such cases we are interacting with an LLM, the results are not 100% deterministic.

    # Get SDK instance and create test workspace
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    gdf = DataFrameFactory(sdk, test_config["workspace_test"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        response = sdk.compute.ai_chat(test_workspace_id, "Display the revenue by product")

        df, df_metadata = gdf.for_created_visualization(response)

        assert len(df.columns) == 1
        assert len(df) == 18
        assert df.columns[0] == ("Revenue",)
        assert df.index.names[0] == "Product name"

    finally:
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)
