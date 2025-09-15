# (C) 2024 GoodData Corporation

import os
import sys
import time
import uuid
from pprint import pprint

import gooddata_api_client
import pytest
from dotenv import load_dotenv
from gooddata_api_client.api import llm_endpoints_api, metadata_sync_api, workspaces_entity_apis_api
from gooddata_api_client.model.json_api_llm_endpoint_in import JsonApiLlmEndpointIn
from gooddata_api_client.model.json_api_llm_endpoint_in_attributes import JsonApiLlmEndpointInAttributes
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_api_client.model.json_api_workspace_patch import JsonApiWorkspacePatch
from gooddata_api_client.model.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)

# Load environment variables from the .env file
load_dotenv()


@pytest.fixture(scope="module")
def test_config():
    return {
        "host": os.getenv("HOST"),
        "token": os.getenv("TOKEN"),
        "workspace_id": os.getenv("WORKSPACE_ID"),
        "llm_token": os.getenv("LLM_TOKEN"),
    }


@pytest.fixture(scope="module")
def api_client(test_config):
    configuration = gooddata_api_client.Configuration(host=test_config["host"])
    api_client = gooddata_api_client.ApiClient(configuration)
    api_client.default_headers["Authorization"] = f"Bearer {test_config['token']}"
    return api_client


def test_create_llm_endpoint(api_client, test_config):
    llm_title = f"python_sdk_test_{int(time.time())}"
    api_instance = llm_endpoints_api.LLMEndpointsApi(api_client)
    json_api_llm_endpoint_in_document = JsonApiLlmEndpointInDocument(
        data=JsonApiLlmEndpointIn(
            attributes=JsonApiLlmEndpointInAttributes(
                llm_model="gpt-4o",
                provider="OPENAI",
                title=llm_title,
                token=test_config["llm_token"],
                workspaceIds=[test_config["workspace_id"]],
            ),
            id=uuid.uuid4().hex,
            type="llmEndpoint",
        ),
    )
    try:
        # Post LLM endpoint entities
        api_response = api_instance.create_entity_llm_endpoints(json_api_llm_endpoint_in_document)
        pprint(api_response)
        assert api_response is not None, "API response should not be None"
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def enable_early_access_per_workspace(api_client, test_config, feature_flag_name):
    api_instance = workspaces_entity_apis_api.WorkspacesEntityAPIsApi(api_client)
    json_api_entities_workspace = api_instance.get_entity_workspaces(test_config["workspace_id"])

    current_early_access_values = json_api_entities_workspace.data.attributes.early_access_values or []
    updated_early_access_values = list(set(current_early_access_values + [feature_flag_name]))

    json_api_workspace_patch_document = JsonApiWorkspacePatchDocument(
        data=JsonApiWorkspacePatch(
            attributes=JsonApiWorkspaceInAttributes(early_access_values=updated_early_access_values),
            id=test_config["workspace_id"],
            type="workspace",
        )
    )
    try:
        print("Attempting to enable early access feature flag...")
        print("workspace_id", test_config["workspace_id"])

        api_response = api_instance.patch_entity_workspaces(
            test_config["workspace_id"], json_api_workspace_patch_document
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_enable_gen_ai_per_workspace(api_client, test_config):
    enable_early_access_per_workspace(api_client, test_config, "experimental-genai-chat")


def test_enable_smart_search_per_workspace(api_client, test_config):
    enable_early_access_per_workspace(api_client, test_config, "experimental-semantic-search")


def test_metadata_sync(api_client, test_config):
    api_instance = metadata_sync_api.MetadataSyncApi(api_client)
    try:
        print("Attempting to sync metadata...")
        print("workspace_id", test_config["workspace_id"])

        api_instance.metadata_sync(test_config["workspace_id"])
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    pytest.main(["-s", __file__])
