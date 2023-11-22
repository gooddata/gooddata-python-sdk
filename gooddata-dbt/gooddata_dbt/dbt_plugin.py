# (C) 2023 GoodData Corporation
import asyncio
import logging
import os
from argparse import Namespace
from asyncio import Semaphore
from pathlib import Path
from time import time
from typing import List, Optional

import tabulate
import yaml
from gooddata_dbt.args import parse_arguments
from gooddata_dbt.dbt.cloud import DbtConnection, DbtCredentials, DbtExecution
from gooddata_dbt.dbt.profiles import DbtProfiles
from gooddata_dbt.dbt.tables import DbtModelTables
from gooddata_dbt.gooddata.api_wrapper import GoodDataApiWrapper
from gooddata_dbt.gooddata.config import GoodDataConfig, GoodDataConfigOrganization, GoodDataConfigProduct
from gooddata_dbt.logger import get_logger
from gooddata_dbt.sdk_wrapper import GoodDataSdkWrapper
from gooddata_dbt.utils import get_duration, report_message_to_merge_request

from gooddata_sdk import CatalogDeclarativeModel, CatalogScanModelRequest, CatalogWorkspace, GoodDataSdk, Insight

# TODO - upgrade AIO, cleanup, start from scratch, test everything

GOODDATA_LAYOUTS_DIR = Path("gooddata_layouts")


def layout_model_path(data_product: GoodDataConfigProduct) -> Path:
    return GOODDATA_LAYOUTS_DIR / data_product.id


def generate_and_put_ldm(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    data_source_id: str,
    workspace_id: str,
    dbt_tables: DbtModelTables,
    model_ids: Optional[List[str]],
) -> None:
    scan_request = CatalogScanModelRequest(scan_tables=True, scan_views=True)
    logger.info(f"Scan data source {data_source_id=}")
    scan_pdm = sdk_wrapper.sdk_facade.scan_data_source(data_source_id, scan_request)
    scan_pdm.store_to_disk(Path("test"))
    # Store data types to dbt_tables class. It is used in make_declarative_datasets to inject data types to LDM.
    dbt_tables.set_data_types(scan_pdm, sdk_wrapper.sdk_facade.dry_run)
    # Construct GoodData LDM from dbt models
    declarative_datasets = dbt_tables.make_declarative_datasets(data_source_id, model_ids)
    ldm = CatalogDeclarativeModel.from_dict({"ldm": declarative_datasets}, camel_case=False)
    # Deploy logical into target workspace
    sdk_wrapper.sdk_facade.put_declarative_ldm(workspace_id, ldm)


def create_workspace(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    workspace_id: str,
    workspace_title: str,
) -> None:
    logger.info(f"Create workspace {workspace_id=} {workspace_title=}")
    # Create workspaces, if they do not exist yet, otherwise update them
    workspace = CatalogWorkspace(workspace_id=workspace_id, name=workspace_title)
    sdk_wrapper.sdk_facade.create_workspace(workspace=workspace)


def deploy_ldm(
    logger: logging.Logger,
    args: Namespace,
    all_model_ids: List[str],
    sdk_wrapper: GoodDataSdkWrapper,
    model_ids: Optional[List[str]],
    workspace_id: str,
) -> None:
    logger.info("Generate and put LDM")
    dbt_profiles = DbtProfiles(args)
    data_source_id = dbt_profiles.data_source_id
    dbt_tables = DbtModelTables.from_local(args.gooddata_upper_case, all_model_ids)
    generate_and_put_ldm(logger, sdk_wrapper, data_source_id, workspace_id, dbt_tables, model_ids)
    workspace_url = f"{sdk_wrapper.get_host_from_sdk()}/modeler/#/{workspace_id}"
    logger.info(f"LDM successfully loaded, verify here: {workspace_url}")


def register_data_source(
    logger: logging.Logger,
    args: Namespace,
    all_model_ids: List[str],
    sdk_wrapper: GoodDataSdkWrapper,
) -> None:
    dbt_profiles = DbtProfiles(args)
    dbt_target = dbt_profiles.target
    data_source_id = dbt_profiles.data_source_id
    logger.info(f"Process data source {data_source_id=}")
    dbt_tables = DbtModelTables.from_local(args.gooddata_upper_case, all_model_ids)

    logger.info(f"Register data source {data_source_id=} schema={dbt_tables.schema_name}")
    data_source = dbt_target.to_gooddata(data_source_id, dbt_tables.schema_name)
    sdk_wrapper.sdk_facade.create_or_update_data_source(data_source)


