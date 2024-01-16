# (C) 2023 GoodData Corporation
import os
import re
import time
from logging import Logger

import requests


def post_gitlab_rest(url: str, headers: dict, data: dict) -> dict:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        raise ValueError(
            f"Response code {response.status_code} was returned. With the following message {response.text}."
        )
    return response.json()


def report_message_to_merge_request(token: str, merge_request_id: str, text: str) -> None:
    url = (
        "https://gitlab.com/api/v4/projects/"
        + f"{os.getenv('CI_MERGE_REQUEST_PROJECT_ID')}/merge_requests/{merge_request_id}/notes"
    )
    headers = {"PRIVATE-TOKEN": token, "Content-Type": "application/json"}
    data = {"body": text}
    post_gitlab_rest(url, headers, data)


def report_message_to_pull_request(logger: Logger, token: str, pull_request_id: int, text: str) -> None:
    try:
        from github import Auth, Github

        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
        issue = repo.get_issue(number=pull_request_id)
        print(f"{issue.user.id=} {issue.user.login=} {issue.user.name=}")
        issue.create_comment(text)
    except ImportError:
        logger.warning("PyGithub module not found, will not be able to report performance to GitHub pull request")


def report_message_to_git_vendor(logger: Logger, degradations: int, allowed_degradation: int, git_table: str) -> None:
    # Running in CI pipeline, report performance of executions to the merge/pull request to notify code reviewer
    gitlab_token = os.getenv("GITLAB_TOKEN")
    merge_request_id = os.getenv("CI_MERGE_REQUEST_IID")
    # Token/PR ID are exposed by GitHub actions in various ways depending on the event type
    # Let's decouple this code from it and expect GitHub workflows to set custom env variables
    github_token = os.getenv("GOODDATA_GITHUB_TOKEN")
    pr_id_str = os.getenv("GOODDATA_GITHUB_PULL_REQUEST_ID")
    pull_request_id = None
    if pr_id_str is not None and pr_id_str != "":
        if re.search(r"^[0-9]+$", pr_id_str) is not None:
            pull_request_id = int(pr_id_str)
        else:
            logger.warning(
                f"Pull request ID '{pr_id_str}' is not a number, "
                + "will not be able to report performance to GitHub pull request"
            )

    # Mention actor in GitHub comment to notify him. E-mail notifications are not sent to GitHub actors by default.
    github_actor = os.getenv("GOODDATA_GITHUB_ACTOR")
    prefix = ""
    if github_actor:
        prefix = f"@{github_actor} "
    if degradations > 0:
        message = (
            f"{prefix}**WARNING:** some executions of dbt models in this merge request are slower than average! "
            + f"Threshold = {allowed_degradation}%\n\n{git_table}"
        )
    else:
        message = f"{prefix}INFO: performance of all executions of dbt models is OK!\n\n{git_table}"

    if github_token and pull_request_id:
        logger.info(f"Sending report to related Github pull request as comment {pull_request_id=}")
        report_message_to_pull_request(logger, github_token, pull_request_id, message)
    elif gitlab_token and merge_request_id:
        logger.info(f"Sending report to related Gitlab merge request as comment {merge_request_id=}")
        report_message_to_merge_request(gitlab_token, merge_request_id, message)


def get_duration(start: float) -> int:
    return int((time.time() - start) * 1000)
