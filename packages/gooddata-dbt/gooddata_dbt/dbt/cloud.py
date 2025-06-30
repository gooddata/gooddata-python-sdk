# (C) 2023 GoodData Corporation
import json
import logging
import os
import time
from pathlib import Path
from typing import Union

import attrs
import requests
import yaml
from cattrs import structure
from gooddata_sdk.utils import safeget
from requests import Response

from gooddata_dbt.dbt.environment import DbtCloudEnvironment


@attrs.define(auto_attribs=True, kw_only=True)
class DbtCloudBase:
    base_v2: str = attrs.field(init=False, default="https://cloud.getdbt.com/api/v2")
    base_v3: str = attrs.field(init=False, default="https://cloud.getdbt.com/api/v3")
    base_graphql: str = attrs.field(init=False, default="https://metadata.cloud.getdbt.com/graphql")

    graphql_applied_models = """
        query AppliedModels($environmentId: BigInt!, $first: Int!) {
            environment(id: $environmentId) {
              applied {
                models(first: $first) {
                  edges {
                    node {
                      name
                      uniqueId
                      materializedType
                      executionInfo {
                        lastSuccessRunId
                        executionTime
                        executeStartedAt
                      }
                    }
                  }
                }
              }
            }
          }
        """
    graphql_model_historical_runs = """
        query modelHistoricalRuns($environmentId: BigInt!, $modelId: String!, $first: Int!) {
          environment(id: $environmentId) {
            applied {
              modelHistoricalRuns(
                uniqueId: $modelId
                lastRunCount: $first
              ) {
                runId # Get historical results for a particular model
                runGeneratedAt
                executionTime # View build time across runs
                status
              }
            }
          }
        }
        """


@attrs.define(auto_attribs=True, kw_only=True)
class DbtCredentials(DbtCloudBase):
    account_id: str
    token: str = attrs.field(repr=lambda value: "***")

    def can_connect(self) -> bool:
        url = f"{self.base_v2}/accounts/"
        response = requests.get(url, headers=self.bearer_token_header)
        return response.status_code == 200

    @property
    def bearer_token_header(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}


