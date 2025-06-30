# (C) 2025 GoodData Corporation

"""Module for managing workspace data filter settings in GoodData Cloud."""

import json
from typing import Any
from uuid import uuid4

from requests import Response

from gooddata_pipelines.api import GoodDataApi
from gooddata_pipelines.logger.logger import LogObserver
from gooddata_pipelines.provisioning.entities.workspaces.models import (
    WDFSetting,
    WorkspaceDataMaps,
)
from gooddata_pipelines.provisioning.utils.context_objects import (
    WorkspaceContext,
)
from gooddata_pipelines.provisioning.utils.exceptions import WorkspaceException


class WorkspaceDataFilterManager:
    """
    Helper class to manage workspace data filter settings. Note that Workspace
    Data Filters themselves are not managed here. The Workspace Data Filter
    Setting object represents the relationship of values in a WDF column and
    a specific workspace.
    """

    def __init__(self, api: GoodDataApi, maps: WorkspaceDataMaps) -> None:
        self.api: GoodDataApi = api
        self.maps: WorkspaceDataMaps = maps
        self.logger: LogObserver = LogObserver()

    @staticmethod
    def _create_wdf_setting_dict(
        wdf_setting_id: str, wdf_id: str, wdf_values: list[str]
    ) -> dict[str, Any]:
        """Loads a JSON template of a WDF setting and fills it with the given values."""
        values = [str(value) for value in wdf_values]

        import os

        wdf_setting_path = os.path.join(
            os.path.dirname(__file__), "../../assets/wdf_setting.json"
        )
        with open(os.path.abspath(wdf_setting_path)) as file:
            wdf_setting: dict[str, Any] = json.load(file)

        wdf_setting["data"]["attributes"]["filterValues"] = values
        wdf_setting["data"]["id"] = wdf_setting_id
        wdf_setting["data"]["relationships"]["workspaceDataFilter"]["data"][
            "id"
        ] = wdf_id

        return wdf_setting

    def _get_wdf_settings_for_workspace(
        self, workspace_id: str
    ) -> list[WDFSetting]:
        """Gets all workspace data filter settings for a given workspace."""
        wdf_settings_response: Response = (
            self.api.get_workspace_data_filter_settings(workspace_id)
        )

        if not wdf_settings_response.ok:
            raise WorkspaceException(
                f"Failed to get WDF settings: {wdf_settings_response.text}",
                workspace_id=workspace_id,
                http_status=str(wdf_settings_response.status_code),
            )

        raw_wdf_settings: dict[str, Any] = wdf_settings_response.json()

        data: list[dict[str, Any]] = raw_wdf_settings["data"]

        wdf_settings: list[WDFSetting] = [
            WDFSetting(**wdf_setting) for wdf_setting in data
        ]

        return wdf_settings

    @staticmethod
    def _get_actual_wdf_setting_id_and_values(
        actual_wdf_settings: list[WDFSetting], actual_wdf_id: str
    ) -> tuple[str, list[str]]:
        """Returns WDF setting ID and values for given WDF ID."""
        for actual_wdf_setting in actual_wdf_settings:
            if (
                actual_wdf_setting.relationships.workspaceDataFilter["data"].id
                == actual_wdf_id
            ):
                actual_wdf_setting_id = actual_wdf_setting.id
                actual_wdf_values = actual_wdf_setting.attributes.filterValues

                return actual_wdf_setting_id, actual_wdf_values

        raise WorkspaceException(
            "Could not find WDF setting for WDF in actual WDF settings.",
            wdf_id=actual_wdf_id,
        )

    def _delete_redundant_wdf_setting(
        self,
        workspace_context: WorkspaceContext,
        actual_wdf_id: str,
        actual_wdf_settings: list[WDFSetting],
    ) -> None:
        """Deletes a WDF setting."""
        actual_wdf_setting_id, actual_wdf_values = (
            self._get_actual_wdf_setting_id_and_values(
                actual_wdf_settings, actual_wdf_id
            )
        )
        # Update context with actual values
        workspace_context.wdf_id = actual_wdf_id
        workspace_context.wdf_values = actual_wdf_values

        # If there is a WDF setting for a WDF that should not be associated with
        # the workspace, then delete the setting
        delete_response: Response = (
            self.api.delete_workspace_data_filter_setting(
                workspace_context.workspace_id,
                actual_wdf_setting_id,
            )
        )
        if delete_response.ok:
            self.logger.info(
                f"Deleted WDF setting for WDF {workspace_context.wdf_id} in "
                + f"workspace {workspace_context.workspace_id}"
            )
        else:
            raise WorkspaceException(
                f"Failed to delete WDF setting: {delete_response.text}",
                delete_response,
                workspace_context,
            )

    def _post_wdf_setting(
        self,
        workspace_context: WorkspaceContext,
    ) -> None:
        """Posts a WDF setting to Panther."""
        wdf_setting = self._create_wdf_setting_dict(
            str(uuid4()),
            str(workspace_context.wdf_id),
            workspace_context.wdf_values
            if workspace_context.wdf_values
            else [],
        )
        post_response: Response = self.api.post_workspace_data_filter_setting(
            workspace_context.workspace_id,
            wdf_setting,
        )
        if post_response.ok:
            self.logger.info(
                f"Created WDF setting for WDF {workspace_context.wdf_id} in workspace {workspace_context.workspace_id}"
            )
        else:
            raise WorkspaceException(
                f"Failed to create WDF setting: {post_response.text}",
                post_response,
                workspace_context,
            )

    def _put_wdf_setting(
        self,
        workspace_context: WorkspaceContext,
        actual_wdf_settings: list[WDFSetting],
    ) -> None:
        # get Panther WDF setting ID
        actual_wdf_setting_id, _ = self._get_actual_wdf_setting_id_and_values(
            actual_wdf_settings, str(workspace_context.wdf_id)
        )

        wdf_setting = self._create_wdf_setting_dict(
            actual_wdf_setting_id,
            str(workspace_context.wdf_id),
            workspace_context.wdf_values
            if workspace_context.wdf_values
            else [],
        )

        put_response: Response = self.api.put_workspace_data_filter_setting(
            workspace_context.workspace_id,
            wdf_setting,
        )
        if put_response.ok:
            self.logger.info(
                f"Updated WDF setting for WDF {workspace_context.wdf_id} in workspace {workspace_context.workspace_id}"
            )
        else:
            raise WorkspaceException(
                f"Failed to update WDF setting: {put_response.text}",
                put_response,
                workspace_context,
            )

    def _compare_wdf_settings(
        self,
        workspace_context: WorkspaceContext,
        source_wdf_config: dict[str, list[str]],
        upstream_wdf_settings: list[WDFSetting],
    ) -> None:
        """
        Compares WDF settings as extracted from the source with the actual WDF
        settings in Panther. We do not know the WDF setting IDs from the outset,
        which is why we need to check the WDF IDs and then the settings values
        in a roundabout way. I.e., we know that a WDF should have some setting
        with an unknown ID, but certain values. In this case, we don't care about
        the setting ID, but need to make sure that the workspace has the correct
        values for the WDF.
        """
        upstream_wdf_ids: set[str] = {
            upstream_wdf_setting.relationships.workspaceDataFilter["data"].id
            for upstream_wdf_setting in upstream_wdf_settings
        }

        source_wdf_ids: set[str] = set(source_wdf_config.keys())

        # Create map of upstream WDF_ID : WDF values
        upstream_wdf_ids_and_values: dict[str, list[str]] = {}
        for upstream_wdf_setting in upstream_wdf_settings:
            upstream_wdf_ids_and_values[
                upstream_wdf_setting.relationships.workspaceDataFilter[
                    "data"
                ].id
            ] = upstream_wdf_setting.attributes.filterValues

        # Iterate through source WDF settings
        for source_wdf_id in source_wdf_ids:
            # Update WDF information in context to make sure we have the correct
            # data -> there can be multiple WDFs per workspace
            source_values: list[str] = source_wdf_config[source_wdf_id]
            workspace_context.wdf_id = source_wdf_id
            workspace_context.wdf_values = source_values

            # Post WDF setting if missing for a WDF, when it should be there
            if source_wdf_id not in upstream_wdf_ids:
                self._post_wdf_setting(workspace_context)

            # If settings exist for a WDF that should be there, then compare values
            elif source_wdf_id in upstream_wdf_ids:
                actual_values: list[str] = upstream_wdf_ids_and_values[
                    source_wdf_id
                ]

                # If values are different, then update the WDF settings
                if set(source_values) != set(actual_values):
                    self._put_wdf_setting(
                        workspace_context,
                        upstream_wdf_settings,
                    )

        # Go through Panther WDF settings and check if there are any that should
        # not be there. Delete them if so.
        for actual_wdf_id in upstream_wdf_ids:
            if actual_wdf_id not in source_wdf_ids:
                self._delete_redundant_wdf_setting(
                    workspace_context,
                    actual_wdf_id,
                    upstream_wdf_settings,
                )

    def check_wdf_settings(
        self,
        workspace_context: WorkspaceContext,
    ) -> None:
        """
        Checks WDF settings for a given workspace.
        Creates WDF settings defined in source if they are missing in Panther.
        Updates WDF setting values if they are different in source and Panther.
        Deletes WDF settings from Panther if they are not defined in source.
        """
        actual_wdf_settings: list[WDFSetting] = (
            self._get_wdf_settings_for_workspace(workspace_context.workspace_id)
        )

        source_wdf_config: dict[str, list[str]] = (
            self.maps.workspace_id_to_wdf_map[workspace_context.workspace_id]
        )

        self._compare_wdf_settings(
            workspace_context, source_wdf_config, actual_wdf_settings
        )
