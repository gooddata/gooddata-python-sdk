# (C) 2021 GoodData Corporation
from gooddata_sdk.catalog import (
    Catalog,
    CatalogService,
    CatalogDataset,
    CatalogLabel,
    CatalogMetric,
    CatalogAttribute,
    CatalogFact,
)
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute import (
    ComputeService,
    ExecutionResponse,
    ExecutionResult,
    ExecutionDefinition,
)
from gooddata_sdk.exec_model import (
    Attribute,
    Filter,
    Measure,
    PositiveAttributeFilter,
    NegativeAttributeFilter,
    AbsoluteDateFilter,
    RelativeDateFilter,
    MeasureValueFilter,
    RankingFilter,
    SimpleMeasure,
    PopDateMeasure,
    PopDatesetMeasure,
    ArithmeticMeasure,
    PopDate,
    PopDateDataset,
    ObjId,
    ExecModelEntity,
)
from gooddata_sdk.insight import (
    Insight,
    InsightService,
    InsightMeasure,
    InsightAttribute,
    InsightBucket,
)
from gooddata_sdk.table import TableService, ExecutionTable
from gooddata_sdk.utils import Sideloads


class GoodDataSdk:
    def __init__(self, host, token, extra_user_agent=None):
        self._client = GoodDataApiClient(host, token, extra_user_agent)
        self._catalog = CatalogService(self._client)
        self._compute = ComputeService(self._client)
        self._insights = InsightService(self._client)
        self._tables = TableService(self._client)

    @property
    def catalog(self) -> CatalogService:
        return self._catalog

    @property
    def compute(self) -> ComputeService:
        return self._compute

    @property
    def insights(self) -> InsightService:
        return self._insights

    @property
    def tables(self) -> TableService:
        return self._tables
