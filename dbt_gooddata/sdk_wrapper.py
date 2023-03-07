from logging import Logger
from typing import Optional
from gooddata_sdk import GoodDataSdk


class GoodDataSdkWrapper:
    # Timeout=600 because supporting waiting for All-in-one image starts
    def __init__(self, args, logger: Logger, timeout=600):
        self.args = args
        self.logger = logger
        self.timeout = timeout
        self.sdk = self.create_sdk()
        self.wait_for_gooddata_is_up(self.timeout)

    @property
    def host(self) -> str:
        return self.args.gooddata_host

    @property
    def token(self) -> str:
        return self.args.gooddata_token

    @property
    def override_host(self) -> Optional[str]:
        return self.args.gooddata_override_host

    def create_sdk(self) -> GoodDataSdk:
        kwargs = {}
        if self.override_host:
            kwargs["Host"] = self.override_host
        masked_token = f"{len(self.token[:-4])*'#'}{self.token[-4:]}"
        self.logger.info(
            f"Connecting to GoodData host={self.host} token={masked_token} override_host={self.override_host}"
        )
        sdk = GoodDataSdk.create(host_=self.host, token_=self.token, **kwargs)
        return sdk

    def wait_for_gooddata_is_up(self, timeout) -> None:
        # Wait for the GoodData.CN docker image to start up
        self.logger.info(f"Waiting for {self.host} to be up")
        self.sdk.support.wait_till_available(timeout=timeout)
        self.logger.info(f"Host {self.host} is up")

    def pre_cache_insights(self, workspaces: list = None) -> None:
        if not workspaces:
            workspaces = [w.id for w in self.sdk.catalog_workspace.list_workspaces()]
        for workspace_id in workspaces:
            insights = self.sdk.insights.get_insights(workspace_id)

            for insight in insights:
                self.sdk.tables.for_insight(workspace_id, insight)
