# (C) 2023 GoodData Corporation
import logging
import sys
from pathlib import Path
from time import time
from typing import List, Optional

import yaml
from gooddata_dbt.args import parse_arguments
from gooddata_dbt.dbt.profiles import DbtOutput, DbtProfiles
from gooddata_dbt.dbt.tables import DbtModelTables
from gooddata_dbt.gooddata.config import GoodDataConfig, GoodDataConfigProduct
from gooddata_dbt.logger import get_logger
from gooddata_dbt.sdk_wrapper import GoodDataSdkWrapper

from gooddata_sdk import (
    CatalogDeclarativeModel,
    CatalogDeclarativeTables,
    CatalogScanModelRequest,
    CatalogWorkspace,
    GoodDataSdk,
)

GOODDATA_LAYOUTS_DIR = Path("gooddata_layouts")

# TODO
#   Tests, ...


def layout_model_path(data_product: GoodDataConfigProduct) -> Path:
    return GOODDATA_LAYOUTS_DIR / data_product.id


def generate_and_put_pdm(
    logger: logging.Logger, sdk: GoodDataSdk, data_source_id: str, dbt_tables: DbtModelTables
) -> None:
    # Construct GoodData PDM from dbt models and put it to the server
    # GoodData caches the metadata to reduce querying them (costly) in runtime.
    scan_request = CatalogScanModelRequest(scan_tables=True, scan_views=True)
    logger.info(f"Scan data source {data_source_id=}")
    scan_pdm = sdk.catalog_data_source.scan_data_source(data_source_id, scan_request, report_warnings=True).pdm

    logger.info(f"Generate and put PDM {data_source_id=}")
    pdm = dbt_tables.make_pdm(scan_pdm)
    declarative_tables = CatalogDeclarativeTables.from_dict(pdm, camel_case=False)
    sdk.catalog_data_source.put_declarative_pdm(data_source_id, declarative_tables)


def generate_and_put_ldm(
    sdk: GoodDataSdk, data_source_id: str, workspace_id: str, dbt_tables: DbtModelTables, model_ids: Optional[List[str]]
) -> None:
    # Construct GoodData LDM from dbt models
    declarative_datasets = dbt_tables.make_declarative_datasets(data_source_id, model_ids)
    ldm = CatalogDeclarativeModel.from_dict({"ldm": declarative_datasets}, camel_case=False)

    # Deploy logical into target workspace
    sdk.catalog_workspace_content.put_declarative_ldm(workspace_id, ldm)


def register_data_source(
    logger: logging.Logger, sdk: GoodDataSdk, data_source_id: str, dbt_target: DbtOutput, dbt_tables: DbtModelTables
) -> None:
    logger.info(f"Register data source {data_source_id=} schema={dbt_tables.schema_name}")
    data_source = dbt_target.to_gooddata(data_source_id, dbt_tables.schema_name)
    sdk.catalog_data_source.create_or_update_data_source(data_source)

    logger.info("Generate and put PDM")
    generate_and_put_pdm(logger, sdk, data_source_id, dbt_tables)


def create_workspace(logger: logging.Logger, sdk: GoodDataSdk, workspace_id: str, workspace_title: str) -> None:
    logger.info(f"Create workspace {workspace_id=} {workspace_title=}")
    # Create workspaces, if they do not exist yet, otherwise update them
    workspace = CatalogWorkspace(workspace_id=workspace_id, name=workspace_title)
    sdk.catalog_workspace.create_or_update(workspace=workspace)


def deploy_ldm(
    logger: logging.Logger,
    sdk: GoodDataSdk,
    data_source_id: str,
    dbt_tables: DbtModelTables,
    model_ids: Optional[List[str]],
    workspace_id: str,
) -> None:
    logger.info("Generate and put LDM")
    generate_and_put_ldm(sdk, data_source_id, workspace_id, dbt_tables, model_ids)


def upload_notification(logger: logging.Logger, sdk: GoodDataSdk, data_source_id: str) -> None:
    logger.info(f"Upload notification {data_source_id=}")
    sdk.catalog_data_source.register_upload_notification(data_source_id)


def deploy_analytics(
    logger: logging.Logger, sdk: GoodDataSdk, workspace_id: str, data_product: GoodDataConfigProduct
) -> None:
    logger.info(f"Deploy analytics {workspace_id=}")

    logger.info("Read analytics model from disk")
    adm = sdk.catalog_workspace_content.load_analytics_model_from_disk(layout_model_path(data_product))

    # Deploy analytics model into target workspace
    logger.info("Load analytics model into GoodData")
    sdk.catalog_workspace_content.put_declarative_analytics_model(workspace_id, adm)


