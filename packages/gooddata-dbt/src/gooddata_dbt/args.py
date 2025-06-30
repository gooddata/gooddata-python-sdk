# (C) 2023 GoodData Corporation
import argparse
import os


def get_parser(description: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        conflict_handler="resolve", description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


def set_gooddata_endpoint_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-gc",
        "--gooddata-config",
        help="Path to GoodData config file containing definitions of environments",
        default=os.getenv("GOODDATA_CONFIG", "gooddata.yml"),
    )
    parser.add_argument(
        "-gh",
        "--gooddata-host",
        help="Hostname(DNS) where GoodData is running",
        default=os.getenv("GOODDATA_HOST", "http://localhost:3000"),
    )
    parser.add_argument(
        "-gt",
        "--gooddata-token",
        help="GoodData API token for authentication",
        default=os.getenv("GOODDATA_TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz"),
    )
    parser.add_argument(
        "-go",
        "--gooddata-override-host",
        help="Override hostname, if necessary. "
        "When you connect to different hostname than where GoodData is running(proxies)",
        default=os.getenv("GOODDATA_OVERRIDE_HOST"),
    )
    # Alternative - use profile.yml file
    env_profiles = os.getenv("GOODDATA_PROFILES")
    env_profiles_list = env_profiles.split(" ") if env_profiles else []
    parser.add_argument(
        "-gp",
        "--gooddata-profiles",
        nargs="*",
        help="Profiles in profile.yml file. Overrides gooddata-host, gooddata-token and gooddata-override-host."
        + "You can use multiple profiles separated by space to deliver models/analytics to multiple organizations.",
        default=env_profiles_list,
    )


def set_environment_id_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-gw",
        "--gooddata-environment-id",
        help="Environment where to deploy. Environments are configured in gooddata.yml.",
        default=os.getenv("GOODDATA_ENVIRONMENT_ID", "development"),
    )


def set_gooddata_upper_case_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-guc",
        "--gooddata-upper-case",
        help="Upper case all physical model entities (tables, columns). Valuable for Snowflake!",
        action="store_true",
        default=False,
    )


def set_gooddata_workspace_title_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-gwt", "--gooddata-workspace-title", help="Workspace title", default=os.getenv("GOODDATA_WORKSPACE_TITLE")
    )


def set_dbt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-pd",
        "--profiles-dir",
        help="Directory where dbt profiles.yml is stored",
        default=os.getenv("DBT_PROFILES_DIR", "~/.dbt"),
    )
    parser.add_argument(
        "-p", "--profile", help="Name of profile from profiles.yml", default=os.getenv("DBT_PROFILE", "default")
    )
    parser.add_argument(
        "-t",
        "--target",
        help="dbt target/output. DB where dbt deploys. GoodData registers it as data source.",
        default=os.getenv("ELT_ENVIRONMENT", "cicd_dev_local"),
    )


def set_dbt_cloud_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-dca",
        "--account-id",
        help="dbt cloud account ID",
        default=os.getenv("DBT_ACCOUNT_ID"),
    )
    parser.add_argument(
        "-dcj",
        "--job-id",
        help="dbt cloud job ID",
        default=os.getenv("DBT_JOB_ID"),
    )
    parser.add_argument(
        "-dcp",
        "--project-id",
        help="dbt cloud project ID",
        default=os.getenv("DBT_PROJECT_ID"),
    )
    parser.add_argument(
        "-dct",
        "--token",
        help="dbt cloud token",
        default=os.getenv("DBT_TOKEN"),
    )
    parser.add_argument(
        "-dcd",
        "--allowed-degradation",
        type=int,
        help="How much performance of model executions can degrade before reported as warning, in percent",
        default=int(os.getenv("DBT_ALLOWED_DEGRADATION", "100")),
    )


def set_dbt_cloud_stats_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-dce",
        "--environment-id",
        help="dbt cloud environment ID",
        default=os.getenv("DBT_ENVIRONMENT_ID"),
    )


def parse_arguments(description: str) -> argparse.Namespace:
    parser = get_parser(description)
    parser.add_argument("--debug", action="store_true", default=False, help="Increase logging level to DEBUG")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Do not call GoodData APIs")
    set_gooddata_endpoint_args(parser)

    subparsers = parser.add_subparsers(help="actions")

    dbt_cloud_run = subparsers.add_parser("dbt_cloud_run")
    set_dbt_cloud_args(dbt_cloud_run)
    set_dbt_args(dbt_cloud_run)
    set_gooddata_upper_case_args(dbt_cloud_run)
    dbt_cloud_run.set_defaults(method="dbt_cloud_run")

    dbt_cloud_stats = subparsers.add_parser("dbt_cloud_stats")
    set_dbt_cloud_args(dbt_cloud_stats)
    set_dbt_cloud_stats_args(dbt_cloud_stats)
    set_dbt_args(dbt_cloud_stats)
    set_gooddata_upper_case_args(dbt_cloud_stats)
    dbt_cloud_stats.set_defaults(method="dbt_cloud_stats")

    provision_workspaces = subparsers.add_parser("provision_workspaces")
    set_environment_id_arg(provision_workspaces)
    provision_workspaces.set_defaults(method="provision_workspaces")

    register_data_sources = subparsers.add_parser("register_data_sources")
    set_dbt_args(register_data_sources)
    set_environment_id_arg(register_data_sources)
    set_gooddata_upper_case_args(register_data_sources)
    register_data_sources.set_defaults(method="register_data_sources")

    deploy_ldm = subparsers.add_parser("deploy_ldm")
    set_dbt_args(deploy_ldm)
    set_environment_id_arg(deploy_ldm)
    set_gooddata_upper_case_args(deploy_ldm)
    deploy_ldm.set_defaults(method="deploy_ldm")

    upload_notification = subparsers.add_parser("upload_notification")
    set_dbt_args(upload_notification)
    set_gooddata_upper_case_args(upload_notification)
    upload_notification.set_defaults(method="upload_notification")

    deploy_analytics = subparsers.add_parser("deploy_analytics")
    set_environment_id_arg(deploy_analytics)
    # TODO - now it is no longer needed. Either delete it or utilize it to do not lower_case everything
    set_gooddata_upper_case_args(deploy_analytics)
    deploy_analytics.set_defaults(method="deploy_analytics")

    store_analytics = subparsers.add_parser("store_analytics")
    set_environment_id_arg(store_analytics)
    set_gooddata_upper_case_args(store_analytics)
    store_analytics.set_defaults(method="store_analytics")

    test_visualizations = subparsers.add_parser("test_visualizations")
    set_environment_id_arg(test_visualizations)
    test_visualizations.set_defaults(method="test_visualizations")

    return parser.parse_args()
