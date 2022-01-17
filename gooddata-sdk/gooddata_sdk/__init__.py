# (C) 2021 GoodData Corporation
"""The `gooddata-sdk` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics.
"""

from gooddata_sdk._version import __version__
from gooddata_sdk.catalog import (
    Catalog,
    CatalogAttribute,
    CatalogDataset,
    CatalogFact,
    CatalogLabel,
    CatalogMetric,
    CatalogService,
)
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute import ComputeService, ExecutionDefinition, ExecutionResponse, ExecutionResult
from gooddata_sdk.compute_model import (
    AbsoluteDateFilter,
    AllTimeFilter,
    ArithmeticMetric,
    Attribute,
    ExecModelEntity,
    Filter,
    Metric,
    MetricValueFilter,
    NegativeAttributeFilter,
    ObjId,
    PopDate,
    PopDateDataset,
    PopDateMetric,
    PopDatesetMetric,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
    SimpleMetric,
)
from gooddata_sdk.insight import Insight, InsightAttribute, InsightBucket, InsightMetric, InsightService
from gooddata_sdk.sdk import GoodDataSdk
from gooddata_sdk.table import ExecutionTable, TableService
from gooddata_sdk.utils import SideLoads
