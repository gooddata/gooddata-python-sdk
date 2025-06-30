# (C) 2021 GoodData Corporation
"""The `gooddata-sdk` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics.
"""

import logging

from gooddata_sdk._version import __version__
from gooddata_sdk.catalog.data_source.action_model.requests.ldm_request import (
    CatalogGenerateLdmRequest,
    CatalogPdmLdmRequest,
    CatalogPdmSql,
)
from gooddata_sdk.catalog.data_source.action_model.requests.scan_model_request import CatalogScanModelRequest
from gooddata_sdk.catalog.data_source.action_model.requests.scan_sql_request import ScanSqlRequest
from gooddata_sdk.catalog.data_source.action_model.responses.scan_sql_response import ScanSqlResponse
from gooddata_sdk.catalog.data_source.action_model.sql_column import SqlColumn
from gooddata_sdk.catalog.data_source.declarative_model.data_source import (
    CatalogDeclarativeDataSource,
    CatalogDeclarativeDataSources,
)
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.pdm import CatalogDeclarativeTables
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.table import (
    CatalogDeclarativeColumn,
    CatalogDeclarativeTable,
)
from gooddata_sdk.catalog.data_source.entity_model.data_source import (
    CatalogDataSource,
    CatalogDataSourceBigQuery,
    CatalogDataSourceDatabricks,
    CatalogDataSourceGreenplum,
    CatalogDataSourceMariaDb,
    CatalogDataSourceMotherDuck,
    CatalogDataSourceMsSql,
    CatalogDataSourceMySql,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    DatabricksAttributes,
    GreenplumAttributes,
    MariaDbAttributes,
    MotherDuckAttributes,
    MsSqlAttributes,
    MySqlAttributes,
    PostgresAttributes,
    RedshiftAttributes,
    SnowflakeAttributes,
    VerticaAttributes,
)
from gooddata_sdk.catalog.data_source.service import CatalogDataSourceService
from gooddata_sdk.catalog.data_source.validation.data_source import DataSourceValidator
from gooddata_sdk.catalog.depends_on import CatalogDependsOn, CatalogDependsOnDateFilter
from gooddata_sdk.catalog.entity import (
    AttrCatalogEntity,
    BasicCredentials,
    ClientSecretCredentials,
    KeyPairCredentials,
    TokenCredentialsFromEnvVar,
    TokenCredentialsFromFile,
)
from gooddata_sdk.catalog.export.request import (
    ExportCustomLabel,
    ExportCustomMetric,
    ExportCustomOverride,
    ExportRequest,
    ExportSettings,
    SlidesExportRequest,
    VisualExportRequest,
)
from gooddata_sdk.catalog.filter_by import CatalogFilterBy
from gooddata_sdk.catalog.identifier import (
    CatalogAssigneeIdentifier,
    CatalogDatasetWorkspaceDataFilterIdentifier,
    CatalogDeclarativeAnalyticalDashboardIdentifier,
    CatalogExportDefinitionIdentifier,
    CatalogNotificationChannelIdentifier,
    CatalogUserIdentifier,
    CatalogWorkspaceIdentifier,
)
from gooddata_sdk.catalog.organization.common.dashboard_slides_template import CatalogDashboardSlidesTemplate
from gooddata_sdk.catalog.organization.common.running_section import CatalogRunningSection
from gooddata_sdk.catalog.organization.common.slide_template import (
    CatalogContentSlideTemplate,
    CatalogCoverSlideTemplate,
    CatalogIntroSlideTemplate,
    CatalogSectionSlideTemplate,
)
from gooddata_sdk.catalog.organization.common.widget_slides_template import CatalogWidgetSlidesTemplate
from gooddata_sdk.catalog.organization.entity_model.directive import CatalogCspDirective
from gooddata_sdk.catalog.organization.entity_model.export_template import (
    CatalogExportTemplate,
    CatalogExportTemplateAttributes,
)
from gooddata_sdk.catalog.organization.entity_model.jwk import (
    CatalogJwk,
    CatalogJwkAttributes,
    CatalogJwkDocument,
    CatalogRsaSpecification,
)
from gooddata_sdk.catalog.organization.entity_model.llm_endpoint import (
    CatalogLlmEndpoint,
    CatalogLlmEndpointDocument,
)
from gooddata_sdk.catalog.organization.entity_model.organization import CatalogOrganization
from gooddata_sdk.catalog.organization.entity_model.setting import CatalogOrganizationSetting
from gooddata_sdk.catalog.organization.layout.export_template import (
    CatalogDeclarativeExportTemplate,
)
from gooddata_sdk.catalog.organization.layout.notification_channel import (
    CatalogDeclarativeNotificationChannel,
    CatalogWebhook,
)
from gooddata_sdk.catalog.organization.service import CatalogOrganizationService
from gooddata_sdk.catalog.permission.declarative_model.dashboard_assignees import (
    CatalogAvailableAssignees,
    CatalogUserAssignee,
    CatalogUserGroupAssignee,
)
from gooddata_sdk.catalog.permission.declarative_model.dashboard_permissions import (
    CatalogDashboardPermissions,
    CatalogGrantedPermission,
    CatalogUserGroupPermission,
    CatalogUserPermission,
)
from gooddata_sdk.catalog.permission.declarative_model.manage_dashboard_permissions import (
    CatalogDashboardAssigneeIdentifier,
    CatalogPermissionsForAssigneeIdentifier,
    CatalogPermissionsForAssigneeRule,
)
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeDashboardPermissionsForAssignee,
    CatalogDeclarativeDashboardPermissionsForAssigneeRule,
    CatalogDeclarativeDataSourcePermission,
    CatalogDeclarativeOrganizationPermission,
    CatalogDeclarativeSingleWorkspacePermission,
    CatalogDeclarativeWorkspaceHierarchyPermission,
    CatalogDeclarativeWorkspacePermissions,
    CatalogOrganizationPermissionAssignment,
)
from gooddata_sdk.catalog.rule import CatalogAssigneeRule
from gooddata_sdk.catalog.user.declarative_model.user import (
    CatalogDeclarativeUser,
    CatalogDeclarativeUserPermission,
    CatalogDeclarativeUsers,
)
from gooddata_sdk.catalog.user.declarative_model.user_and_user_groups import CatalogDeclarativeUsersUserGroups
from gooddata_sdk.catalog.user.declarative_model.user_group import (
    CatalogDeclarativeUserGroup,
    CatalogDeclarativeUserGroupPermission,
    CatalogDeclarativeUserGroups,
)
from gooddata_sdk.catalog.user.entity_model.user import CatalogUser
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup
from gooddata_sdk.catalog.user.management_model.management import (
    CatalogDataSourcePermissionAssignment,
    CatalogPermissionAssignments,
    CatalogPermissionsAssignment,
    CatalogWorkspacePermissionAssignment,
)
from gooddata_sdk.catalog.validate_by_item import CatalogValidateByItem
from gooddata_sdk.catalog.workspace.content_service import CatalogWorkspaceContent, CatalogWorkspaceContentService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalytics,
    CatalogDeclarativeMetric,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.export_definition import (
    CatalogDeclarativeExportDefinition,
    CatalogDeclarativeExportDefinitionRequestPayload,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.automation import (
    CatalogAutomationSchedule,
    CatalogDeclarativeAutomation,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.data_filter_references import (
    CatalogDeclarativeWorkspaceDataFilterReferences,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDataSourceTableIdentifier,
    CatalogDeclarativeAttribute,
    CatalogDeclarativeDataset,
    CatalogDeclarativeDatasetSql,
    CatalogDeclarativeFact,
    CatalogDeclarativeLabel,
    CatalogDeclarativeReference,
    CatalogDeclarativeWorkspaceDataFilterColumn,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset_extensions.dataset_extension import (  # noqa: E501
    CatalogDeclarativeDatasetExtension,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.date_dataset.date_dataset import (
    CatalogDeclarativeDateDataset,
    CatalogGranularitiesFormatting,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
    CatalogDeclarativeModel,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
    CatalogDeclarativeFilterView,
    CatalogDeclarativeUserDataFilter,
    CatalogDeclarativeUserDataFilters,
    CatalogDeclarativeWorkspace,
    CatalogDeclarativeWorkspaceDataFilter,
    CatalogDeclarativeWorkspaceDataFilters,
    CatalogDeclarativeWorkspaceDataFilterSetting,
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
from gooddata_sdk.catalog.workspace.entity_model.content_objects.workspace_setting import CatalogWorkspaceSetting
from gooddata_sdk.catalog.workspace.entity_model.graph_objects.graph import (
    CatalogDependentEntitiesGraph,
    CatalogDependentEntitiesNode,
    CatalogDependentEntitiesRequest,
    CatalogDependentEntitiesResponse,
    CatalogEntityIdentifier,
)
from gooddata_sdk.catalog.workspace.entity_model.user_data_filter import (
    CatalogUserDataFilter,
    CatalogUserDataFilterAttributes,
    CatalogUserDataFilterRelationships,
)
from gooddata_sdk.catalog.workspace.entity_model.workspace import CatalogWorkspace
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.compute.compute_to_sdk_converter import ComputeToSdkConverter
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ExecModelEntity, ObjId
from gooddata_sdk.compute.model.execution import (
    BareExecutionResponse,
    Execution,
    ExecutionDefinition,
    ExecutionResponse,
    ExecutionResult,
    ResultCacheMetadata,
    ResultSizeBytesLimitExceeded,
    ResultSizeDimensions,
    ResultSizeDimensionsLimitsExceeded,
    TableDimension,
    TotalDefinition,
    TotalDimension,
)
from gooddata_sdk.compute.model.filter import (
    AbsoluteDateFilter,
    AllMetricValueFilter,
    AllTimeFilter,
    AttributeFilter,
    Filter,
    InlineFilter,
    MetricValueFilter,
    NegativeAttributeFilter,
    PositiveAttributeFilter,
    RankingFilter,
    RelativeDateFilter,
)
from gooddata_sdk.compute.model.metric import (
    ArithmeticMetric,
    InlineMetric,
    Metric,
    PopDate,
    PopDateDataset,
    PopDateMetric,
    PopDatesetMetric,
    SimpleMetric,
)
from gooddata_sdk.compute.service import ComputeService
from gooddata_sdk.sdk import GoodDataSdk
from gooddata_sdk.table import ExecutionTable, TableService
from gooddata_sdk.utils import SideLoads
from gooddata_sdk.visualization import (
    Visualization,
    VisualizationAttribute,
    VisualizationBucket,
    VisualizationFilter,
    VisualizationMetric,
    VisualizationService,
)

# by default don't log anything
logging.getLogger(__name__).addHandler(logging.NullHandler())
