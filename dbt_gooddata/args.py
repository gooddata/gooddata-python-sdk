import argparse
import os


def get_parser(description: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        conflict_handler="resolve",
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


def set_gooddata_endpoint_args(parser):
    parser.add_argument("-gh", "--gooddata-host",
                        help="Hostname(DNS) where GoodData is running",
                        default=os.getenv("GOODDATA_HOST", "http://localhost:3000"))
    parser.add_argument("-gt", "--gooddata-token",
                        help="GoodData API token for authentication",
                        default=os.getenv("GOODDATA_TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz"))
    parser.add_argument("-go", "--gooddata-override-host",
                        help="Override hostname, if necessary. "
                             "When you connect to different hostname than where GoodData is running(proxies)",
                        default=os.getenv("GOODDATA_OVERRIDE_HOST"))


def set_environment_id_arg(parser: argparse.ArgumentParser):
    parser.add_argument("-gw", "--gooddata-environment-id",
                        help="Environment where to deploy. Environments are configured in gooddata.yml.",
                        default=os.getenv("GOODDATA_ENVIRONMENT_ID", "development"))


def set_gooddata_model_id_args(parser: argparse.ArgumentParser):
    model_ids = os.getenv("GOODDATA_MODEL_IDS", None)
    if model_ids:
        default = model_ids.split(" ")
    else:
        default = []
    parser.add_argument("-gm", "--gooddata-model-ids",
                        nargs='+',
                        help="Model ID specified in meta of dbt models. Models(tables) to be included into GoodData.",
                        default=default)


def set_gooddata_upper_case_args(parser: argparse.ArgumentParser):
    parser.add_argument("-guc", "--gooddata-upper-case",
                        help="Upper case all physical model entities (tables, columns). Valuable for Snowflake!",
                        action='store_true', default=False)


def set_gooddata_workspace_title_args(parser: argparse.ArgumentParser):
    parser.add_argument("-gwt", "--gooddata-workspace-title",
                        help="Workspace title",
                        default=os.getenv("GOODDATA_WORKSPACE_TITLE"))


def set_dbt_args(parser: argparse.ArgumentParser):
    parser.add_argument("-pd", "--profile-dir",
                        help="Directory where dbt profiles.yml is stored",
                        default=os.getenv("DBT_PROFILE_DIR", "~/.dbt"))
    parser.add_argument("-p", "--profile",
                        help="Name of profile from profiles.yml",
                        default=os.getenv("DBT_PROFILE", "default"))
    parser.add_argument("-t", "--target",
                        help="dbt target/output. DB where dbt deploys. GoodData registers it as data source.",
                        default=os.getenv("ELT_ENVIRONMENT", "cicd_dev_local"))


def parse_arguments(description: str):
    parser = get_parser(description)
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Increase logging level to DEBUG')
    set_gooddata_endpoint_args(parser)

    subparsers = parser.add_subparsers(help='actions')

    deploy_models = subparsers.add_parser("deploy_models")
    set_dbt_args(deploy_models)
    set_environment_id_arg(deploy_models)
    set_gooddata_model_id_args(deploy_models)
    set_gooddata_upper_case_args(deploy_models)
    deploy_models.set_defaults(method='deploy_models')

    upload_notification = subparsers.add_parser("upload_notification")
    set_dbt_args(upload_notification)
    upload_notification.set_defaults(method='upload_notification')

    deploy_analytics = subparsers.add_parser("deploy_analytics")
    set_environment_id_arg(deploy_analytics)
    set_gooddata_model_id_args(deploy_analytics)
    # TODO - now it is no longer needed. Either delete it or utilize it to do not lower_case everything
    set_gooddata_upper_case_args(deploy_analytics)
    deploy_analytics.set_defaults(method='deploy_analytics')

    store_analytics = subparsers.add_parser("store_analytics")
    set_environment_id_arg(store_analytics)
    set_gooddata_model_id_args(store_analytics)
    set_gooddata_upper_case_args(store_analytics)
    store_analytics.set_defaults(method='store_analytics')

    test_insights = subparsers.add_parser("test_insights")
    set_environment_id_arg(test_insights)
    test_insights.set_defaults(method='test_insights')

    return parser.parse_args()
