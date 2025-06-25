# (C) 2025 GoodData Corporation

"""Provisioning base class for GoodData Pipelines."""

from pathlib import Path
from typing import Generic, Type, TypeVar

from gooddata_sdk.utils import PROFILES_FILE_PATH, profile_content

from gooddata_pipelines.api import GoodDataAPI
from gooddata_pipelines.logger.logger import (
    LogObserver,
)

TSourceData = TypeVar("TSourceData")


class Provisioning(Generic[TSourceData]):
    """Base provisioning class."""

    TProvisioning = TypeVar("TProvisioning", bound="Provisioning")

    def __init__(self, host: str, token: str) -> None:
        self.source_id: set[str] = set()
        self.upstream_id: set[str] = set()
        self._api = GoodDataAPI(host, token)
        self.logger: LogObserver = LogObserver()
        self.fatal_exception: str = ""

    @classmethod
    def create(
        cls: Type[TProvisioning], host: str, token: str
    ) -> TProvisioning:
        """Creates a provisioner instance using provided host and token."""
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
    def _create_groups(
        source_id: set[str], panther_id: set[str]
    ) -> tuple[set[str], set[str], set[str]]:
        """Creates groups for provisioning.

        Sorts the IDs into three categories:
        - IDs that exist both source and upstream (to be checked further)
        - IDs that exist upstream but not in source (to be deleted)
        - IDs that exist in source but not upstream (to be created)
        """
        ids_in_both_systems: set[str] = source_id.intersection(panther_id)
        ids_to_delete: set[str] = panther_id.difference(source_id)
        ids_to_create: set[str] = source_id.difference(panther_id)

        return ids_in_both_systems, ids_to_delete, ids_to_create

    def _provision(self) -> None:
        raise NotImplementedError(
            "Provisioning method to be implemented in the subclass."
        )

    def provision(self, source_data: list[TSourceData]) -> None:
        """Runs the provisioning workflow with the provided source data."""
        self.source_group: list[TSourceData] = source_data

        try:
            self._provision()
            self.logger.info("Provisioning completed successfully.")
        except Exception as e:
            self.fatal_exception = str(e)
            self.logger.error(
                f"Provisioning failed. Error: {self.fatal_exception} "
                + f"Context: {e.__dict__}"
            )
