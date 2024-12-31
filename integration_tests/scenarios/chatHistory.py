# (C) 2024 GoodData Corporation

import os
from pathlib import Path
from pprint import pprint

import gooddata_api_client
import pytest
from dotenv import load_dotenv
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_request import ChatRequest

from integration_tests.scenarios.utils import compare_and_print_diff, load_json, normalize_metrics

_current_dir = Path(__file__).parent.absolute()
parent_dir = _current_dir.parent
expected_object_dir = parent_dir / "expected"
questions_list_dir = parent_dir / "fixtures" / "ai_questions.json"

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


def validate_response(actual_response, expected_response):
    actual_metrics = normalize_metrics(
        actual_response["created_visualizations"]["objects"][0]["metrics"], exclude_keys=["title"]
    )
    expected_metrics = normalize_metrics(expected_response["metrics"], exclude_keys=["title"])
    compare_and_print_diff(actual_metrics, expected_metrics, "Metrics")
    actual_visualization_type = actual_response["created_visualizations"]["objects"][0]["visualization_type"]
    expected_visualization_type = expected_response["visualizationType"]
    compare_and_print_diff(actual_visualization_type, expected_visualization_type, "Visualization type")
    actual_dimensionality = actual_response["created_visualizations"]["objects"][0]["dimensionality"]
    expected_dimensionality = expected_response["dimensionality"]
    compare_and_print_diff(actual_dimensionality, expected_dimensionality, "Dimensionality")
    actual_filters = actual_response["created_visualizations"]["objects"][0]["filters"]
    expected_filters = expected_response["filters"]
    compare_and_print_diff(actual_filters, expected_filters, "Filters")


def test_ai_chat_history_reset(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    chat_history_request = ChatHistoryRequest(reset=True)
    try:
        api_response = api_instance.ai_chat_history(test_config["workspace_id"], chat_history_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


questions_list = load_json(questions_list_dir)


@pytest.mark.parametrize(
    "question, expected_file",
    [(item["question"], item["expected_objects_file"]) for item in questions_list],
    ids=[item["question"] for item in questions_list],
)
def test_ai_chat(api_client, test_config, question, expected_file):
    expected_objects = load_json(os.path.join(expected_object_dir, expected_file))
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    try:
        api_response = api_instance.ai_chat(test_config["workspace_id"], ChatRequest(question=question))
        print("\napi_response", api_response.created_visualizations.objects[0])
        print("\nexpected_file", expected_objects)

        validate_response(api_response.to_dict(), expected_objects)

    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    pytest.main(["-s", __file__])
