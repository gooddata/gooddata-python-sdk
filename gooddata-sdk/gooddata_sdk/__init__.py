# (C) 2021 GoodData Corporation
"""The `gooddata-sdk` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics.
"""

from gooddata_sdk._version import __version__
from gooddata_sdk.catalog.data_source.action_requests.ldm_request import CatalogGenerateLdmRequest
from gooddata_sdk.catalog.data_source.action_requests.scan_model_request import CatalogScanModelRequest
from gooddata_sdk.catalog.data_source.entity_model.content_objects.table import CatalogDataSourceTable
from gooddata_sdk.catalog.data_source.entity_model.data_source import (
    BigQueryAttributes,
    CatalogDataSource,
    CatalogDataSourceBigQuery,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    PostgresAttributes,
    RedshiftAttributes,
    SnowflakeAttributes,
    VerticaAttributes,
)
from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService
from gooddata_sdk.catalog.data_source.validation.data_source import DataSourceValidator
from gooddata_sdk.catalog.entity import BasicCredentials, TokenCredentialsFromFile
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeWorkspaceModel,
    CatalogDeclarativeWorkspaces,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.dataset import (
    CatalogAttribute,
    CatalogDataset,
    CatalogFact,
    CatalogLabel,
)
from gooddata_sdk.catalog.workspace.entity_model.content_objects.metric import CatalogMetric
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.catalog.workspace.service import CatalogWorkspaceContent, CatalogWorkspaceContentService
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ExecModelEntity, ObjId
from gooddata_sdk.compute.model.execution import ExecutionDefinition, ExecutionResponse, ExecutionResult
from gooddata_sdk.compute.model.filter import (
    AbsoluteDateFilter,
    AllTimeFilter,
    AttributeFilter,
    Filter,
    MetricValueFilter,
    NegativeAttributeFilter,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
)
from gooddata_sdk.compute.model.metric import (
    ArithmeticMetric,
    Metric,
    PopDate,
    PopDateDataset,
    PopDateMetric,
    PopDatesetMetric,
    SimpleMetric,
)
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.insight import Insight, InsightAttribute, InsightBucket, InsightMetric, InsightService
from gooddata_sdk.sdk import GoodDataSdk
from gooddata_sdk.table import ExecutionTable, TableService
from gooddata_sdk.utils import SideLoads