def upload_notification(logger: logging.Logger, sdk_wrapper: GoodDataSdkWrapper, data_source_id: str) -> None:
    logger.info(f"Upload notification {data_source_id=}")
    sdk_wrapper.sdk_facade.register_upload_notification(data_source_id)


def deploy_analytics(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    workspace_id: str,
    data_product: GoodDataConfigProduct,
) -> None:
    logger.info(f"Deploy analytics {workspace_id=}")

    logger.info("Read analytics model from disk")
    adm = sdk_wrapper.sdk.catalog_workspace_content.load_analytics_model_from_disk(layout_model_path(data_product))

    # Deploy analytics model into target workspace
    logger.info("Load analytics model into GoodData")
    sdk_wrapper.sdk_facade.put_declarative_analytics_model(workspace_id, adm)

    workspace_url = f"{sdk_wrapper.get_host_from_sdk()}/dashboards/#/workspace/{workspace_id}"
    logger.info(f"Analytics successfully loaded, verify here: {workspace_url}")


def store_analytics(
    logger: logging.Logger, sdk: GoodDataSdk, workspace_id: str, data_product: GoodDataConfigProduct
) -> None:
    logger.info("Store analytics model to disk")
    sdk.catalog_workspace_content.store_analytics_model_to_disk(
        workspace_id,
        layout_model_path(data_product),
        # Exclude attributes related to activities of users, e.g. createdBy
        # When delivering programmatically,
        #   we don't want to transfer info about users and their activities into another environments
        exclude=["ACTIVITY_INFO"],
    )


async def execute_insight(sdk_wrapper: GoodDataSdkWrapper, workspace_id: str, insight: Insight) -> None:
    sdk_wrapper.sdk_facade.execute_insight(workspace_id, insight)


async def test_insight(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    workspace_id: str,
    insight: Insight,
) -> dict:
    logger.info(f"Executing insight {insight.id=} {insight.title=} ...")
    start = time()
    try:
        await execute_insight(sdk_wrapper, workspace_id, insight)
        duration = get_duration(start)
        logger.info(f"Test successful {insight.id=} {insight.title=} duration={duration}(ms)")
        return {"id": insight.id, "title": insight.title, "duration": duration, "status": "success"}
    except Exception as e:
        duration = get_duration(start)
        logger.error(f"Test failed {insight.id=} {insight.title=} duration={duration}(ms) reason={str(e)}")
        return {"id": insight.id, "title": insight.title, "duration": duration, "status": "failed", "reason": str(e)}


async def safe_test_insight(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    workspace_id: str,
    insight: Insight,
    semaphore: Semaphore,
) -> dict:
    async with semaphore:  # semaphore limits num of simultaneous executions
        return await test_insight(
            logger,
            sdk_wrapper,
            workspace_id,
            insight,
        )


async def test_insights(
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    workspace_id: str,
    skip_tests: Optional[List[str]],
    test_insights_parallelism: int = 1,
) -> None:
    start = time()
    logger.info(f"Test insights {workspace_id=}")
    insights = sdk_wrapper.sdk_facade.get_insights(workspace_id)
    semaphore = asyncio.Semaphore(test_insights_parallelism)
    tasks = []
    for insight in insights:
        if skip_tests is not None and insight.id in skip_tests:
            logger.info(f"Skip test insight={insight.title} (requested in gooddata.yaml)")
        else:
            tasks.append(safe_test_insight(logger, sdk_wrapper, workspace_id, insight, semaphore))
    results = await asyncio.gather(*tasks)
    duration = get_duration(start)
    errors = [result for result in results if result["status"] == "failed"]
    if len(errors) > 0:
        raise Exception(f"Test insights failed {workspace_id=} {duration=}(ms) {errors=}")
    else:
        logger.info(f"Test insights finished {workspace_id=} {duration=}(ms)")


