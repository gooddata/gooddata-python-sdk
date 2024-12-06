# (C) 2024 GoodData Corporation
import os
import sys

import pytest

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import HOST, TOKEN, WORKSPACE_ID
from gooddata_sdk import GoodDataSdk


@pytest.fixture
def test_config():
    return {"host": HOST, "token": TOKEN, "workspace_id": WORKSPACE_ID}


questions = [
    "What is the number of Accounts?",
    "What is the total of Amount?",
]


@pytest.mark.parametrize("question", questions)
def test_ask_ai(test_config, question):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace_id"]
    chat_ai_res = sdk.compute.ai_chat(workspace_id, question=question)

    print(f"Chat AI response: {chat_ai_res}")
    assert chat_ai_res is not None, "Response should not be None"


if __name__ == "__main__":
    pytest.main()
