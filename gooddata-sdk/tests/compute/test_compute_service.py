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
    path = _current_dir / "load" / "ai"
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
    path = _current_dir / "load" / "ai"
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


@gd_vcr.use_cassette(str(_fixtures_dir / "ai_chat.yaml"))
def test_ai_chat(test_config):
    """Test AI chat with minimal required parameters."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        response = sdk.compute.ai_chat(test_workspace_id, "Create a visualization for total revenue")
        assert hasattr(response, "routing")
        assert hasattr(response, "created_visualizations")
        assert hasattr(response, "chat_history_interaction_id")
        assert response.chat_history_interaction_id is not None
    finally:
        # Clean up workspace and all related content
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "get_ai_chat_history.yaml"))
def test_get_ai_chat_history(test_config):
    """Test get AI chat history."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        first_question = "Create a visualization for total revenue"
        second_question = "Switch to a table"
        sdk.compute.ai_chat(test_workspace_id, first_question)
        sdk.compute.ai_chat(test_workspace_id, second_question)
        response = sdk.compute.get_ai_chat_history(test_workspace_id)
        assert hasattr(response, "interactions")
        assert len(response.interactions) == 2
        assert response.interactions[0]["question"] == first_question
        assert response.interactions[1]["question"] == second_question

    finally:
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "set_ai_chat_history_feedback.yaml"))
def test_set_ai_chat_history_feedback(test_config):
    """Test set AI chat history feedback."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        chat_response = sdk.compute.ai_chat(test_workspace_id, "Create a visualization for total revenue")
        sdk.compute.set_ai_chat_history_feedback(
            test_workspace_id, "POSITIVE", chat_response.chat_history_interaction_id
        )
        response = sdk.compute.get_ai_chat_history(test_workspace_id)
        assert response.interactions[0]["userFeedback"] == "POSITIVE"
    finally:
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "reset_ai_chat_history.yaml"))
def test_reset_ai_chat_history(test_config):
    """Test reset AI chat history."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        sdk.compute.ai_chat(test_workspace_id, "Create a visualization for total revenue")
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        response = sdk.compute.get_ai_chat_history(test_workspace_id)
        assert len(response.interactions) == 0
    finally:
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "ai_chat_stream.yaml"))
def test_ai_chat_stream(test_config):
    """Test AI chat stream.

    vcrpy is not able to record streaming responses properly, so we don't have a proper test for this.
    """
    path = _current_dir / "load" / "ai"
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    test_workspace_id = test_config["workspace_test"]

    question = "What is the total revenue for the year 2024?"
    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        buffer = {}
        for chunk in sdk.compute.ai_chat_stream(test_workspace_id, question):
            buffer = {**buffer, **chunk}
        assert buffer is not None
    finally:
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)


@gd_vcr.use_cassette(str(_fixtures_dir / "build_exec_def_from_chat_result.yaml"))
def test_build_exec_def_from_chat_result(test_config):
    """Test build execution definition from chat result."""
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    path = _current_dir / "load" / "ai"
    test_workspace_id = test_config["workspace_test"]

    try:
        _setup_test_workspace(sdk, test_workspace_id, path)
        response = sdk.compute.ai_chat(test_workspace_id, "Display the revenue by product")
        execution_definition = sdk.compute.build_exec_def_from_chat_result(response)
        assert execution_definition is not None

        execution = sdk.compute.for_exec_def(test_workspace_id, execution_definition)
        assert execution.result_id is not None

    finally:
        sdk.compute.reset_ai_chat_history(test_workspace_id)
        sdk.catalog_workspace.delete_workspace(test_workspace_id)