def create_localized_workspaces(
    data_product: GoodDataConfigProduct,
    sdk_facade: GoodDataApiWrapper,
    workspace_id: str,
) -> None:
    if data_product.localization is None:
        return
    for to in data_product.localization.to:
        from deep_translator import GoogleTranslator

        translator_func = GoogleTranslator(
            source=data_product.localization.from_language, target=to.language
        ).translate_batch
        logging.info(f"create_localized_workspaces layout_root_path={GOODDATA_LAYOUTS_DIR / data_product.id}")
        sdk_facade.generate_localized_workspaces(
            workspace_id,
            to=to,
            data_product=data_product,
            translator_func=translator_func,
            layout_path=GOODDATA_LAYOUTS_DIR / data_product.id,
            provision_workspace=True,
            store_layouts=False,
        )


def get_table(data: List[list], headers: List[str], fmt: str) -> str:
    return tabulate.tabulate(data, headers=headers, tablefmt=fmt)


def dbt_cloud_stats_degradations(
    args: Namespace,
    logger: logging.Logger,
    environment_id: str,
    model_executions: List[DbtExecution],
    dbt_conn: DbtConnection,
) -> None:
    logger.info("Get stats for historical executions...")
    models_history_avg_execution_times = dbt_conn.get_average_times(logger, model_executions, environment_id, 5)
    differences = []
    degradations = 0
    for execution in model_executions:
        for model_id, avg_time in models_history_avg_execution_times.items():
            last_execution = execution.execution_info.execution_time
            difference = float(last_execution - avg_time) / avg_time * 100
            degradation = difference > args.allowed_degradation
            if model_id == execution.unique_id:
                differences.append(
                    [
                        model_id,
                        round(last_execution, 2),
                        round(avg_time, 2),
                        round(difference, 2),
                        str(degradation),
                    ]
                )
                if degradation:
                    degradations += 1
    headers = ["Model ID", "Last duration(s)", "Average duration(s)", "Difference(%)", "Degradation"]
    pretty_table = get_table(differences, headers, "outline")
    if degradations > 0:
        logger.warning(
            "Stats for historical executions contain degradations! "
            + f"Threshold={args.allowed_degradation}%\n{pretty_table}"
        )
    else:
        logger.info(f"Stats for historical executions:\n{pretty_table}")

    gitlab_token = os.getenv("GITLAB_TOKEN")
    if os.getenv("CI_MERGE_REQUEST_IID") and gitlab_token:
        # Running in Gitlab CI pipeline, report performance of executions to the merge request to notify code reviewer
        git_table = get_table(differences, headers, "github")
        logger.info("Sending report to related Gitlab merge request as comment")
        if degradations > 0:
            message = (
                "WARNING: some executions of dbt models in this merge request are slower than average!"
                + f"Threshold={args.allowed_degradation}%\n\n{git_table}"
            )
            report_message_to_merge_request(gitlab_token, message)
        else:
            message = f"INFO: performance of all executions of dbt models is OK!\n\n{git_table}"
            report_message_to_merge_request(gitlab_token, message)


def dbt_cloud_stats(
    args: Namespace,
    logger: logging.Logger,
    all_model_ids: List[str],
    environment_id: str,
) -> None:
    logger.info("Get stats for last execution...")
    dbt_conn = DbtConnection(credentials=DbtCredentials(account_id=args.account_id, token=args.token))
    dbt_tables = DbtModelTables.from_local(args.gooddata_upper_case, all_model_ids)
    model_executions = dbt_conn.get_last_execution(environment_id, len(dbt_tables.tables))
    exec_list = []
    for execution in model_executions:
        exec_list.append([execution.unique_id, round(execution.execution_info.execution_time, 2)])

    headers = ["Model ID", "Duration(s)"]
    pretty_table = get_table(exec_list, headers, "outline")
    logger.info(f"Stats for last execution:\n{pretty_table}")

    dbt_cloud_stats_degradations(args, logger, environment_id, model_executions, dbt_conn)


