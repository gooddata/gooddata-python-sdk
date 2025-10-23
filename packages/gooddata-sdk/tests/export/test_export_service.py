# (C) 2023 GoodData Corporation
import os
from pathlib import Path

from gooddata_sdk import (
    Attribute,
    ExecutionDefinition,
    ExportCustomLabel,
    ExportCustomMetric,
    ExportCustomOverride,
    ExportRequest,
    GoodDataSdk,
    ObjId,
    SimpleMetric,
    TableDimension,
)
from tests_support.vcrpy_utils import get_vcr

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
        dimensions=[
            TableDimension(item_ids=["state", "region"]),
            TableDimension(item_ids=["measureGroup"]),
        ],
    )
    return sdk.compute.for_exec_def(workspace_id, exec_def).result_id


def _validate_clean(goal_path: Path):
    if not goal_path.exists():
        assert False, "The export was not stored"
    os.remove(goal_path)
    assert True


def _tabular_export_base(test_config, export_format: str):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]
    execution_result = _get_execution_result(sdk, workspace_id)
    export_request = ExportRequest(
        format=export_format,
        execution_result=execution_result,
        file_name=f"test_{export_format.lower()}",
        custom_override=ExportCustomOverride(
            labels={"region": ExportCustomLabel(title="Custom Title Region")},
            metrics={
                "price": ExportCustomMetric(title="Sum Of Price", format=""),
                "order_amount": ExportCustomMetric(title="Order Amount Metric", format="#,##0.00"),
            },
        ),
    )
    goal_path = _exports_dir / export_request.file
    sdk.export.export_tabular(workspace_id, export_request, _exports_dir)
    _validate_clean(goal_path)


def _tabular_by_visualization_id_base(test_config, export_format: str):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    workspace_id = test_config["workspace"]
    visualization_id = test_config["visualization_id"]
    visualization_name = test_config["visualization_name"]
    goal_path = _exports_dir / f"{visualization_name}.{export_format.lower()}"
    sdk.export.export_tabular_by_visualization_id(
        workspace_id=workspace_id, visualization_id=visualization_id, file_format=export_format, store_path=_exports_dir
    )
    _validate_clean(goal_path)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_csv.yaml"))
def test_export_csv(test_config):
    _tabular_export_base(test_config, "CSV")


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_excel.yaml"))
def test_export_excel(test_config):
    _tabular_export_base(test_config, "XLSX")


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_csv_by_visualization_id.yaml"))
def test_export_by_visualization_id_csv(test_config):
    _tabular_by_visualization_id_base(test_config, "CSV")


@gd_vcr.use_cassette(str(_fixtures_dir / "test_export_excel_by_visualization_id.yaml"))
def test_export_by_visualization_id_excel(test_config):
    _tabular_by_visualization_id_base(test_config, "XLSX")
