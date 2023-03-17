# (C) 2023 GoodData Corporation
import os
from pathlib import Path

from tests_support.vcrpy_utils import get_vcr

from gooddata_sdk import Attribute, ExecutionDefinition, ExportRequest, GoodDataSdk, ObjId, SimpleMetric

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"
_exports_dir = _current_dir / "exports"


# The following test works only in GoodData Cloud
# def test_export_pdf(test_config):
#     sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
#     sdk.export.export_pdf("demo", "campaign", "test")


def _get_execution_result(sdk: GoodDataSdk, workspace_id: str) -> str:
    exec_def = ExecutionDefinition(
        attributes=[Attribute(local_id="region", label="region"), Attribute(local_id="state", label="state")],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[["state", "region"], ["measureGroup"]],
    )
    return sdk.compute.for_exec_def(workspace_id, exec_def).result_id


def _tabular_export_base(test_config, export_format: str):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]
    execution_result = _get_execution_result(sdk, workspace_id)
    export_request = ExportRequest(
        format=export_format, execution_result=execution_result, file_name=f"test_{export_format.lower()}"
    )
    goal_path = _exports_dir / export_request.file
    sdk.export.export_tabular(workspace_id, export_request, _exports_dir)
    if not goal_path.exists():
        assert False, "The export was not stored"
    os.remove(goal_path)
    assert True


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_csv.yaml"))
def test_export_csv(test_config):
    _tabular_export_base(test_config, "CSV")


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_excel.yaml"))
def test_export_excel(test_config):
    _tabular_export_base(test_config, "XLSX")
