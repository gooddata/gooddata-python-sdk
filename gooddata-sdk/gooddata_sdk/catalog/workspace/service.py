# (C) 2022 GoodData Corporation
from __future__ import annotations

import copy
import functools
import logging
import re
from copy import deepcopy
from math import ceil
from pathlib import Path
from time import time
from typing import Any, Callable, Optional
from xml.etree import ElementTree as ET

import attrs
from gooddata_api_client.api.translations_api import LocaleRequest
from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest

from gooddata_sdk import CatalogDeclarativeAutomation
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.permission.service import CatalogPermissionService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeFilterView,
    CatalogDeclarativeUserDataFilters,
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
    get_workspace_folder,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.workspace_setting import CatalogWorkspaceSetting
from gooddata_sdk.catalog.workspace.entity_model.filter_view import (
    CatalogFilterView,
    CatalogFilterViewDocument,
)
from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogUserDataFilter,
    CatalogUserDataFilterDocument,
)
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.utils import (
    HttpMethod,
    create_directory,
    get_namespace_from_xliff,
    load_all_entities,
    load_all_entities_dict,
    read_layout_from_file,
    write_layout_to_file,
)

logger = logging.getLogger(__name__)


class CatalogWorkspaceService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)
        self._permissions_service = CatalogPermissionService(api_client)

    # Entities methods

    def create_or_update(self, workspace: CatalogWorkspace) -> None:
        """Create a new workspace or overwrite an existing workspace with the same id.

        Args:
            workspace (CatalogWorkspace):
                Catalog Workspace object to be created or updated.

        Returns:
            None

        Raises:
            ValueError: Workspace parent can not be updated.
        """
        try:
            found_workspace = self.get_workspace(workspace.id)
            # Update of parent is not allowed
            if found_workspace.parent_id == workspace.parent_id:
                self._entities_api.update_entity_workspaces(
                    workspace.id,
                    workspace.to_api(),
                )
            else:
                raise ValueError(
                    f"Workspace parent can not be updated. "
                    f"Original parent {found_workspace.parent_id}, wanted parent {workspace.parent_id}."
                )
        except NotFoundException:
            self._entities_api.create_entity_workspaces(workspace.to_api())

    def get_workspace(self, workspace_id: str) -> CatalogWorkspace:
        """Get an individual workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            CatalogWorkspace:
                Catalog workspace object containing structure of the workspace.
        """
        return CatalogWorkspace.from_api(
            self._entities_api.get_entity_workspaces(workspace_id, include=["workspaces"]).data
        )

    def delete_workspace(self, workspace_id: str) -> None:
        """Delete a workspace with all its content - logical model and analytics model.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            None

        Raises:
            ValueError:
                Workspace does not exist.
            ValueError:
                Workspace is a parent of a workspace.
        """
        workspaces = self.list_workspaces()
        if workspace_id not in [w.id for w in workspaces]:
            raise ValueError(f"Can not delete {workspace_id} workspace. This workspace does not exist.")
        children = [w.id for w in workspaces if w.parent_id == workspace_id]
        if children:
            raise ValueError(
                f"Can not delete {workspace_id} workspace. "
                f"This workspace is parent of the following workspaces: {', '.join(children)}. "
            )
        self._entities_api.delete_entity_workspaces(workspace_id)

    def list_workspaces(self) -> list[CatalogWorkspace]:
        """Returns a list of all workspaces in current organization

        Returns:
            list[CatalogWorkspace]: List of workspaces in the current organization.

        """
        get_workspaces = functools.partial(
            self._entities_api.get_all_entities_workspaces,
            include=["workspaces"],
            _check_return_type=False,
        )
        workspaces = load_all_entities(get_workspaces)
        return [CatalogWorkspace.from_api(w) for w in workspaces.data]

    def create_or_update_workspace_setting(self, workspace_id: str, workspace_setting: CatalogWorkspaceSetting) -> None:
        """Create a new workspace setting or overwrite an existing workspace setting with the same id.

        Args:
            workspace_id (str):
                ID of workspace where we create the setting
            workspace_setting (CatalogWorkspaceSetting):
                Catalog Workspace Setting object to be created or updated.

        Returns:
            None
        """
        if workspace_setting.id is None:
            self._entities_api.create_entity_workspace_settings(workspace_id, workspace_setting.to_api(True))
        else:
            try:
                self.get_workspace_setting(workspace_id, workspace_setting.id)
                self._entities_api.update_entity_workspace_settings(
                    workspace_id,
                    workspace_setting.id,
                    workspace_setting.to_api(),
                )
            except NotFoundException:
                self._entities_api.create_entity_workspace_settings(workspace_id, workspace_setting.to_api(True))

    def delete_workspace_setting(self, workspace_id: str, workspace_setting_id: str) -> None:
        try:
            self._entities_api.delete_entity_workspace_settings(workspace_id, workspace_setting_id)
        except NotFoundException:
            pass

    def get_workspace_setting(self, workspace_id: str, workspace_setting_id: str) -> CatalogWorkspaceSetting:
        return CatalogWorkspaceSetting.from_api(
            self._entities_api.get_entity_workspace_settings(workspace_id, workspace_setting_id).data
        )

    def list_workspace_settings(self, workspace_id: str) -> list[CatalogWorkspaceSetting]:
        get_workspace_settings = functools.partial(
            self._entities_api.get_all_entities_workspace_settings,
            workspace_id,
            _check_return_type=False,
        )
        workspace_settings = load_all_entities(get_workspace_settings).data
        return [CatalogWorkspaceSetting.from_api(ws) for ws in workspace_settings]

    def resolve_all_workspace_settings(self, workspace_id: str) -> dict:
        """
        Resolves values for all settings in a workspace by current user, workspace, organization, or default settings
        and return them as a dictionary. Proper parsing is up to the caller.
        TODO: long-term we should return a proper entity object.

        :param workspace_id: Workspace ID
        :return: Dict of settings
        """
        # note: in case some settings were recently added and the API client was not regenerated it can fail on
        #       invalid value when validating allowed types on the client side before request is sent to the server
        resolved_workspace_settings = [
            setting.to_dict()
            for setting in self._client.actions_api.workspace_resolve_all_settings(
                workspace_id,
                _check_return_type=False,
            )
        ]
        return {setting["type"]: setting for setting in resolved_workspace_settings}

    def resolve_workspace_settings(self, workspace_id: str, settings: list) -> dict:
        """
        Resolves values for given settings in a workspace by current user, workspace, organization, or default settings
        and return them as a dictionary. Proper parsing is up to the caller.
        TODO: long-term we should return a proper entity object.

        :param workspace_id: Workspace ID
        :param settings: List of settings to resolve
        :return: Dict of settings
        """
        resolved_workspace_settings = [
            setting.to_dict()
            for setting in self._client.actions_api.workspace_resolve_settings(
                workspace_id,
                ResolveSettingsRequest(settings=settings),
                _check_return_type=False,
            )
        ]
        return {setting["type"]: setting for setting in resolved_workspace_settings}

    # Declarative methods - workspaces

    def get_declarative_workspaces(self, exclude: Optional[list[str]] = None) -> CatalogDeclarativeWorkspaces:
        """Get all workspaces in the current organization in a declarative form.

        Args:
            exclude (Optional[list[str]]):
                Defines properties which should not be included in the payload.

        Returns:
            CatalogDeclarativeWorkspaces:
                Declarative Workspaces object including all the workspaces for given organization.
        """
        if exclude is None:
            exclude = []
        return CatalogDeclarativeWorkspaces.from_dict(
            self._layout_api.get_workspaces_layout(exclude=exclude).to_dict(camel_case=False), camel_case=False
        )

    def put_declarative_workspaces(self, workspace: CatalogDeclarativeWorkspaces) -> None:
        """Set layout of all workspaces and their hierarchy. Parameter is in declarative form.

        Args:
            workspace (CatalogDeclarativeWorkspaces):
                Declarative Workspaces object including all the workspaces for given organization.


        Returns:
            None
        """
        self._layout_api.set_workspaces_layout(workspace.to_api())

    def store_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        """Stores declarative workspaces in a given path, as folder hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_workspaces().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeWorkspaces:
        """Load declarative workspaces layout, which was stored using `store_declarative_workspaces`

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
        Returns:
            CatalogDeclarativeWorkspaces:
                Declarative Workspaces Object
        """
        return CatalogDeclarativeWorkspaces.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspaces(self, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_workspaces`.

        This method combines `load_declarative_workspaces` and `put_declarative_workspaces`
        methods to load and set layouts stored using `store_declarative_workspaces`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspaces = self.load_declarative_workspaces(layout_root_path)
        self.put_declarative_workspaces(declarative_workspaces)

    # Declarative methods - workspace

    def get_declarative_workspace(
        self, workspace_id: str, exclude: Optional[list[str]] = None
    ) -> CatalogDeclarativeWorkspaceModel:
        """Retrieve a workspace layout.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            exclude (Optional[list[str]]):
                Defines properties which should not be included in the payload.

        Returns:
            CatalogDeclarativeWorkspaceModel:
                Object Containing declarative Logical Data Model and declarative Analytical Model.
        """
        if exclude is None:
            exclude = []
        return CatalogDeclarativeWorkspaceModel.from_dict(
            self._layout_api.get_workspace_layout(workspace_id=workspace_id, exclude=exclude).to_dict(camel_case=False),
            camel_case=False,
        )

    def put_declarative_workspace(
        self, workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel, standalone_copy: bool = False
    ) -> None:
        """Set a workspace layout.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            workspace (CatalogDeclarativeWorkspaceModel):
                Object Containing declarative Logical Data Model and declarative Analytical Model.
            standalone_copy (bool):
                If true, then workspace data filter references will be removed from LDM.
                Note that first, the copy is made so we do not interfere with the original input.
        Returns:
            None
        """
        if standalone_copy:
            workspace = copy.deepcopy(workspace)
            workspace.remove_wdf_refs()
        self._layout_api.put_workspace_layout(workspace_id, workspace.to_api())

    def store_declarative_workspace(
        self, workspace_id: str, layout_root_path: Path = Path.cwd(), exclude: Optional[list[str]] = None
    ) -> None:
        """Store workspace layout in a directory hierarchy.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().
            exclude (Optional[list[str]]):
                Defines properties which should not be included in the payload.
        """
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        self.get_declarative_workspace(workspace_id=workspace_id, exclude=exclude).store_to_disk(
            workspace_folder=workspace_folder
        )

    def load_declarative_workspace(
        self, workspace_id: str, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceModel:
        """Load declarative workspaces layout, which was stored using `store_declarative_workspace`.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeWorkspaceModel:
                Object Containing declarative Logical Data Model and declarative Analytical Model.
        """
        workspace_folder = get_workspace_folder(
            workspace_id=workspace_id, layout_organization_folder=self.layout_organization_folder(layout_root_path)
        )
        return CatalogDeclarativeWorkspaceModel.load_from_disk(workspace_folder=workspace_folder)

    def load_and_put_declarative_workspace(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_workspace`.

        This method combines `load_declarative_workspace` and `put_declarative_workspace` methods
        to load and set layouts stored using `store_declarative_workspace`.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspace = self.load_declarative_workspace(
            workspace_id=workspace_id, layout_root_path=layout_root_path
        )
        self.put_declarative_workspace(workspace_id=workspace_id, workspace=declarative_workspace)

    def clone_workspace(
        self,
        source_workspace_id: str,
        target_workspace_id: Optional[str] = None,
        target_workspace_name: Optional[str] = None,
        overwrite_existing: Optional[bool] = None,
        data_source_mapping: Optional[dict] = None,
        upper_case: Optional[bool] = True,
        place_in_hierarchy: bool = True,
    ) -> None:
        """Clone workspace from existing workspace.

        Clones complete workspace content - LDM, ADM, permissions.

        If the target workspace already exists, it's content is overwritten.
        This can be useful when testing changes in the clone
          - once you are satisfied, you can clone it back to the origin workspace.
        For the safety, you have to enforce this behavior by the dedicated input argument `overwrite_existing`.

        Beware of workspace data filters - after the clone you have to set WDF value for the new workspace.

        Args:
            source_workspace_id (str):
                Source workspace ID, from which we wanna create a clone
            target_workspace_id (str):
                Target workspace ID, where we wanna clone the source workspace
                Optional, if empty, we generate <source_workspace_id>_clone
            target_workspace_name (str):
                Target workspace name
                Optional, if empty, we generate <source_workspace_name> (Clone)
            overwrite_existing (bool):
                Overwrite existing workspace.
            data_source_mapping (dict):
                Optional, allows users to map LDM to different data source ID
            upper_case (bool):
                Optional, allows users to change the case of all physical object IDs (table names, columns names)
                True changes it to upper-case, False to lower-case, None(default) is noop
                Useful when migrating to Snowflake, which is the only DB with upper-case default.
            place_in_hierarchy (bool):
                Place in the hierarchy of the source parent workspace.

        Returns:
            None
        """
        if not place_in_hierarchy:
            raise ValueError(f"{place_in_hierarchy=} currently not supported")
        # TODO - what if it has already been cloned? List existing WS and find first free WS ID?
        source_declarative_ws = self.get_declarative_workspace(workspace_id=source_workspace_id)
        source_ws = self.get_workspace(source_workspace_id)

        final_target_workspace_id = target_workspace_id or f"{source_workspace_id}_clone"
        final_target_workspace_name = target_workspace_name or f"{source_ws.name} (Clone)"
        # TODO - enable cloning into another hierarchy
        final_target_parent_id = source_ws.parent_id

        try:
            self.get_workspace(final_target_workspace_id)
            if not overwrite_existing:
                raise Exception(
                    f"Target workspace {final_target_workspace_id} already exists, "
                    "and `overwrite_existing` argument is False"
                )
            if overwrite_existing:
                self.delete_workspace(final_target_workspace_id)
                self.create_or_update(
                    CatalogWorkspace(
                        workspace_id=final_target_workspace_id,
                        name=final_target_workspace_name,
                        parent_id=final_target_parent_id,
                    )
                )
        except NotFoundException:
            self.create_or_update(
                CatalogWorkspace(
                    workspace_id=final_target_workspace_id,
                    name=final_target_workspace_name,
                    parent_id=final_target_parent_id,
                )
            )

        target_declarative_ws = source_declarative_ws
        if source_declarative_ws.ldm:
            target_declarative_ws = attrs.evolve(
                source_declarative_ws,
                ldm=source_declarative_ws.ldm.modify_mapped_data_source(data_source_mapping).change_tables_columns_case(
                    upper_case
                ),
            )
        # copy workspace data filters
        # TODO: reimplement using entity when available
        filters = self.get_declarative_workspace_data_filters()
        new_filters, filters_mapping = filters.create_copy(source_workspace_id, final_target_workspace_id)
        target_declarative_ws.change_wdf_refs_id(filters_mapping)
        self.put_declarative_workspace_data_filters(new_filters)

        self.put_declarative_workspace(workspace_id=final_target_workspace_id, workspace=target_declarative_ws)
        self._permissions_service.put_declarative_permissions(
            final_target_workspace_id, self._permissions_service.get_declarative_permissions(source_workspace_id)
        )

    def generate_localized_workspaces(
        self,
        workspace_id: str,
        to_lang: str,
        to_locale: str,
        from_lang: str = "en",
        translator_func: Optional[Callable] = None,
        layout_root_path: Optional[Path] = None,
        provision_workspace: Optional[bool] = False,
        store_layouts: Optional[bool] = False,
        place_in_hierarchy: bool = True,
    ) -> None:
        """
        Generate layouts of new workspaces based on the source workspace.
        All texts (titles, ...) will be translated to different languages if requested.
        Translation YAML files are created for each language containing pairs of source and target texts.
        If translation is not requested, source and target texts are identical. Users must translate it manually
        We recommend to translate using a third party service and polish the result manually.
        Args:
            workspace_id: ID of source workspace which we clone and translate all texts in it
            to_lang: ISO lang name (IETF BCP 47)
            to_locale: ISO lang code and country code (IETF BCP 47, e.g. en-US, cs-CZ, ...).
                                Check GoodData documentation for what codes are supported.
            from_lang: from which language we are going to translate
            translator_func: 3rd party service capable of translating a batch of strings to various languages
            layout_root_path: folder, where to store all layout YAML files (of new translated workspaces)
                                        Also, the translation files are stored there.
                                        if empty, they are stored to:
                                        <CURRENT_DIR>/<LAYOUT_ROOT_FOLDER>/<organization_id>/
                                        <LAYOUT_WORKSPACES_DIR>/<workspace_id>
                                        else they are stored to <layout_root_path>/
            provision_workspace: Should new workspace for the target language be provisioned?
                                        Including setting of corresponding locales.
            store_layouts: Store declarative layouts of all workspaces to disk
            place_in_hierarchy (bool): Flag if localized workspace should be placed in the hierarchy.

        Returns:
            None
        """
        if not place_in_hierarchy:
            raise ValueError(f"{place_in_hierarchy=} currently not supported")
        logger.info(f"generate_localized_workspaces START from_lang={from_lang} to_lang={to_lang}")
        workspace_folder = self.create_custom_workspace_folder(workspace_id, layout_root_path)
        translation_file_path = workspace_folder / f"translations_{to_lang}.yml"
        already_translated = self.read_translation_file(translation_file_path)
        # Get current WS and its content definitions
        workspace = self.get_workspace(workspace_id)
        workspace_content = self.get_declarative_workspace(workspace_id)
        # Get all texts from WS definition to be translated. Skip already translated.
        to_translate = self.get_texts_to_translate(workspace, workspace_content, already_translated)
        if store_layouts:
            # Backup current workspace
            workspace_content.store_to_disk(workspace_folder)
        # Translate, if requested, otherwise fill in already translated or 1:1 copy of original texts
        translated = self.translate_if_requested(
            to_translate, translator_func, to_lang, from_lang, already_translated, translation_file_path
        )

        # Create new workspace definition with translated texts
        new_workspace = deepcopy(workspace)
        new_workspace_content = deepcopy(workspace_content)
        self.set_translated_texts(workspace, new_workspace, new_workspace_content, to_lang, translated)
        workspace_new_folder = self.create_custom_workspace_folder(new_workspace.id, layout_root_path)
        if store_layouts:
            # Store layouts of new workspace to disk
            new_workspace_content.store_to_disk(workspace_new_folder)
        # Provision new WS if requested
        if provision_workspace:
            self.provision_workspace_with_locales(workspace_id, new_workspace, new_workspace_content, to_locale)

    def create_custom_workspace_folder(self, workspace_id: str, layout_root_path: Optional[Path]) -> Path:
        if layout_root_path:
            workspace_folder = layout_root_path
        else:
            layout_organization_folder = self.layout_organization_folder(Path.cwd())
            workspace_folder = get_workspace_folder(workspace_id, layout_organization_folder)
        create_directory(workspace_folder)
        return workspace_folder

    @staticmethod
    def translate_in_batches(
        to_translate: set[str], to_lang: str, from_lang: str, translator_func: Callable, batch_size: int = 100
    ) -> dict[str, str]:
        start = time()
        # Group the values into batches
        value_batches = [list(to_translate)[i : i + batch_size] for i in range(0, len(to_translate), batch_size)]
        num_of_batches = ceil(float(len(to_translate)) / batch_size)
        logger.info(
            f"Going to translate {len(to_translate)} tokens from {from_lang} "
            f"into {to_lang} language in {num_of_batches} batches"
        )
        result = {}
        # Create a list to store the translated values
        translated_values = []
        # Loop through each value batch
        for i, batch in enumerate(value_batches):
            logger.info(f"Batch {i + 1}/{num_of_batches}")
            # Translate the batch using the Google Cloud Translation API
            api_result = translator_func(batch)
            # Extract the translated values and add them to the list
            translated_values.extend(api_result)
        # Update the data dictionary with the translated values
        result = {key: value for key, value in zip(to_translate, translated_values)}
        duration = int((time() - start) * 1000)
        logger.info(f"Translation finished duration={duration}")
        return result

    @staticmethod
    def read_translation_file(translation_file_path: Path) -> dict[str, str]:
        # Read already existing translation file, if it exists
        already_translated = {}
        if translation_file_path.is_file():
            already_translated = read_layout_from_file(translation_file_path)
        return already_translated

    def provision_workspace_with_locales(
        self,
        source_workspace_id: str,
        new_workspace: CatalogWorkspace,
        new_workspace_content: CatalogDeclarativeWorkspaceModel,
        to_locale: str,
    ) -> None:
        logger.info(f"Provision workspace with locales workspace_id={new_workspace.id}")
        self.create_or_update(new_workspace)

        filters = self.get_declarative_workspace_data_filters()
        new_filters, filters_mapping = filters.create_copy(source_workspace_id, new_workspace.id)
        new_workspace_content.change_wdf_refs_id(filters_mapping)
        self.put_declarative_workspace_data_filters(new_filters)

        self.put_declarative_workspace(new_workspace.id, new_workspace_content)
        # TODO - uncomment the copy after the fix is fully released
        #      - list_workspace_settings is failing with 500 error too :-(
        # Copy settings from source workspace
        # current_settings = self.list_workspace_settings(source_workspace_id)
        # for setting in current_settings:
        #     # TODO - remove delete after the fix is fully released
        #     self.delete_workspace_setting(new_workspace.id, setting.id)
        #     self.create_or_update_workspace_setting(new_workspace.id, setting)
        # TODO - remove deletes after the fix is fully released
        self.delete_workspace_setting(new_workspace.id, "locale")
        self.delete_workspace_setting(new_workspace.id, "formatLocale")
        # Create/update locale settings to target language
        self.create_or_update_workspace_setting(
            new_workspace.id, CatalogWorkspaceSetting(id="locale", content={"value": to_locale}, setting_type="LOCALE")
        )
        self.create_or_update_workspace_setting(
            new_workspace.id,
            CatalogWorkspaceSetting(id="formatLocale", content={"value": to_locale}, setting_type="FORMAT_LOCALE"),
        )

    def translate_if_requested(
        self,
        to_translate: set[str],
        translator_func: Optional[Callable],
        to_lang: str,
        from_lang: str,
        already_translated: dict[str, str],
        translation_file_path: Path,
    ) -> dict[str, str]:
        if to_translate and translator_func:
            translated = {
                **self.translate_in_batches(to_translate, to_lang, from_lang, translator_func),
                **already_translated,
            }
            # Write translation file
            write_layout_to_file(translation_file_path, translated)
        elif already_translated:
            logger.info("Nothing to translate, but translation file exists, so we can apply it.")
            translated = already_translated
        else:
            logger.info(
                "No translation function specified, no translation file exists."
                f"Creating translation file with {from_lang}:{from_lang} mapping."
                "Translate texts manually in this file and run this function again."
            )
            translated = {}
            for x in to_translate:
                translated[x] = x
            write_layout_to_file(translation_file_path, translated)
        return translated

    @staticmethod
    def add_title_description(to_translate: set[str], title: Optional[str], description: Optional[str]) -> None:
        if title:
            to_translate.add(title)
        if description:
            to_translate.add(description)

    def add_title_description_tags(
        self, to_translate: set[str], title: Optional[str], description: Optional[str], tags: Optional[list[str]]
    ) -> None:
        self.add_title_description(to_translate, title, description)
        if tags:
            to_translate.update(set(tags))

    @staticmethod
    def set_title_description(workspace_object: Any, translated: dict[str, str]) -> None:
        if workspace_object.title:
            workspace_object.title = translated[workspace_object.title]
        if workspace_object.description:
            workspace_object.description = translated[workspace_object.description]

    def set_title_description_tags(self, workspace_object: Any, translated: dict[str, str]) -> None:
        self.set_title_description(workspace_object, translated)
        if workspace_object.tags:
            workspace_object.tags = [translated[x] for x in workspace_object.tags]

    def get_texts_to_translate(
        self,
        workspace: CatalogWorkspace,
        workspace_content: CatalogDeclarativeWorkspaceModel,
        already_translated: dict[str, str],
    ) -> set[str]:
        # We translate each string just once. Collect all strings into a set()
        to_translate = set()
        to_translate.add(workspace.name)
        if workspace_content.ldm:
            for dataset in workspace_content.ldm.datasets:
                self.add_title_description(to_translate, dataset.title, dataset.description)
                for attribute in dataset.attributes or []:
                    self.add_title_description_tags(
                        to_translate, attribute.title, attribute.description, attribute.tags
                    )
                    for label in attribute.labels:
                        self.add_title_description_tags(to_translate, label.title, label.description, label.tags)
                for fact in dataset.facts or []:
                    self.add_title_description_tags(to_translate, fact.title, fact.description, fact.tags)
            for date_dataset in workspace_content.ldm.date_instances:
                self.add_title_description_tags(
                    to_translate, date_dataset.title, date_dataset.description, date_dataset.tags
                )
        if workspace_content.analytics:
            for metric in workspace_content.analytics.metrics or []:
                self.add_title_description(to_translate, metric.title, metric.description)
        if workspace_content.analytics:
            for visualization in workspace_content.analytics.visualization_objects or []:
                self.add_title_description(to_translate, visualization.title, visualization.description)
                for bucket in visualization.content["buckets"]:
                    for item in bucket["items"]:
                        if "measure" in item and "alias" in item["measure"]:
                            to_translate.add(item["measure"]["alias"])
            for dashboard in workspace_content.analytics.analytical_dashboards or []:
                self.add_title_description(to_translate, dashboard.title, dashboard.description)
                # Hack: translate titles in free-form, which is not processed intentionally by this SDK
                for section in dashboard.content["layout"]["sections"]:
                    for item in section["items"]:
                        title = item["widget"].get("title")
                        description = item["widget"].get("description")
                        self.add_title_description(to_translate, title, description)
                    if "header" in section:
                        title = section["header"].get("title")
                        description = section["header"].get("description")
                        self.add_title_description(to_translate, title, description)

        # Translate texts, which have not been translated yet
        if already_translated:
            to_translate = to_translate - set(already_translated.keys())
        return to_translate

    def set_translated_texts(
        self,
        workspace: CatalogWorkspace,
        new_workspace: CatalogWorkspace,
        new_workspace_content: CatalogDeclarativeWorkspaceModel,
        lang: str,
        translated: dict[str, str],
    ) -> None:
        # TODO - WS ID/NAME may not be handled if provisioning of WS is not requested
        lang_for_id = re.sub(r"[^a-zA-Z0-9_]", "_", lang)
        new_workspace.id = f"{workspace.id}_{lang_for_id}"
        new_workspace.name = f"{translated[workspace.name]} ({lang})"
        # LDM
        if new_workspace_content.ldm:
            for dataset in new_workspace_content.ldm.datasets:
                self.set_title_description(dataset, translated)
                for attribute in dataset.attributes or []:
                    self.set_title_description_tags(attribute, translated)
                    for label in attribute.labels or []:
                        self.set_title_description_tags(label, translated)
                for fact in dataset.facts or []:
                    self.set_title_description_tags(fact, translated)
            for date_dataset in new_workspace_content.ldm.date_instances:
                self.set_title_description_tags(date_dataset, translated)
        # ADM
        if new_workspace_content.analytics:
            for metric in new_workspace_content.analytics.metrics or []:
                self.set_title_description(metric, translated)
        if new_workspace_content.analytics:
            for visualization in new_workspace_content.analytics.visualization_objects or []:
                self.set_title_description(visualization, translated)
                for bucket in visualization.content["buckets"]:
                    for item in bucket["items"]:
                        if "measure" in item and "alias" in item["measure"]:
                            item["measure"]["alias"] = translated[item["measure"]["alias"]]
            for dashboard in new_workspace_content.analytics.analytical_dashboards or []:
                self.set_title_description(dashboard, translated)
                # Hack: translate titles in free-form, which is not processed intentionally by this SDK
                for section in dashboard.content["layout"]["sections"]:
                    for item in section["items"]:
                        if "title" in item["widget"]:
                            item["widget"]["title"] = translated.get(item["widget"]["title"])
                        if "description" in item["widget"]:
                            item["widget"]["description"] = translated.get(item["widget"]["description"])
                    if "header" in section:
                        if "title" in section["header"]:
                            section["header"]["title"] = translated.get(section["header"]["title"])
                        if "description" in section["header"]:
                            section["header"]["description"] = translated.get(section["header"]["description"])

    @staticmethod
    def _add_target_tags(xliff_content: str, translate_func: Callable) -> bytes:
        """Add target tags to the XLIFF content for translation purposes.

        Args:
            xliff_content (str): The XLIFF content as a string.
            translate_func (Optional[Callable]):
                A function that translates the source text. It can take an optional argument
                `already_translated` and `old_translation` for updating existing translations.

        Returns:
            bytes: The modified XLIFF content with target tags, encoded as UTF-8.
        """
        namespace = get_namespace_from_xliff(xliff_content)

        ET.register_namespace("", namespace["ns"])
        tree = ET.ElementTree(ET.fromstring(xliff_content))
        root = tree.getroot()

        # Segment is always parent of source/target - no need to find parents
        for segment in root.findall(".//ns:segment", namespaces=namespace):
            source = segment.find("ns:source", namespaces=namespace)
            if source is not None and "".join(source.itertext()).strip():
                to_translate = "".join(source.itertext()).strip()
                target = segment.find("ns:target", namespaces=namespace)
                if target is None:
                    target = ET.Element("target")
                    segment.append(target)
                if not target.text or not target.text.strip():
                    target.text = translate_func(to_translate)
                else:
                    old_translation = "".join(target.itertext()).strip()
                    target.text = translate_func(
                        to_translate=to_translate,
                        already_translated=True,
                        old_translation=old_translation,
                    )

        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    def get_metadata_localization(
        self,
        workspace_id: str,
        target_language: str,
    ) -> bytes:
        """Retrieve the metadata localization for a workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to retrieve the metadata localization.
            target_language (str): The target language code for the localization.

        Returns:
            bytes: The encoded metadata localization in the target language.
        """
        ans = self._actions_api.retrieve_translations(
            workspace_id=workspace_id,
            locale_request=LocaleRequest(locale=target_language),
            _preload_content=False,
        )
        return ans.data

    def set_metadata_localization(
        self,
        workspace_id: str,
        encoded_xml: bytes,
    ) -> None:
        """Set the metadata localization for a workspace.

        Args:
            workspace_id (str): The ID of the workspace to which the metadata localization applies.
            encoded_xml (bytes): The encoded XML metadata to be set.

        Returns:
            None
        """
        self._client.do_request(
            method=HttpMethod.POST,
            endpoint=f"api/v1/actions/workspaces/{workspace_id}/translations/set",
            content_type="application/xml",
            data=encoded_xml,
        )

    def clean_metadata_localization(
        self,
        workspace_id: str,
        target_language: str,
    ) -> None:
        """Clean the metadata localization for a workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to clean the metadata localization.
            target_language (str): The target language code for the localization to be cleaned.

        Returns:
            None
        """
        self._client.actions_api.clean_translations(
            workspace_id=workspace_id, locale_request=LocaleRequest(target_language)
        )

    def add_metadata_locale(
        self,
        workspace_id: str,
        target_language: str,
        translator_func: Callable,
        set_locale: bool = True,
    ) -> None:
        """Add and optionally set the metadata localization for a workspace in a target language.

        Args:
            workspace_id (str): The ID of the workspace.
            target_language (str): The target language for the metadata localization.
            translator_func (Callable): A function to translate the source text.
            set_locale (bool): Flag to indicate if the locale settings should be updated in the workspace.

        Returns:
            None
        """
        ans = self._actions_api.retrieve_translations(
            workspace_id=workspace_id,
            locale_request=LocaleRequest(locale=target_language),
            _preload_content=False,
        )

        encoded_xml = self._add_target_tags(ans.data.decode(), translator_func)

        self.set_metadata_localization(workspace_id=workspace_id, encoded_xml=encoded_xml)
        if set_locale:
            metadata_locale = "METADATA_LOCALE"
            locale = "LOCALE"

            self.create_or_update_workspace_setting(
                workspace_id,
                CatalogWorkspaceSetting(
                    id=metadata_locale, setting_type=metadata_locale, content={"value": target_language}
                ),
            )
            self.create_or_update_workspace_setting(
                workspace_id,
                CatalogWorkspaceSetting(id=locale, setting_type=locale, content={"value": target_language}),
            )

    def save_metadata_locale_to_disk(self, workspace_id: str, target_language: str, file_path: Path) -> None:
        """Save the metadata localization for a workspace to a file.

        Args:
            workspace_id (str): The ID of the workspace.
            target_language (str): The target language for the metadata localization.
            file_path (Path): The path to the file where the XLIFF content will be saved.

        Returns:
            None
        """
        xliff_content = self.get_metadata_localization(workspace_id, target_language)

        ns = get_namespace_from_xliff(xliff_content.decode())

        ET.register_namespace("", ns["ns"])
        tree = ET.ElementTree(ET.fromstring(xliff_content))

        tree.write(file_path, "utf-8")

    def set_metadata_locale_from_disk(self, workspace_id: str, file_path: Path) -> None:
        """Load and set the metadata localization for a workspace from a file.

        Args:
            workspace_id (str): The ID of the workspace to which the metadata localization applies.
            file_path (Path): The path to the file containing the encoded XML metadata.

        Returns:
            None
        """
        with open(file_path, "rb") as f:
            encoded_xml = f.read()
            self.set_metadata_localization(workspace_id=workspace_id, encoded_xml=encoded_xml)

    # Declarative methods - workspace data filters

    def get_declarative_workspace_data_filters(self) -> CatalogDeclarativeWorkspaceDataFilters:
        """Retrieve a workspace data filers layout.

        Args:
            None

        Returns:
            CatalogDeclarativeWorkspaceDataFilters:
                Object containing List of declarative workspace data filters.
        """
        return CatalogDeclarativeWorkspaceDataFilters.from_api(self._layout_api.get_workspace_data_filters_layout())

    def put_declarative_workspace_data_filters(
        self, workspace_data_filters: CatalogDeclarativeWorkspaceDataFilters
    ) -> None:
        """Set workspace data filters layout.

        Args:
            workspace_data_filters (CatalogDeclarativeWorkspaceDataFilters):
                Object containing List of declarative workspace data filters.

        Returns:
            None
        """
        self._layout_api.set_workspace_data_filters_layout(
            declarative_workspace_data_filters=workspace_data_filters.to_api()
        )

    def store_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        """Store workspace data filters layout in a directory hierarchy.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_workspace_data_filters().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_workspace_data_filters(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeWorkspaceDataFilters:
        """Loads workspace data filters layout, which was stored using `store_declarative_workspace_data_filters`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeWorkspaceDataFilters:
                Object containing List of declarative workspace data filters.
        """
        return CatalogDeclarativeWorkspaceDataFilters.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_workspace_data_filters(self, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_workspace_data_filters`.

        This method combines `load_declarative_workspace_data_filters` and `put_declarative_workspace_data_filters`
        methods to load and set layouts stored using `store_declarative_workspace_data_filters`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_workspace_data_filters = CatalogDeclarativeWorkspaceDataFilters.load_from_disk(
            self.layout_organization_folder(layout_root_path)
        )
        self.put_declarative_workspace_data_filters(declarative_workspace_data_filters)

    def list_user_data_filters(self, workspace_id: str) -> list[CatalogUserDataFilter]:
        """list all user data filers.

        Args:
            workspace_id (str):
                String containing id of the workspace.

        Returns:
            list[CatalogUserDataFilter]:
                List of user data filter entities.
        """
        get_user_data_filters = functools.partial(
            self._entities_api.get_all_entities_user_data_filters,
            workspace_id,
            _check_return_type=False,
            include=["ALL"],
        )
        user_data_filters = load_all_entities_dict(get_user_data_filters, camel_case=False)
        return [CatalogUserDataFilter.from_dict(v, camel_case=False) for v in user_data_filters["data"]]

    def create_or_update_user_data_filter(self, workspace_id: str, user_data_filter: CatalogUserDataFilter) -> None:
        """Create a new user data filter or overwrite an existing one.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            user_data_filter (CatalogUserDataFilter):
                UserDataFilter entity object.

        Returns:
            None
        """
        user_data_filter_document = CatalogUserDataFilterDocument(data=user_data_filter)
        if user_data_filter.id is None:
            self._entities_api.create_entity_user_data_filters(
                workspace_id=workspace_id,
                json_api_user_data_filter_post_optional_id_document=user_data_filter_document.to_api(True),
            )
        else:
            try:
                self.get_user_data_filter(workspace_id=workspace_id, user_data_filter_id=user_data_filter.id)
                self._entities_api.update_entity_user_data_filters(
                    workspace_id=workspace_id,
                    object_id=user_data_filter.id,
                    json_api_user_data_filter_in_document=user_data_filter_document.to_api(),
                )
            except NotFoundException:
                self._entities_api.create_entity_user_data_filters(
                    workspace_id=workspace_id,
                    json_api_user_data_filter_post_optional_id_document=user_data_filter_document.to_api(True),
                )

    def get_user_data_filter(self, workspace_id: str, user_data_filter_id: str) -> CatalogUserDataFilter:
        """Get user data filter by its id.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            user_data_filter_id (str):
                String containing id of the user data filter.

        Returns:
            CatalogUserDataFilter:
                UserDataFilter entity object.
        """
        user_data_filter_dict = self._entities_api.get_entity_user_data_filters(
            workspace_id=workspace_id,
            object_id=user_data_filter_id,
            include=["ALL"],
            _check_return_type=False,
        ).data

        return CatalogUserDataFilter.from_dict(user_data_filter_dict, camel_case=True)

    def delete_user_data_filter(self, workspace_id: str, user_data_filter_id: str) -> None:
        """Delete user data filter.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            user_data_filter_id (str):
                String containing id of the deleting user data filter.

        Returns:
            None
        """
        self._entities_api.delete_entity_user_data_filters(workspace_id=workspace_id, object_id=user_data_filter_id)

    def get_declarative_user_data_filters(self, workspace_id: str) -> CatalogDeclarativeUserDataFilters:
        """Retrieve a user data filers layout.

        Args:
            workspace_id (str):
                String containing id of the workspace

        Returns:
            CatalogDeclarativeUserDataFilters:
                Object containing List of declarative user data filters.
        """
        return CatalogDeclarativeUserDataFilters.from_api(self._layout_api.get_user_data_filters(workspace_id))

    def put_declarative_user_data_filters(
        self, workspace_id: str, user_data_filters: CatalogDeclarativeUserDataFilters
    ) -> None:
        """Set user data filters layout.

        Args:
            workspace_id (str):
                String containing id of the workspace
            user_data_filters (CatalogDeclarativeUserDataFilters):
                Object containing List of declarative user data filters.

        Returns:
            None
        """
        self._layout_api.set_user_data_filters(
            workspace_id=workspace_id, declarative_user_data_filters=user_data_filters.to_api()
        )

    def store_declarative_user_data_filters(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store user data filters layout in a directory hierarchy.

        Args:
            workspace_id (str):
                id of the related workspace
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        self.get_declarative_user_data_filters(workspace_id).store_to_disk(
            self.layout_organization_folder(layout_root_path)
        )

    def load_declarative_user_data_filters(
        self, layout_root_path: Path = Path.cwd()
    ) -> CatalogDeclarativeUserDataFilters:
        """Loads user data filters layout, which was stored using `store_declarative_user_data_filters`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            CatalogDeclarativeUserDataFilters:
                Object containing List of declarative user data filters.
        """
        return CatalogDeclarativeUserDataFilters.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_user_data_filters(
        self, workspace_id: str, layout_root_path: Path = Path.cwd()
    ) -> None:
        """Loads and sets the layouts stored using `store_declarative_user_data_filters`.

        This method combines `load_declarative_user_data_filters` and `put_declarative_user_data_filters`
        methods to load and set layouts stored using `store_declarative_user_data_filters`.

        Args:
            workspace_id (str):
                String containing id of the workspace
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_user_data_filters = CatalogDeclarativeUserDataFilters.load_from_disk(
            self.layout_organization_folder(layout_root_path)
        )
        self.put_declarative_user_data_filters(workspace_id, declarative_user_data_filters)

    def get_declarative_automations(self, workspace_id: str) -> list[CatalogDeclarativeAutomation]:
        """Retrieve a list of declarative automations.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogDeclarativeAutomation]:
                List of declarative automations.
        """
        return [
            CatalogDeclarativeAutomation.from_dict(automation.to_dict())
            for automation in self._layout_api.get_automations(workspace_id)
        ]

    def put_declarative_automations(self, workspace_id: str, automations: list[CatalogDeclarativeAutomation]) -> None:
        """Set automations for the workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            automations (list[CatalogDeclarativeAutomation]):
                List of declarative automations.
        Returns:
            None
        """
        api_automations = [automation.to_api() for automation in automations]
        self._layout_api.set_automations(workspace_id, api_automations)

    def list_filters_views(self, workspace_id: str) -> list[CatalogFilterView]:
        """list all filter views.

        Args:
            workspace_id (str):
                String containing id of the workspace.

        Returns:
            list[CatalogFilterView]:
                List of filter view entities.
        """
        get_filter_views = functools.partial(
            self._entities_api.get_all_entities_filter_views,
            workspace_id,
            _check_return_type=False,
            include=["ALL"],
        )
        filter_views = load_all_entities_dict(get_filter_views, camel_case=False)
        return [CatalogFilterView.from_dict(v, camel_case=False) for v in filter_views["data"]]

    def create_or_update_filter_view(self, workspace_id: str, filter_view: CatalogFilterView) -> None:
        """Create a new filter view or overwrite an existing one.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            filter_view (CatalogFilterView):
                FilterView entity object.

        Returns:
            None
        """
        filter_view_document = CatalogFilterViewDocument(data=filter_view)
        if filter_view.id is None:
            self._entities_api.create_entity_filter_views(
                workspace_id=workspace_id,
                json_api_filter_view_in_document=filter_view_document.to_api(),
            )
        else:
            try:
                self.get_filter_view(workspace_id=workspace_id, filter_view_id=filter_view.id)
                self._entities_api.update_entity_filter_views(
                    workspace_id=workspace_id,
                    object_id=filter_view.id,
                    json_api_filter_view_in_document=filter_view_document.to_api(),
                )
            except NotFoundException:
                self._entities_api.create_entity_filter_views(
                    workspace_id=workspace_id,
                    json_api_filter_view_in_document=filter_view_document.to_api(),
                )

    def get_filter_view(self, workspace_id: str, filter_view_id: str) -> CatalogFilterView:
        """Get filter view by its id.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            filter_view_id (str):
                String containing id of the filter view.

        Returns:
            CatalogFilterView:
                FilterView entity object.
        """
        filter_view_dict = self._entities_api.get_entity_filter_views(
            workspace_id=workspace_id,
            object_id=filter_view_id,
            include=["ALL"],
            _check_return_type=False,
        ).data

        return CatalogFilterView.from_dict(filter_view_dict, camel_case=True)

    def delete_filter_view(self, workspace_id: str, filter_view_id: str) -> None:
        """Delete filter view.

        Args:
            workspace_id (str):
                String containing id of the workspace.
            filter_view_id (str):
                String containing id of the deleting filter view.

        Returns:
            None
        """
        self._entities_api.delete_entity_filter_views(workspace_id=workspace_id, object_id=filter_view_id)

    def get_declarative_filter_views(self, workspace_id: str) -> list[CatalogDeclarativeFilterView]:
        """Retrieve a list of declarative filter views.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"

        Returns:
            list[CatalogDeclarativeFilterView]:
                List of declarative filter views.
        """
        return [
            CatalogDeclarativeFilterView.from_dict(filter_view.to_dict(), camel_case=False)
            for filter_view in self._layout_api.get_filter_views(workspace_id)
        ]

    def put_declarative_filter_views(self, workspace_id: str, filter_views: list[CatalogDeclarativeFilterView]) -> None:
        """Set filter views for the workspace.

        Args:
            workspace_id (str):
                Workspace identification string e.g. "demo"
            filter_views (list[CatalogDeclarativeFilterView]):
                List of declarative filter views.

        Returns:
            None
        """
        api_filter_views = [filter_view.to_api() for filter_view in filter_views]
        self._layout_api.set_filter_views(workspace_id=workspace_id, declarative_filter_view=api_filter_views)

    def store_declarative_filter_views(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Store filter views layout in a directory hierarchy.

        Args:
            workspace_id (str):
                id of the related workspace
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        filter_views = self.get_declarative_filter_views(workspace_id)
        CatalogDeclarativeFilterView.store_filter_views_to_disk(
            filter_views, self.layout_organization_folder(layout_root_path)
        )

    def load_declarative_filter_views(self, layout_root_path: Path = Path.cwd()) -> list[CatalogDeclarativeFilterView]:
        """Loads filter views layout, which was stored using `store_declarative_filter_views`.

        Args:
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            list[CatalogDeclarativeFilterView]:
                List of declarative filter views.
        """
        return CatalogDeclarativeFilterView.load_filter_views_from_disk(
            self.layout_organization_folder(layout_root_path)
        )

    def load_and_put_declarative_filter_views(self, workspace_id: str, layout_root_path: Path = Path.cwd()) -> None:
        """Loads and sets the layouts stored using `store_declarative_filter_views`.

        This method combines `load_declarative_filter_views` and `put_declarative_filter_views`
        methods to load and set layouts stored using `store_declarative_filter_views`.

        Args:
            workspace_id (str):
                String containing id of the workspace
            layout_root_path (Path, optional):
                Path to the root of the layout directory. Defaults to Path.cwd().

        Returns:
            None
        """
        declarative_filter_views = CatalogDeclarativeFilterView.load_filter_views_from_disk(
            self.layout_organization_folder(layout_root_path)
        )
        self.put_declarative_filter_views(workspace_id, declarative_filter_views)
