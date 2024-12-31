# (C) 2024 GoodData Corporation

import os
from pathlib import Path
from pprint import pprint

import gooddata_api_client
import pytest
from dotenv import load_dotenv
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.search_request import SearchRequest

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
    }


@pytest.fixture(scope="module")
def api_client(test_config):
    configuration = gooddata_api_client.Configuration(host=test_config["host"])
    api_client = gooddata_api_client.ApiClient(configuration)
    api_client.default_headers["Authorization"] = f"Bearer {test_config['token']}"
    return api_client


def test_smart_search_limit_set_to_1(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    search_request = SearchRequest(
        deep_search=False,
        limit=1,
        object_types=["metric", "visualization", "dashboard"],
        question="customer state",
        relevant_score_threshold=0.3,
        title_to_descriptor_ratio=0.7,
    )
    try:
        api_response = api_instance.ai_search(test_config["workspace_id"], search_request)
        pprint(api_response.to_dict())
        assert api_response["results"].__len__() == 1, "Response result should equal to 1"
        assert api_response["results"][0].title == "Customers by State", "Response title should be 'Customer by State'"
        assert api_response["results"][0].type == "visualization", "Response type should be 'visualization'"
        assert api_response["results"][0].score >= 0.7, "Response score should be greater than or equal to 0.7"
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_smart_search_limit_set_to_4(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    search_request = SearchRequest(
        deep_search=False,
        limit=4,
        object_types=["metric", "visualization", "dashboard"],
        question="Product category",
        relevant_score_threshold=0.3,
        title_to_descriptor_ratio=0.7,
    )
    try:
        api_response = api_instance.ai_search(test_config["workspace_id"], search_request)
        response_dict = api_response.to_dict()
        pprint(response_dict)

        results = response_dict.get("results", [])
        assert len(results) == 4, f"Expected 4 results, got {len(results)}"

        expected_results = [
            {
                "title": "Product Category Breakdown",
                "type": "visualization",
                "visualization_url": "local:pyramid",
                "score": 0.78567904,
            },
            {
                "title": "Product Category Rating",
                "type": "visualization",
                "visualization_url": "local:sankey",
                "score": 0.729191,
            },
            {
                "title": "Net Sales by Product Category",
                "type": "visualization",
                "visualization_url": "local:donut",
                "score": 0.5827423,
            },
            {
                "title": "Net Sales by Product Category (v2)",
                "type": "visualization",
                "visualization_url": "local:bar",
                "score": 0.52440727,
            },
        ]

        for actual, expected in zip(results, expected_results):
            assert (
                actual["title"] == expected["title"]
            ), f"Expected title '{expected['title']}', got '{actual['title']}'"
            assert actual["type"] == expected["type"], f"Expected type '{expected['type']}', got '{actual['type']}'"
            assert (
                actual["visualization_url"] == expected["visualization_url"]
            ), f"Expected visualization_url '{expected['visualization_url']}', got '{actual['visualization_url']}'"
            assert round(actual["score"]) >= round(
                expected["score"]
            ), f"Expected score >= {round(expected["score"])}, got {round(actual["score"])}"

        expected_relationships = [
            {
                "source_object_title": "1. Overview",
                "source_object_type": "dashboard",
                "target_object_title": "Net Sales by Product Category (v2)",
            },
            {
                "source_object_title": "4. Products",
                "source_object_type": "dashboard",
                "target_object_title": "Net Sales by Product Category (v2)",
            },
            {
                "source_object_title": "4. Products",
                "source_object_type": "dashboard",
                "target_object_title": "Product Category Breakdown",
            },
            {
                "source_object_title": "1. Overview",
                "source_object_type": "dashboard",
                "target_object_title": "Product Category Rating",
            },
        ]

        for actual, expected in zip(response_dict.get("relationships", []), expected_relationships):
            assert (
                actual["source_object_title"] == expected["source_object_title"]
            ), f"Expected source_object_title '{expected['source_object_title']}', got '{actual['source_object_title']}'"
            assert (
                actual["source_object_type"] == expected["source_object_type"]
            ), f"Expected source_object_type '{expected['source_object_type']}', got '{actual['source_object_type']}'"
            assert (
                actual["target_object_title"] == expected["target_object_title"]
            ), f"Expected target_object_title '{expected['target_object_title']}', got '{actual['target_object_title']}'"
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_smart_search_deep_search(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    search_request = SearchRequest(
        deep_search=True,
        limit=5,
        object_types=["metric", "visualization", "dashboard"],
        question="net sales over time",
        relevant_score_threshold=0.5,
        title_to_descriptor_ratio=0.7,
    )
    try:
        api_response = api_instance.ai_search(test_config["workspace_id"], search_request)
        pprint(api_response.to_dict())
        assert api_response["results"].__len__() == 5, "Response result should equal to 5"

        assert api_response["relationships"].__len__() == 25, "Response result should equal to 25"
    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_smart_search_attrbute_dataset(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    search_request = SearchRequest(
        deep_search=True,
        limit=5,
        object_types=["attribute", "dataset"],
        question="customer email",
        relevant_score_threshold=0.5,
        title_to_descriptor_ratio=0.7,
    )
    try:
        api_response = api_instance.ai_search(test_config["workspace_id"], search_request)
        pprint(api_response.to_dict())
        results = api_response.to_dict().get("results", [])
        assert api_response["results"].__len__() == 5, "Response result should equal to 5"

        assert api_response["relationships"].__len__() == 5, "Response result should equal to 5"

        expected_results = [
            {
                "title": "Customer email",
                "tags": ["Customer"],
                "type": "attribute",
                "score": 1.0,
                "workspace_id": test_config["workspace_id"],
            },
            {
                "title": "Customer",
                "tags": ["Customer"],
                "type": "dataset",
                "score": 0.6708147,
                "workspace_id": test_config["workspace_id"],
            },
            {
                "title": "Customer id",
                "tags": ["Customer"],
                "type": "attribute",
                "score": 0.64592105,
                "workspace_id": test_config["workspace_id"],
            },
            {
                "title": "Customer country",
                "tags": ["Customer"],
                "type": "attribute",
                "score": 0.5076896,
                "workspace_id": test_config["workspace_id"],
            },
            {
                "title": "Customer state",
                "tags": ["Customer"],
                "type": "attribute",
                "score": 0.506533,
                "workspace_id": test_config["workspace_id"],
            },
        ]

        for actual, expected in zip(results, expected_results):
            assert (
                actual["title"] == expected["title"]
            ), f"Expected title '{expected['title']}', got '{actual['title']}'"
            assert actual["tags"] == expected["tags"], f"Expected tags '{expected['tags']}', got '{actual['tags']}'"
            assert actual["type"] == expected["type"], f"Expected type '{expected['type']}', got '{actual['type']}'"
            assert round(actual["score"]) >= round(
                expected["score"]
            ), f"Expected score >= {round(expected["score"])}, got {round(actual["score"])}"
            assert (
                actual["workspace_id"] == expected["workspace_id"]
            ), f"Expected workspace_id '{expected['workspace_id']}', got '{actual['workspace_id']}'"

    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_smart_search_label_and_date(api_client, test_config):
    api_instance = smart_functions_api.SmartFunctionsApi(api_client)
    search_request = SearchRequest(
        deep_search=True,
        limit=2,
        object_types=["label", "date"],
        question="Inventory month",
        relevant_score_threshold=0.7,
        title_to_descriptor_ratio=0.7,
    )
    try:
        api_response = api_instance.ai_search(test_config["workspace_id"], search_request)
        pprint(api_response.to_dict())
        results = api_response.to_dict().get("results", [])
        assert api_response["results"].__len__() == 2, "Response result should equal to 2"

        assert api_response["relationships"].__len__() == 0, "There is no relationship"

        expected_results = [
            {
                "title": "Inventory month",
                "tags": ["Inventory month"],
                "type": "date",
                "score": 1.0,
                "workspace_id": test_config["workspace_id"],
            },
            {
                "title": "Inventory month - Year",
                "tags": ["Inventory month"],
                "type": "label",
                "score": 0.935153,
                "workspace_id": test_config["workspace_id"],
            },
        ]

        for actual, expected in zip(results, expected_results):
            assert (
                actual["title"] == expected["title"]
            ), f"Expected title '{expected['title']}', got '{actual['title']}'"
            assert actual["tags"] == expected["tags"], f"Expected tags '{expected['tags']}', got '{actual['tags']}'"
            assert actual["type"] == expected["type"], f"Expected type '{expected['type']}', got '{actual['type']}'"
            assert round(actual["score"]) >= round(
                expected["score"]
            ), f"Expected score >= {round(expected["score"])}, got {round(actual["score"])}"
            assert (
                actual["workspace_id"] == expected["workspace_id"]
            ), f"Expected workspace_id '{expected['workspace_id']}', got '{actual['workspace_id']}'"

    except gooddata_api_client.ApiException as e:
        pytest.fail(f"API exception: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    pytest.main(["-s", __file__])
