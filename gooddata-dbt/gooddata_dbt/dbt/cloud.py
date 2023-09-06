# (C) 2023 GoodData Corporation
import json
import os
import time
from pathlib import Path
from typing import Dict, Union

import attrs
import requests
from gooddata_dbt.dbt.environment import Environment
from requests import Response

from gooddata_sdk.utils import safeget


@attrs.define(auto_attribs=True, kw_only=True)
class DbtCloudBase:
    base_v2: str = attrs.field(init=False, default="https://cloud.getdbt.com/api/v2")
    base_v3: str = attrs.field(init=False, default="https://cloud.getdbt.com/api/v3")


@attrs.define(auto_attribs=True, kw_only=True)
class DbtCredentials(DbtCloudBase):
    account_id: str
    token: str = attrs.field(repr=lambda value: "***")

    def can_connect(self) -> bool:
        url = f"{self.base_v2}/accounts/"
        response = requests.get(url, headers=self.bearer_token_header)
        return response.status_code == 200

    @property
    def bearer_token_header(self) -> Dict:
        return {"Authorization": f"Bearer {self.token}"}


@attrs.define(auto_attribs=True, kw_only=True)
class DbtConnection(DbtCloudBase):
    credentials: DbtCredentials

    def __attrs_post_init__(self) -> None:
        can_connect = self.credentials.can_connect()
        if not can_connect:
            raise ValueError("Cannot connect to dbt Cloud. Please, check credentials.")

    def run_job(self, job_id: str) -> str:
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/jobs/{job_id}/run/"
        data = {"cause": "Triggered via API"}
        response = requests.post(url, headers=self.credentials.bearer_token_header, data=data)
        if response.status_code != 200:
            raise ValueError(
                f"Response code {response.status_code} was returned. With the following message {response.text}."
            )
        result = response.json()
        run_id = safeget(result, ["data", "id"])
        if run_id is None:
            raise ValueError("Could not find wanted content.")
        return run_id

    @staticmethod
    def _was_fetch_success(response: Dict) -> bool:
        is_complete = safeget(response, ["data", "is_complete"])
        is_success = safeget(response, ["data", "is_success"])
        return is_complete and is_success

    @staticmethod
    def _is_fetch_done(response: Dict) -> bool:
        in_progress = safeget(response, ["data", "in_progress"])
        return not in_progress

    def _call_get_dbt_endpoint(self, url: str) -> Response:
        response = requests.get(url, headers=self.credentials.bearer_token_header)
        if response.status_code != 200:
            raise ValueError(
                f"Response code {response.status_code} was returned. With the following message {response.text}."
            )
        return response

    def fetch_run_result(
        self,
        run_id: str,
        timeout: float = 120.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        time_sum = 0.0
        url = f"{self.base_v2}/accounts/{self.base_v2}/runs/{run_id}"
        while True:
            response = self._call_get_dbt_endpoint(url)
            result = response.json()
            if self._is_fetch_done(result) and time_sum <= timeout:
                break
            time.sleep(retry)
            time_sum += retry
            retry = min(retry * 2, max_retry)
        if not self._was_fetch_success(result):
            raise ValueError(f"Job with {run_id=} failed.")
        if time_sum >= timeout:
            raise ValueError(f"Job with {run_id=} timed out. The time out was {timeout}.")

    def download_artifact(self, run_id: str, identifier: str, path: Union[str, Path]) -> None:
        """
        :param run_id: Identifier of the run.
        :param identifier: E.g., manifest.json
        :param path: Path where to store file.
        """
        path = path if isinstance(path, Path) else Path(path)
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/runs/{run_id}/artifacts/{identifier}"
        response = self._call_get_dbt_endpoint(url)
        result = response.json()
        os.makedirs(path)
        with open(path / identifier, "w") as f:
            json.dump(result, f)

    def download_manifest(self, run_id: str, path: Union[str, Path]) -> None:
        self.download_artifact(run_id, "manifest.json", path)

    def read_env_vars(self, project_id: str, job_id: str) -> Dict:
        url = (
            f"{self.base_v3}/accounts/{self.credentials.account_id}/projects/{project_id}"
            f"/environment-variables/job/?job_definition_id={job_id}"
        )
        response = self._call_get_dbt_endpoint(url)
        result = response.json()
        data = result["data"]
        env_vars = {}
        for k, v in data.items():
            env_vars[k] = safeget(v, ["project", "value"])
        return env_vars

    def read_environment(
        self,
        environment_id: str,
        project_id: str,
        job_id: str,
        schema_key: str = "DBT_OUTPUT_SCHEMA",
        user_key: str = "DBT_USER",
        password_key: str = "DBT_PASSWORD",
    ) -> Environment:
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/environments/{environment_id}"
        response = self._call_get_dbt_endpoint(url)
        result = response.json()
        connection = safeget(result, ["data", "connection"])
        env_vars = self.read_env_vars(project_id, job_id)
        environment_dict = {
            **connection,
            "environment_name": safeget(result, ["data", "name"]),
            "schema": env_vars[schema_key],
            "user_key": user_key,
            "password_key": password_key,
        }
        environment = Environment.from_dict(environment_dict)
        return environment
