# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel


class DataSourceValidator:
    def __init__(self, data_source_service: CatalogDataSourceService):
        self._ds_service = data_source_service

    def validate_ldm(self, model: CatalogDeclarativeModel) -> None:
        """
        Validates that referenced data sources in LDM actually exist.
        If they do not exist, raises ValueError.

        Returns:
            None
        """
        if model.ldm is not None:
            ldm_ds_in_use = set(
                dataset.data_source_table_id.data_source_id
                for dataset in model.ldm.datasets
                if dataset.data_source_table_id is not None
            )
            self.validate_data_source_ids(ldm_ds_in_use)

    def validate_data_source_ids(self, data_source_ids: set[str]) -> None:
        """
        Compares data source ids with existing data sources in the catalog.

        Returns:
            None
        """
        full_ds_set = set(data_source.id for data_source in self._ds_service.list_data_sources())
        diff_ds = data_source_ids - full_ds_set
        if len(diff_ds) != 0:
            raise ValueError(
                f"There are not existing data source ids in data source mapping. "
                f"These data source ids does not exist {', '.join(diff_ds)}"
            )
