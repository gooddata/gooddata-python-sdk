# (C) 2023 GoodData Corporation
import argparse
from logging import Logger
from typing import Optional

from gooddata_sdk import GoodDataSdk

from gooddata_dbt.gooddata.api_wrapper import GoodDataApiWrapper


class GoodDataSdkWrapper:
    # Timeout=600 because supporting waiting for All-in-one image starts
    def __init__(
        self, args: argparse.Namespace, logger: Logger, profile: Optional[str] = None, timeout: int = 600
    ) -> None:
        self.args = args
        self.logger = logger
        self.timeout = timeout
        self.profile = profile
        self.sdk = self.create_sdk()
        self.sdk_facade = self.create_sdk_facade()
        if not self.args.dry_run:
            self.wait_for_gooddata_is_up(self.timeout)

    def get_host_from_sdk(self) -> Optional[str]:
        # TODO - make _hostname public in gooddata_sdk
        return self.sdk.client._hostname

    def create_sdk(self) -> GoodDataSdk:
        if self.profile:
            self.logger.info(f"Connecting to GoodData using profile={self.profile}")
            sdk = GoodDataSdk.create_from_profile(profile=self.profile)
            return sdk
        else:
            host = self.args.gooddata_host
            token = self.args.gooddata_token
            override_host = self.args.gooddata_override_host
            kwargs = {}
            if override_host:
                kwargs["Host"] = override_host
            masked_token = f"{len(token[:-4]) * '#'}{token[-4:]}"
            self.logger.info(f"Connecting to GoodData host={host} token={masked_token} override_host={override_host}")
            sdk = GoodDataSdk.create(host_=host, token_=token, **kwargs)
            return sdk

    def create_sdk_facade(self) -> GoodDataApiWrapper:
        return GoodDataApiWrapper(self.sdk, self.logger, self.args.dry_run)

    def wait_for_gooddata_is_up(self, timeout: int) -> None:
        # Wait for the GoodData.CN docker image to start up or prevent hiccups of cloud deployments
        # We have to take hostname from sdk.client, because it can also be collected from profiles.yml file
        host = self.get_host_from_sdk()
        self.logger.info(f"Waiting for {host} to be up")
        self.sdk.support.wait_till_available(timeout=timeout)
        self.logger.info(f"Host {host} is up")

    def pre_cache_visualizations(self, workspaces: Optional[list] = None) -> None:
        if not workspaces:
            workspaces = [w.id for w in self.sdk.catalog_workspace.list_workspaces()]
        for workspace_id in workspaces:
            visualizations = self.sdk.visualizations.get_visualizations(workspace_id)

            for visualization in visualizations:
                self.sdk.tables.for_visualization(workspace_id, visualization)
