# (C) 2023 GoodData Corporation
import logging
from pathlib import Path
from typing import Any, List, Union

from gooddata_dbt.gooddata.config import GoodDataConfigLocalizationTo, GoodDataConfigProduct

from gooddata_sdk import (
    CatalogDataSourcePostgres,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    CatalogDeclarativeAnalytics,
    CatalogDeclarativeColumn,
    CatalogDeclarativeModel,
    CatalogDeclarativeTable,
    CatalogDeclarativeTables,
    CatalogScanModelRequest,
    CatalogWorkspace,
    GoodDataSdk,
    Insight,
)

DataSource = Union[CatalogDataSourcePostgres, CatalogDataSourceSnowflake, CatalogDataSourceVertica]


class GoodDataApiWrapper:
    def __init__(self, sdk: GoodDataSdk, logger: logging.Logger, dry_run: bool = False) -> None:
        self.sdk = sdk
        self.logger = logger
        self.dry_run = dry_run

    def get_insights(self, workspace_id: str) -> List[Insight]:
        if self.dry_run:
            self.logger.info("Dry run - skipping insights listing")
            return []
        else:
            return self.sdk.insights.get_insights(workspace_id)

    def execute_insight(self, workspace_id: str, insight: Insight) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping insights execution")
        else:
            self.sdk.tables.for_insight(workspace_id, insight)

    def scan_data_source(self, data_source_id: str, scan_request: CatalogScanModelRequest) -> CatalogDeclarativeTables:
        if self.dry_run:
            self.logger.info("Dry run - skipping data source scanning")
            return CatalogDeclarativeTables(
                tables=[
                    CatalogDeclarativeTable(
                        id="dry_run",
                        type="DATA_SOURCE_TABLE",
                        path=["table"],
                        columns=[CatalogDeclarativeColumn(name="dry_run", data_type="STRING")],
                    )
                ]
            )
        else:
            return self.sdk.catalog_data_source.scan_data_source(data_source_id, scan_request, report_warnings=True).pdm

    def put_declarative_ldm(self, workspace_id: str, declarative_ldm: CatalogDeclarativeModel) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping declarative LDM put")
        else:
            self.sdk.catalog_workspace_content.put_declarative_ldm(workspace_id, declarative_ldm)

    def create_workspace(self, workspace: CatalogWorkspace) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping workspace creation")
        else:
            self.sdk.catalog_workspace.create_or_update(workspace=workspace)

    def create_or_update_data_source(self, data_source: DataSource) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping data source creation")
        else:
            self.sdk.catalog_data_source.create_or_update_data_source(data_source)

    def register_upload_notification(self, data_source_id: str) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping upload notification registration")
        else:
            self.sdk.catalog_data_source.register_upload_notification(data_source_id)

    def put_declarative_analytics_model(self, workspace_id: str, adm: CatalogDeclarativeAnalytics) -> None:
        if self.dry_run:
            self.logger.info("Dry run - skipping declarative analytics model put")
        else:
            self.sdk.catalog_workspace_content.put_declarative_analytics_model(workspace_id, adm)

    def generate_localized_workspaces(
        self,
        workspace_id: str,
        to: GoodDataConfigLocalizationTo,
        data_product: GoodDataConfigProduct,
        translator_func: Any,
        layout_path: Path,
        provision_workspace: bool = True,
        store_layouts: bool = False,
    ) -> None:
        from_language = "en"
        if data_product.localization is not None:
            from_language = data_product.localization.from_language
        if self.dry_run:
            self.logger.info("Dry run - skipping localized workspaces generation")
        else:
            self.sdk.catalog_workspace.generate_localized_workspaces(
                workspace_id,
                to_lang=to.language,
                to_locale=to.locale,
                from_lang=from_language,
                translator_func=translator_func,
                layout_root_path=layout_path,
                provision_workspace=provision_workspace,
                store_layouts=store_layouts,
            )
