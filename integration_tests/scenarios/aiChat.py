# (C) 2024 GoodData Corporation
import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv
from gooddata_sdk import GoodDataSdk

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)

# Load environment variables from the .env file
load_dotenv()

# Create the test_config dictionary with the loaded environment variables
test_config = {"host": os.getenv("HOST"), "token": os.getenv("TOKEN")}
workspace_id = os.getenv("WORKSPACE_ID")

questions = ["What is number of order line id ?"]
sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])


def test_reset_chat_history():
    sdk.compute.ai_chat_history_reset(workspace_id)


@pytest.mark.parametrize("question", questions)
def test_ask_ai(question):
    chat_ai_res = sdk.compute.ai_chat(workspace_id, question=question)
    pprint(chat_ai_res.to_dict())
    assert chat_ai_res["created_visualizations"] is not None, "Created visualizations should not be None"
    assert chat_ai_res["routing"] is not None, "Routing should not be None"


def test_ai_chat_history():
    chat_ai_res = sdk.compute.ai_chat(workspace_id, question="show me a headline generating net sales and net order")
    chat_ai_res.to_dict()
    chat_history_interaction_id = chat_ai_res["chat_history_interaction_id"]
    pprint(chat_history_interaction_id)
    chat_history_res = sdk.compute.ai_chat_history(workspace_id, chat_history_interaction_id)
    sdk.compute.ai_chat_history_user_feedback(workspace_id, chat_history_interaction_id, "POSITIVE")
    pprint(chat_history_res.to_dict())


def test_get_chat_history():
    chat_history_res = sdk.compute.ai_chat_history(workspace_id)
    pprint(chat_history_res.to_dict())
    assert chat_history_res["interactions"] is not None, "Interactions should not be None"
    assert (
        chat_history_res["interactions"][0]["question"] == "What is number of order line id ?"
    ), "First interaction question should match"


if __name__ == "__main__":
    pytest.main()