def dbt_cloud_run(args: Namespace, logger: logging.Logger, all_model_ids: List[str]) -> None:
    dbt_conn = DbtConnection(credentials=DbtCredentials(account_id=args.account_id, token=args.token))
    logger.info("#" * 80)
    logger.info(f"Starting job in dbt cloud with job_id={args.job_id}")
    logger.info("#" * 80)

    run_id, run_href = dbt_conn.run_job(logger, args.job_id)
    logger.info(f"Job with {run_id=} successfully initiated. Link to job run {run_href=}")

    dbt_conn.fetch_run_result(run_id)
    dbt_conn.download_manifest(run_id)
    logger.info("Manifest downloaded successfully")

    environment_id = dbt_conn.get_environment_id(args.job_id)
    logger.info(f"Found environment with {environment_id=} for job_id={args.job_id}")

    environment = dbt_conn.read_environment(environment_id, args.project_id, args.job_id)
    dbt_conn.make_profiles(environment, path_to_profiles=Path(args.profiles_dir))
    logger.info(f"Profile file stored to {args.profiles_dir}")

    dbt_cloud_stats(args, logger, all_model_ids, environment_id)


def process_organization(
    args: Namespace,
    logger: logging.Logger,
    sdk_wrapper: GoodDataSdkWrapper,
    gd_config: GoodDataConfig,
    organization: Optional[GoodDataConfigOrganization] = None,
) -> None:
    if args.method == "upload_notification":
        dbt_profiles = DbtProfiles(args)
        # Caches are invalidated only per data source, not per data product
        upload_notification(logger, sdk_wrapper, dbt_profiles.data_source_id)
    elif args.method == "register_data_sources":
        register_data_source(logger, args, gd_config.all_model_ids, sdk_wrapper)
    else:
        if organization:
            data_products = [dp for dp in gd_config.data_products if dp.id in organization.data_product_ids]
        else:
            data_products = gd_config.data_products
        for data_product in data_products:
            logger.info(f"Process product name={data_product.name}")
            environments = gd_config.get_environment_workspaces(data_product.environment_setup_id)
            for environment in environments:
                if environment.id == args.gooddata_environment_id:
                    workspace_id = f"{data_product.id}_{environment.id}"
                    workspace_title = f"{data_product.name} ({environment.name})"
                    if args.method == "provision_workspaces":
                        create_workspace(logger, sdk_wrapper, workspace_id, workspace_title)
                    elif args.method == "deploy_ldm":
                        deploy_ldm(
                            logger, args, gd_config.all_model_ids, sdk_wrapper, data_product.model_ids, workspace_id
                        )
                        if data_product.localization:
                            create_localized_workspaces(data_product, sdk_wrapper.sdk_facade, workspace_id)
                    elif args.method == "store_analytics":
                        store_analytics(logger, sdk_wrapper.sdk, workspace_id, data_product)
                    elif args.method == "deploy_analytics":
                        deploy_analytics(logger, sdk_wrapper, workspace_id, data_product)
                    elif args.method == "test_insights":
                        parallelism = gd_config.global_properties.test_insights_parallelism or 1
                        asyncio.run(
                            test_insights(logger, sdk_wrapper, workspace_id, data_product.skip_tests, parallelism)
                        )
                    else:
                        raise Exception(f"Unsupported method requested in args: {args.method}")


def main() -> None:
    args = parse_arguments("gooddata-dbt plugin for models management and invalidating caches(upload notification)")
    logger = get_logger("gooddata-dbt", args.debug)
    logger.info("Start")
    with open(args.gooddata_config) as fp:
        gd_config = GoodDataConfig.from_dict(yaml.safe_load(fp))
    # dbt cloud tasks must run only once, not for each organization
    if args.method == "dbt_cloud_run":
        dbt_cloud_run(args, logger, gd_config.all_model_ids)
    elif args.method == "dbt_cloud_stats":
        dbt_cloud_stats(args, logger, gd_config.all_model_ids, args.environment_id)
    else:
        if args.gooddata_profiles:
            logger.info(f"Process multiple organizations profiles={args.gooddata_profiles}")
            for organization in gd_config.organizations:
                if organization.gooddata_profile in args.gooddata_profiles:
                    sdk_wrapper = GoodDataSdkWrapper(args, logger, profile=organization.gooddata_profile)
                    logger.info(f"Process organization profile={organization.gooddata_profile}")
                    process_organization(args, logger, sdk_wrapper, gd_config, organization)
        else:
            sdk_wrapper = GoodDataSdkWrapper(args, logger)
            logger.info(f"Process single organization from env vars host={args.gooddata_host}")
            process_organization(args, logger, sdk_wrapper, gd_config)

    logger.info("End")
