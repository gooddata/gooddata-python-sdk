# (C) 2022 GoodData Corporation
from __future__ import annotations

import re
from typing import NamedTuple, Optional

from gooddata_sdk import (
    CatalogWorkspaceContent,
    GoodDataSdk,
    ObjId,
    Visualization,
    VisualizationAttribute,
    VisualizationMetric,
)

from gooddata_fdw import column_utils, options
from gooddata_fdw.environment import ColumnDefinition, TableDefinition
from gooddata_fdw.naming import (
    DefaultCatalogNamingStrategy,
    DefaultInsightColumnNaming,
    DefaultInsightTableNaming,
    InsightColumnNamingStrategy,
)
from gooddata_fdw.pg_logging import _log_debug, _log_info, _log_warn


def _metric_format_to_precision(metric_format: Optional[str]) -> Optional[str]:
    if metric_format:
        re_decimal_places = re.compile(r"^[^.]+\.([#0]+)")
        match = re_decimal_places.search(metric_format)
        if match:
            return str(len(match.group(1)))

    return None


class ImporterInitData(NamedTuple):
    sdk: GoodDataSdk
    workspace: str
    server_options: options.ServerOptions
    import_options: options.ImportSchemaOptions
    restriction_type: Optional[str]
    restricts: list[str]


class WorkspaceImporter:
    _SUPPORTED_TYPES: list[str] = []

    def __init__(self, data: ImporterInitData) -> None:
        self._sdk = data.sdk
        self._workspace = data.workspace
        self._server_options = data.server_options
        self._import_options = data.import_options
        self._restriction_type = data.restriction_type
        self._restricts = data.restricts

    @classmethod
    def support_object_type(cls, object_type: str) -> bool:
        return object_type in cls._SUPPORTED_TYPES

    def import_tables(self) -> list[TableDefinition]:
        raise NotImplementedError()


class WorkspaceImportersLocator:
    _IMPORTERS: set[type[WorkspaceImporter]] = set()

    @classmethod
    def register(cls, class_: type[WorkspaceImporter]) -> type[WorkspaceImporter]:
        cls._IMPORTERS.add(class_)
        return class_

    @classmethod
    def locate(cls, object_type: str) -> list[type[WorkspaceImporter]]:
        return [importer for importer in cls._IMPORTERS if importer.support_object_type(object_type)]


