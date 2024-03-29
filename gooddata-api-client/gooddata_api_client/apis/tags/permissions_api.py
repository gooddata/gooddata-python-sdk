# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_analytical_dashboards_dashboard_id_available_assignees.get import AvailableAssignees
from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_analytical_dashboards_dashboard_id_permissions.get import DashboardPermissions
from gooddata_api_client.paths.api_v1_layout_workspaces_workspace_id_permissions.get import GetWorkspacePermissions
from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_analytical_dashboards_dashboard_id_manage_permissions.post import ManageDashboardPermissions
from gooddata_api_client.paths.api_v1_layout_workspaces_workspace_id_permissions.put import SetWorkspacePermissions


class PermissionsApi(
    AvailableAssignees,
    DashboardPermissions,
    GetWorkspacePermissions,
    ManageDashboardPermissions,
    SetWorkspacePermissions,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