@attrs.define(auto_attribs=True, kw_only=True)
class DbtExecutionInfo:
    last_success_run_id: str
    execution_time: float

    @classmethod
    def from_dict(cls, data: dict) -> "DbtExecutionInfo":
        return structure(data, cls)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtExecutionHistoryInfo:
    run_id: str
    execution_time: float
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "DbtExecutionHistoryInfo":
        return structure(data, cls)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtExecution:
    name: str
    unique_id: str
    execution_info: DbtExecutionInfo

    @classmethod
    def from_dict(cls, data: dict) -> "DbtExecution":
        return structure(data, cls)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtConnection(DbtCloudBase):
    credentials: DbtCredentials

    def __attrs_post_init__(self) -> None:
        can_connect = self.credentials.can_connect()
        if not can_connect:
            raise ValueError("Cannot connect to dbt Cloud. Please, check credentials.")

    def _post_rest(self, url: str, data: dict) -> dict:
        response = requests.post(url, headers=self.credentials.bearer_token_header, data=data)
        if response.status_code != 200:
            raise ValueError(
                f"Response code {response.status_code} was returned. With the following message {response.text}."
            )
        return response.json()

    def _post_graphql(self, query: str, variables: dict) -> dict:
        response = requests.post(
            self.base_graphql,
            headers=self.credentials.bearer_token_header,
            json={"query": query, "variables": variables},
        )
        if response.status_code != 200:
            raise ValueError(
                f"Response code {response.status_code} was returned. With the following message {response.text}."
            )
        return response.json()

    def run_job(self, logger: logging.Logger, job_id: str) -> tuple[str, str]:
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/jobs/{job_id}/run/"
        data = {"cause": "Triggered via API by gooddata-dbt plugin"}
        # Allow testing from localhost where COMMIT_SHA is not set
        # GitHub does not propagate CI_COMMIT_SHA to environment variable in workers
        # Developers must propagate it manually from ${{ github.event.pull_request.head.sha }} to GOODDATA_GITHUB_SHA
        # DOC: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request
        commit_sha = os.getenv("GOODDATA_GITHUB_SHA") or os.getenv("CI_COMMIT_SHA")
        if commit_sha:
            data = {
                "cause": f"Triggered via API by gooddata-dbt plugin - {commit_sha=}",
                "git_sha": commit_sha,
            }
        logger.info(f"Run dbt cloud job {job_id=} with cause={data['cause']}")
        result = self._post_rest(url, data)
        run_id = safeget(result, ["data", "id"])
        run_href = safeget(result, ["data", "href"])
        if run_id is None:
            raise ValueError("Could not find wanted content.")
        return run_id, run_href

    @staticmethod
    def _was_fetch_success(response: dict) -> bool:
        is_complete = safeget(response, ["data", "is_complete"])
        is_success = safeget(response, ["data", "is_success"])
        return is_complete and is_success

    @staticmethod
    def _is_fetch_done(response: dict) -> bool:
        is_complete = safeget(response, ["data", "is_complete"])
        is_error = safeget(response, ["data", "is_error"])
        if is_error:
            status_humanized = safeget(response, ["data", "status_humanized"])
            raise Exception(f"dbt cloud job failed {status_humanized=}")
        return is_complete

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
        # TODO - allow users to configure this from outside
        timeout: float = 600.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        time_sum = 0.0
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/runs/{run_id}"
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
        if not os.path.isdir(path):
            os.makedirs(path)
        with open(path / identifier, "w") as f:
            json.dump(result, f)

    def download_manifest(self, run_id: str, path: Union[str, Path] = Path("target")) -> None:
        self.download_artifact(run_id, "manifest.json", path)

    def read_env_vars(self, project_id: str, job_id: str) -> dict:
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

    def get_environment_id(self, job_id: str) -> str:
        url = f"{self.base_v2}/accounts/{self.credentials.account_id}/jobs/{job_id}/"
        response = self._call_get_dbt_endpoint(url)
        result = response.json()
        environment_id = safeget(result, ["data", "environment_id"])
        return environment_id

    # TODO - now it supports only Snowflake, add all supported data sources
    def read_environment(
        self,
        environment_id: str,
        project_id: str,
    ) -> DbtCloudEnvironment:
        url = (
            f"{self.base_v3}/accounts/{self.credentials.account_id}/projects/{project_id}/"
            + f"environments/{environment_id}"
        )
        response = self._call_get_dbt_endpoint(url)
        result = response.json()
        return DbtCloudEnvironment.from_dict(result["data"])

    @staticmethod
    def make_profiles(
        environment: DbtCloudEnvironment,
        path_to_profiles: Path,
        profile_file: str = "profiles.yml",
    ) -> None:
        if not os.path.isdir(path_to_profiles):
            os.makedirs(path_to_profiles)
        profile_file_path = path_to_profiles / profile_file
        profile = os.getenv("ELT_ENVIRONMENT")
        target = os.getenv("DBT_TARGET")
        db_pass = os.getenv("DBT_DB_PASS")
        schema_name = os.getenv("DBT_OUTPUT_SCHEMA")
        if not profile or not target or not db_pass or not schema_name:
            raise ValueError("Env variables ELT_ENVIRONMENT, DBT_TARGET, DBT_DB_PASS, DBT_OUTPUT_SCHEMA must be set.")
        data = {profile: {"outputs": {target: environment.to_profile(db_pass, schema_name)}}}

        with open(profile_file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, encoding="utf-8")

    @staticmethod
    def string_camel_to_snake(element: str) -> str:
        return "".join(["_" + c.lower() if c.isupper() else c for c in element]).lstrip("_")

    def dict_camel_to_snake(self, data: Union[dict, list]) -> Union[dict, list]:
        if isinstance(data, list):
            result = []
            for record in data:
                if isinstance(record, dict):
                    result.append(self.dict_camel_to_snake(record))
                else:
                    return record
        else:
            result = {}  # type: ignore
            for key, value in data.items():
                if isinstance(value, dict):
                    result[self.string_camel_to_snake(key)] = self.dict_camel_to_snake(value)  # type: ignore
                else:
                    result[self.string_camel_to_snake(key)] = value  # type: ignore
        return result

    def get_last_execution(self, environment_id: str, model_count: int) -> list[DbtExecution]:
        variables = {"environmentId": environment_id, "first": model_count}
        result = self._post_graphql(self.graphql_applied_models, variables)
        model_edges = self.dict_camel_to_snake(safeget(result, ["data", "environment", "applied", "models", "edges"]))
        return [DbtExecution.from_dict(m["node"]) for m in model_edges]

    def get_average_times(
        self, logger: logging.Logger, models: list[DbtExecution], environment_id: str, history_count: int
    ) -> dict[str, float]:
        models_history_avg_execution_times = {}
        for model in models:
            variables = {"environmentId": environment_id, "modelId": model.unique_id, "first": history_count}
            logger.debug(f"Calling modelHistoricalRuns with {variables=}")
            try:
                result = self._post_graphql(self.graphql_model_historical_runs, variables)
            except Exception as e:
                logger.error(f"modelHistoricalRuns API returned error: {str(e)}")
                raise Exception("Error calling modelHistoricalRuns")
            model_historical_runs = self.dict_camel_to_snake(
                safeget(result, ["data", "environment", "applied", "modelHistoricalRuns"])
            )
            execs = [DbtExecutionHistoryInfo.from_dict(r) for r in model_historical_runs]
            exec_times = [e.execution_time for e in execs]
            avg_exec_time = sum(exec_times) / len(exec_times)
            models_history_avg_execution_times[model.unique_id] = avg_exec_time

        return models_history_avg_execution_times
