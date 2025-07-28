# (C) 2025 GoodData Corporation

"""Module for context objects used in GoodData Pipelines provisioning."""


class WorkspaceContext:
    workspace_id: str
    workspace_name: str | None
    wdf_id: str | None
    wdf_values: list[str] | None

    def __init__(
        self,
        workspace_id: str | None,
        workspace_name: str | None,
        wdf_id: str | None = None,
        wdf_values: list[str] | None = None,
    ):
        self.workspace_id: str = workspace_id if workspace_id else "NA"
        self.workspace_name: str | None = workspace_name
        self.wdf_id: str | None = wdf_id
        self.wdf_values: list[str] | None = wdf_values


class UserContext:
    user_id: str
    user_groups: str

    def __init__(self, user_id: str, user_groups: list[str]):
        """User context object, stringifies list of user groups"""
        self.user_id: str = user_id
        self.user_groups: str = ",".join(user_groups)