@WorkspaceImportersLocator.register
class InsightsWorkspaceImporter(WorkspaceImporter):
    _SUPPORTED_TYPES: list[str] = ["insights", "all"]

    def __init__(self, data: ImporterInitData) -> None:
        super().__init__(data)

    def import_tables(self) -> list[TableDefinition]:
        table_naming = DefaultInsightTableNaming()

        _log_info(
            f"importing insights as tables from {self._server_options.host} workspace {self._workspace} "
            f"headers_host={self._server_options.headers_host}"
        )
        _log_debug("loading full catalog")
        catalog = self._sdk.catalog_workspace_content.get_full_catalog(self._workspace)
        _log_debug("loading all insights")
        insights = self._sdk.visualizations.get_visualizations(self._workspace)

        tables = []
        for insight in insights:
            if not insight.are_relations_valid:
                _log_warn(f"Insight title={insight.title} id={insight.id} is invalid, we cannot import it.")
                continue
            table_name = table_naming.table_name_for_insight(insight)
            if table_name == "compute":
                _log_warn("Insight name may not equal to `compute` used by import_semantic_layer_from_workspace()")
                continue

            _log_info(f'creating table def "{table_name}" for insight "{insight.title}"')
            tables.append(
                TableDefinition(
                    table_name=table_name,
                    columns=self._table_columns_from_insight(insight, catalog),
                    options=dict(workspace=self._workspace, insight=insight.id),
                )
            )

        return tables

    def _table_columns_from_insight(
        self, insight: Visualization, catalog: CatalogWorkspaceContent
    ) -> list[ColumnDefinition]:
        column_naming = DefaultInsightColumnNaming()
        attr_cols = [self._attribute_to_table_column(attr, column_naming, catalog) for attr in insight.attributes]
        metric_cols = [self._metric_to_table_column(metric, column_naming, catalog) for metric in insight.metrics]

        return attr_cols + metric_cols

    @staticmethod
    def _attribute_to_table_column(
        attr: VisualizationAttribute, column_naming: InsightColumnNamingStrategy, catalog: CatalogWorkspaceContent
    ) -> ColumnDefinition:
        column_name = column_naming.col_name_for_attribute(attr)
        _log_debug(f'creating col def "{column_name}" for attribute "{attr.label_id}"')

        label_id = ObjId(id=attr.label_id, type="label")
        data_type = column_utils.column_data_type_for(catalog.find_label_attribute(label_id))

        return ColumnDefinition(
            column_name=column_name,
            type_name=data_type,
            options=dict(id=f"label/{attr.label_id}", local_id=attr.local_id),
        )

    def _metric_to_table_column(
        self, metric: VisualizationMetric, column_naming: InsightColumnNamingStrategy, catalog: CatalogWorkspaceContent
    ) -> ColumnDefinition:
        column_name = column_naming.col_name_for_metric(metric)
        metric_format = self._get_insight_metric_format(metric, catalog)
        data_type = self._import_options.metric_data_type(_metric_format_to_precision(metric_format))

        column_options = dict(local_id=metric.local_id)
        if metric.item_id:
            # add column OPTION id even if it is not required by insight table - for better user experience
            # TODO - distinguish facts and metrics better when loading insights
            column_options["id"] = f"{'fact' if metric.format else 'metric'}/{metric.item_id}"

        _log_debug(
            f'creating col def "{column_name}" for metric "{metric.title}(id={metric.item_id},'
            f'local_id={metric.local_id})" format={metric_format} data_type={data_type}'
        )
        return ColumnDefinition(
            column_name=column_name,
            type_name=data_type,
            options=column_options,
        )

    # InsightMetric do not contain format in case of stored metrics
    @staticmethod
    def _get_insight_metric_format(metric: VisualizationMetric, catalog: CatalogWorkspaceContent) -> Optional[str]:
        if metric.format:
            return metric.format
        elif metric.item_id:
            metric_id = ObjId(id=metric.item_id, type="metric")
            full_metric = catalog.get_metric(metric_id)
            if full_metric:
                return full_metric.format

        return None


@WorkspaceImportersLocator.register
class SemanticLayerWorkspaceImporter(WorkspaceImporter):
    _SUPPORTED_TYPES: list[str] = ["compute", "all"]

    def __init__(self, data: ImporterInitData) -> None:
        super().__init__(data)

    def import_tables(self) -> list[TableDefinition]:
        _log_info(
            f"importing semantic layer as tables from {self._server_options.host} workspace {self._workspace} "
            f"headers_host={self._server_options.headers_host}"
        )

        catalog = self._sdk.catalog_workspace_content.get_full_catalog(self._workspace)
        naming = DefaultCatalogNamingStrategy()
        columns = []

        for metric in catalog.metrics:
            column_name = naming.col_name_for_metric(metric)
            data_type = self._import_options.metric_data_type(_metric_format_to_precision(metric.format))
            _log_info(f"metric {metric.id} mapped to column {column_name} target data_type={data_type}")

            columns.append(
                ColumnDefinition(
                    column_name=column_name,
                    type_name=data_type,
                    options=dict(id=f"metric/{metric.id}"),
                )
            )

        for dataset in catalog.datasets:
            for fact in dataset.facts:
                column_name = naming.col_name_for_fact(fact, dataset)

                _log_info(f"fact {fact.id} mapped to column {column_name}")

                columns.append(
                    ColumnDefinition(
                        column_name=column_name,
                        # TODO - get data type from PDM
                        type_name=self._import_options.metric_data_type(),
                        options=dict(id=f"fact/{fact.id}"),
                    )
                )

            for attribute in dataset.attributes:
                for label in attribute.labels:
                    column_name = naming.col_name_for_label(label, dataset)
                    data_type = column_utils.column_data_type_for(attribute)

                    _log_info(f"label {label.id} mapped to column {column_name}")

                    columns.append(
                        ColumnDefinition(
                            column_name=column_name,
                            type_name=data_type,
                            options=dict(id=f"label/{label.id}"),
                        )
                    )

        return [
            TableDefinition(
                table_name="compute",
                columns=columns,
                options=dict(workspace=self._workspace, compute="pseudo-table"),
            )
        ]
