# (C) 2025 GoodData Corporation

"""Provisioning base class for GoodData Pipelines."""

from pathlib import Path
from typing import Generic, Type, TypeVar

from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content

from gooddata_pipelines.api import GoodDataApi
from gooddata_pipelines.logger.logger import (
    LogObserver,
)
from gooddata_pipelines.provisioning.utils.utils import EntityGroupIds

TFullLoadSourceData = TypeVar("TFullLoadSourceData")
TIncrementalSourceData = TypeVar("TIncrementalSourceData")


class Provisioning(Generic[TFullLoadSourceData, TIncrementalSourceData]):
    """Base provisioning class."""

    TProvisioning = TypeVar("TProvisioning", bound="Provisioning")
    source_group_full: list[TFullLoadSourceData]
    source_group_incremental: list[TIncrementalSourceData]

    def __init__(self, host: str, token: str) -> None:
        self.source_id: set[str] = set()
        self.upstream_id: set[str] = set()
        self._api = GoodDataApi(host, token)
        self.logger: LogObserver = LogObserver()
        self.fatal_exception: str = ""

    @classmethod
    def create(
        cls: Type[TProvisioning], host: str, token: str
    ) -> TProvisioning:
        """Creates a provisioner instance using provided host and token."""
        cls._validate_credentials(host, token)
        return cls(host=host, token=token)

    @classmethod
    def create_from_profile(
        cls: Type[TProvisioning],
        profile: str = "default",
        profiles_path: Path = PROFILES_FILE_PATH,
    ) -> TProvisioning:
        """Creates a provisioner instance using a GoodData profile file."""
        content = profile_content(profile, profiles_path)
        return cls(**content)

    @staticmethod
    def _validate_credentials(host: str, token: str) -> None:
        """Validates the credentials."""
        if (not host) and (not token):
            raise ValueError("Host and token are required.")
        if not host:
            raise ValueError("Host is required.")
        if not token:
            raise ValueError("Token is required.")

    @staticmethod
    def _create_groups(
        source_id: set[str], panther_id: set[str]
    ) -> EntityGroupIds:
        """Creates groups for provisioning as sets of IDs.

        Sorts the IDs into three categories:
        - IDs that exist both source and upstream (to be checked further)
        - IDs that exist upstream but not in source (to be deleted)
        - IDs that exist in source but not upstream (to be created)
        """
        ids_in_both_systems: set[str] = source_id.intersection(panther_id)
        ids_to_delete: set[str] = panther_id.difference(source_id)
        ids_to_create: set[str] = source_id.difference(panther_id)

        return EntityGroupIds(
            ids_in_both_systems=ids_in_both_systems,
            ids_to_delete=ids_to_delete,
            ids_to_create=ids_to_create,
        )

    def _provision_incremental_load(self) -> None:
        raise NotImplementedError(
            "Provisioning method to be implemented in the subclass."
        )

    def _provision_full_load(self) -> None:
        raise NotImplementedError(
            "Provisioning method to be implemented in the subclass."
        )

    def full_load(self, source_data: list[TFullLoadSourceData]) -> None:
        """Runs full provisioning workflow with the provided source data.

        Full provisioning is a full load of the source data, where the source data
        is assumed to a single source of truth and the upstream workspaces are updated
        to match it.

        That means:
        - All workspaces declared in the source data are created if missing, or
        updated to match the source data
        - All workspaces not declared in the source data are deleted
        """
        self.source_group_full = source_data

        try:
            self._provision_full_load()
            self.logger.info("Provisioning completed.")
        except Exception as e:
            self._handle_fatal_exception(e)

    def incremental_load(
        self, source_data: list[TIncrementalSourceData]
    ) -> None:
        """Runs incremental provisioning workflow with the provided source data.

        Incremental provisioning is used to modify a subset of the upstream workspaces
        based on the source data provided.
        """
        # TODO: validate the data type of source group at runtime
        self.source_group_incremental = source_data

        try:
            self._provision_incremental_load()
            self.logger.info("Provisioning completed.")
        except Exception as e:
            self._handle_fatal_exception(e)

    def _handle_fatal_exception(self, e: Exception) -> None:
        """Handles fatal exceptions during provisioning.

        Logs the exception content. Re-raises the exception if there is no
        subscriber to the logger.
        """
        self.fatal_exception = str(e)

        if hasattr(e, "__dict__"):
            exception_context = f"Context: {e.__dict__}"
        else:
            exception_context = ""

        exception_message = (
            f"Provisioning failed. Error: {self.fatal_exception}. "
            + exception_context
        )

        self.logger.error(exception_message)

        if not self.logger.subscribers:
            raise Exception(exception_message)
