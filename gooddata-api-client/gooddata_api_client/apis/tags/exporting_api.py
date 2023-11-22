# coding: utf-8

"""
    OpenAPI definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v0
    Contact: support@gooddata.com
    Generated by: https://openapi-generator.tech
"""

from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_export_visual.post import CreatePdfExport
from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_export_visual_export_id.get import GetExportedFile
from gooddata_api_client.paths.api_v1_actions_workspaces_workspace_id_export_visual_export_id_metadata.get import GetMetadata


class ExportingApi(
    CreatePdfExport,
    GetExportedFile,
    GetMetadata,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