def store_analytics(
    logger: logging.Logger, sdk: GoodDataSdk, workspace_id: str, data_product: GoodDataConfigProduct
) -> None:
    logger.info("Store analytics model to disk")
    sdk.catalog_workspace_content.store_analytics_model_to_disk(workspace_id, layout_model_path(data_product))


def test_insights(logger: logging.Logger, sdk: GoodDataSdk, workspace_id: str) -> None:
    logger.info(f"Test insights {workspace_id=}")
    insights = sdk.insights.get_insights(workspace_id)

    for insight in insights:
        try:
            start = time()
            sdk.tables.for_insight(workspace_id, insight)
            duration = int((time() - start) * 1000)
            logger.info(f'Test successful insight="{insight.title}" duration={duration}(ms) ...')
        except RuntimeError:
            sys.exit()


def create_localized_workspaces(data_product: GoodDataConfigProduct, sdk: GoodDataSdk, workspace_id: str) -> None:
    if data_product.localization is None:
        return
    for to in data_product.localization.to:
        from deep_translator import GoogleTranslator

        translator_func = GoogleTranslator(
            source=data_product.localization.from_language, target=to.language
        ).translate_batch
        logging.info(f"create_localized_workspaces layout_root_path={GOODDATA_LAYOUTS_DIR / data_product.id}")
        sdk.catalog_workspace.generate_localized_workspaces(
            workspace_id,
            to_lang=to.language,
            to_locale=to.locale,
            from_lang=data_product.localization.from_language,
            translator_func=translator_func,
            provision_workspace=True,
            store_layouts=False,
            layout_root_path=GOODDATA_LAYOUTS_DIR / data_product.id,
        )


def main() -> None:
    args = parse_arguments("gooddata-dbt plugin for models management and invalidating caches(upload notification)")
    logger = get_logger("gooddata-dbt", args.debug)
    logger.info("Start")
    sdk = GoodDataSdkWrapper(args, logger).sdk
    with open("gooddata.yml") as fp:
        gd_config = GoodDataConfig.from_dict(yaml.safe_load(fp))

    if args.method in ["upload_notification", "deploy_models"]:
        dbt_target = DbtProfiles(args).target
        data_source_id = dbt_target.name
        if args.method == "upload_notification":
            # Caches are invalidated only per data source, not per data product
            upload_notification(logger, sdk, data_source_id)
        else:
            dbt_tables = DbtModelTables.from_local(args.gooddata_upper_case, gd_config.all_model_ids)
            if args.gooddata_upper_case:
                dbt_target.schema = dbt_target.schema.upper()
                dbt_target.database = dbt_target.database.upper()
            register_data_source(logger, sdk, data_source_id, dbt_target, dbt_tables)
            for data_product in gd_config.data_products:
                logger.info(f"Process product name={data_product.name}")
                environments = gd_config.get_environment_workspaces(data_product.environment_setup_id)
                for environment in environments:
                    if environment.id == args.gooddata_environment_id:
                        workspace_id = f"{data_product.id}_{environment.id}"
                        workspace_title = f"{data_product.name} ({environment.name})"
                        create_workspace(logger, sdk, workspace_id, workspace_title)
                        deploy_ldm(logger, sdk, data_source_id, dbt_tables, data_product.model_ids, workspace_id)
                        if data_product.localization:
                            create_localized_workspaces(data_product, sdk, workspace_id)
    else:
        for data_product in gd_config.data_products:
            logger.info(f"Process product name={data_product.name}")
            environments = gd_config.get_environment_workspaces(data_product.environment_setup_id)
            for environment in environments:
                if environment.id == args.gooddata_environment_id:
                    workspace_id = f"{data_product.id}_{environment.id}"
                    if args.method == "store_analytics":
                        store_analytics(logger, sdk, workspace_id, data_product)
                    elif args.method == "deploy_analytics":
                        deploy_analytics(logger, sdk, workspace_id, data_product)
                    elif args.method == "test_insights":
                        test_insights(logger, sdk, workspace_id)
                    else:
                        raise Exception(f"Unsupported method requested in args: {args.method}")

    logger.info("End")
