# (C) 2023 GoodData Corporation
import os
import time

import requests


def post_gitlab_rest(url: str, headers: dict, data: dict) -> dict:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        raise ValueError(
            f"Response code {response.status_code} was returned. With the following message {response.text}."
        )
    return response.json()


def report_message_to_merge_request(token: str, text: str) -> None:
    url = (
        "https://gitlab.com/api/v4/projects/"
        + f"{os.getenv('CI_MERGE_REQUEST_PROJECT_ID')}/merge_requests/{os.getenv('CI_MERGE_REQUEST_IID')}/notes"
    )
    headers = {"PRIVATE-TOKEN": token, "Content-Type": "application/json"}
    data = {"body": text}
    post_gitlab_rest(url, headers, data)


def get_duration(start: float) -> int:
    return int((time.time() - start) * 1000)
