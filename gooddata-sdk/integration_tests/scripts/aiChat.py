# (C) 2024 GoodData Corporation

import os
import sys
from pprint import pprint

import gooddata_api_client
import pytest
from gooddata_api_client.api import smart_functions_api
from gooddata_api_client.model.chat_history_request import ChatHistoryRequest
from gooddata_api_client.model.chat_history_result import ChatHistoryResult
from gooddata_api_client.model.chat_request import ChatRequest
from gooddata_api_client.model.chat_result import ChatResult

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import HOST, TOKEN, WORKSPACE_ID


@pytest.fixture(scope="module")
def api_client():
    configuration = gooddata_api_client.Configuration(host=HOST)
    configuration.access_token = TOKEN
    with gooddata_api_client.ApiClient(configuration) as api_client:
        yield api_client


class GoodDataAiChatApp:
    def __init__(self, api_client, workspace_id):
        self.api_instance = smart_functions_api.SmartFunctionsApi(api_client)
        self.workspace_id = workspace_id

    async def ask_question(self, question: str):
        chat_request = ChatRequest(question=question)
        return self.api_instance.ai_chat(self.workspace_id, chat_request)

    async def chat_history(self, chat_history_interaction_id: int, user_feedback: str):
        chat_history_request = ChatHistoryRequest(
            chat_history_interaction_id=chat_history_interaction_id,
            user_feedback=user_feedback,
        )
        return self.api_instance.ai_chat_history(self.workspace_id, chat_history_request)


def set_authorization_header(api_client, token):
    api_client.default_headers["Authorization"] = f"Bearer {token}"


def handle_api_response(api_response):
    # Print the raw response
    pprint(api_response.to_dict())
    # Assert that the response is not empty
    assert api_response.routing is not None, "Routing should not be None"
    assert api_response.created_visualizations is not None, "createdVisualizations should not be None"
    assert api_response.found_objects is not None, "foundObjects should not be None"
    assert isinstance(api_response, ChatResult), "Response is not of type ChatResult"


@pytest.fixture(scope="module")
def app(api_client):
    # Initialize the GoodDataAiChatApp class
    app = GoodDataAiChatApp(api_client, WORKSPACE_ID)
    # Set the Authorization header
    set_authorization_header(api_client, TOKEN)
    return app


@pytest.mark.asyncio
async def test_ai_chat(app):
    question = "generate HEADLINE showing Sum of Amount"

    try:
        api_response = await app.ask_question(question)
        handle_api_response(api_response)
    except gooddata_api_client.ApiException as e:
        print(f"Exception when calling SmartFunctionsApi->ai_chat: {e}")
        pytest.fail(f"Exception when calling SmartFunctionsApi->ai_chat: {e}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pytest.fail(f"An unexpected error occurred: {e}\n")


@pytest.mark.asyncio
async def test_ai_chat_history(app):
    try:
        api_response = await app.chat_history(1260, "POSITIVE")
        pprint(api_response.to_dict())
        assert isinstance(api_response, ChatHistoryResult), "Response is not of type ChatHistoryResult"
    except gooddata_api_client.ApiException as e:
        print(f"Exception when calling SmartFunctionsApi->ai_chat_history: {e}")
        pytest.fail(f"Exception when calling SmartFunctionsApi->ai_chat_history: {e}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        pytest.fail(f"An unexpected error occurred: {e}\n")


if __name__ == "__main__":
    pytest.main()
