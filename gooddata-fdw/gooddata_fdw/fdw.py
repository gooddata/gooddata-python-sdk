# (C) 2021 GoodData Corporation
from __future__ import annotations

import datetime
import re
import traceback
from operator import itemgetter
from typing import Any, Optional, Union

import gooddata_sdk as sdk
from gooddata_fdw import __version__
from gooddata_fdw.environment import ColumnDefinition, ForeignDataWrapper, Qual, TableDefinition
from gooddata_fdw.naming import DefaultCatalogNamingStrategy, DefaultInsightColumnNaming, DefaultInsightTableNaming
from gooddata_fdw.pg_logging import _log_debug, _log_error, _log_info, _log_warn
from gooddata_sdk import create_sdk
from gooddata_sdk.catalog import Catalog, CatalogAttribute
from gooddata_sdk.compute_model import (
    AbsoluteDateFilter,
    Attribute,
    Filter,
    Metric,
    NegativeAttributeFilter,
    ObjId,
    PositiveAttributeFilter,
)
from gooddata_sdk.insight import InsightMetric
from gooddata_sdk.type_converter import AttributeConverterStore, Converter, DBTypeConverterStore

USER_AGENT = f"gooddata-fdw/{__version__}"
"""Extra segment of the User-Agent header that will be appended to standard gooddata-sdk user agent."""


DEFAULT_ATTRIBUTE_DATATYPE = "VARCHAR(255)"
METRIC_DATA_TYPE = "DECIMAL"
METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT = "18"
METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT = "2"

# Once AbsoluteDateFilter supports empty from/to, remove this workaround
MIN_DATE = "0001-01-01"
MAX_DATE = "2999-01-01"


def _col_as_computable(col: ColumnDefinition) -> Union[Attribute, Metric]:
    item_type, item_id = col.options["id"].split("/")

    # since all cols are from the compute table, the uniqueness of local_id is ensured...
    if item_type == "label":
        return sdk.Attribute(local_id=col.column_name, label=item_id)
    else:
        aggregation = col.options["agg"] if "agg" in col.options else None

        return sdk.SimpleMetric(
            local_id=col.column_name,
            item=sdk.ObjId(item_id, item_type),
            aggregation=aggregation,
        )


def column_data_type_for(attribute: Optional[CatalogAttribute]) -> str:
    """Determine what postgres type should be used for `attribute`."""
    if not attribute:
        return Converter.DEFAULT_DB_DATA_TYPE

    converter = AttributeConverterStore.find_converter(attribute.dataset.data_type, attribute.granularity)
    return converter.db_data_type()


# InsightMetric do not contain format in case of stored metrics
def get_insight_metric_format(metric: InsightMetric, catalog: Catalog) -> Optional[str]:
    if metric.format:
        return metric.format
    elif metric.item_id:
        metric_id = ObjId(id=metric.item_id, type="metric")
        full_metric = catalog.get_metric(metric_id)
        if full_metric:
            return full_metric.format

    return None


def get_metric_data_type(metric_digits_before_dec_point: str, digits_after: str) -> str:
    return f"{METRIC_DATA_TYPE}({metric_digits_before_dec_point}, {digits_after})"


def metric_format_to_data_type(metric_format: Optional[str], metric_digits_before_dec_point: str) -> str:
    digits_after = METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT
    if metric_format:
        re_decimal_places = re.compile(r"^[^.]+\.([#0]+)")
        match = re_decimal_places.search(metric_format)
        if match:
            digits_after = str(len(match.group(1)))

    return get_metric_data_type(metric_digits_before_dec_point, digits_after)


class GoodDataForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options: dict[str, str], columns: dict[str, ColumnDefinition]) -> None:
        super(GoodDataForeignDataWrapper, self).__init__(options, columns)

        if "host" not in options or "token" not in options:
            raise ValueError("server OPTIONS must contain 'host' and 'token' keys.")

        if "workspace" not in options:
            raise ValueError(
                "attempting to work with an incorrectly defined foreign table.Table must contain both 'workspace'."
            )

        _log_debug(f"initializing (options={options}, columns={columns})")

        self._host, self._token, self._workspace = itemgetter("host", "token", "workspace")(options)
        self._options = options
        self._columns = columns
        self._insight = options.get("insight")
        self._compute = options.get("compute")
        self._sdk = create_sdk(self._host, self._token, USER_AGENT, options.get("headers_host"))

        self._validate()

    def _validate(self) -> None:
        """
        Validates column definitions, making sure that the options contain all the essential mapping metadata.

        For table mapped to an insight, each column's OPTIONS must contain localId.
        For all other tables (including the 'compute' pseudo-table), each column's OPTIONS must contain 'id'
        :return:
        """
        if self._insight is not None:
            for c in self._columns.values():
                if "local_id" not in c.options:
                    raise ValueError(
                        f"Foreign table column '{c.column_name}' is not defined correctly. "
                        f"For tables that map GoodData.CN insight, the column OPTIONS must specify "
                        f"'localId' which is localIdentifier of the Insight's bucket item. If you created "
                        f"this table manually, please rather use the IMPORT FOREIGN SCHEMA and import "
                        f"from the 'gooddata_insights' schema. The import will set everything correctly."
                    )

            return

        for c in self._columns.values():
            if "id" not in c.options:
                raise ValueError(
                    f"Foreign table column '{c.column_name}' is not defined correctly. "
                    f"For tables mapping to GoodData.CN semantic layer, the column OPTIONS must specify "
                    f"'id' which in format: 'fact/your.fact.id', 'label/your.label.id', "
                    f"'metric/your.metric.id'."
                )
            else:
                split = c.options["id"].split("/")

                if len(split) > 2 or split[0] not in ("fact", "label", "metric"):
                    raise ValueError(
                        f"Foreign table column '{c.column_name}' is not defined correctly. "
                        f"For tables mapping to GoodData.CN semantic layer, the column OPTIONS must "
                        f"specify 'id' which in format: 'fact/your.fact.id', 'label/your.label.id', "
                        f"'metric/your.metric.id'. Instead got: {c.options['id']}"
                    )

    def _execute_insight(  # type: ignore
        self, quals: list[Qual], columns: list[str], sortKeys: Optional[list[Any]] = None
    ):
        """
        Computes data for table mapped to an insight. Note that this execution maintains insight's filters - the
        table is implicitly filtered.
        """
        # TODO add validation that the table columns are consistent with insight bucket items
        assert self._insight is not None

        col_to_local_id = dict([(c.column_name, c.options["local_id"]) for c in self._columns.values()])
        insight = self._sdk.insights.get_insight(self._workspace, self._insight)
        try:
            table = self._sdk.tables.for_insight(self._workspace, insight)
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

        for result_row in table.read_all():
            row = dict()

            for column_name in columns:
                value = result_row[col_to_local_id[column_name]]
                sanitized = self._sanitize_value(column_name, value)
                row[column_name] = sanitized

            yield row

    def _sanitize_value(self, column_name: str, value: str) -> Any:
        """Alter the value to comply with postgres data type"""
        type_name = self._columns[column_name].base_type_name
        converter = DBTypeConverterStore.find_converter(type_name)
        return converter.to_type(value)

    def get_computable_for_col_name(self, column_name: str) -> Union[Attribute, Metric]:
        return _col_as_computable(self._columns[column_name])

    @staticmethod
    def _date_to_str(date: datetime.date) -> str:
        return date.strftime("%Y-%m-%d")

    def _get_date_filter(self, operator: str, value: datetime.date, label: ObjId) -> Union[Filter, None]:
        date_from = MIN_DATE
        date_to = MAX_DATE
        add_filter = True
        # AbsoluteDateFilter supports only day granularity
        # date_to must equal to qual.value + 1 day, if qual.value day is to be included
        if operator == ">=":
            date_from = self._date_to_str(value)
        elif operator == "<=":
            date_to = self._date_to_str(value + datetime.timedelta(days=1))
        elif operator == ">":
            date_from = self._date_to_str(value + datetime.timedelta(days=1))
        elif operator == "<":
            date_to = self._date_to_str(value)
        elif operator == "=":
            date_from = self._date_to_str(value)
            date_to = self._date_to_str(value + datetime.timedelta(days=1))
        else:
            add_filter = False

        if add_filter:
            date_filter = AbsoluteDateFilter(label, date_from, date_to)
            _log_debug(f"extract_filters_from_quals: date_filter={date_filter.__dict__}")
            return date_filter
        else:
            return None

    def qual_to_date_filter(self, filters: list[Filter], filter_entity: Attribute, qual: Qual) -> None:
        _log_debug(f"extract_filters_from_quals: filter_column={filter_entity} is date attribute")
        # Hack - Absolute date filter requires <date_dataset>.day label, but user can limit e.g. month granularity
        re_day = re.compile(r"(.*)\.[^.]+$")
        label = ObjId(re_day.sub(r"\1", filter_entity.label.id), "dataset")
        if isinstance(qual.operator, tuple):
            # Can't be implemented by multiple filters, because GD.CN does not support OR between filters
            _log_debug("extract_filters_from_quals: IN (date1, date2, ..) is not supported")
        else:
            date_filter = self._get_date_filter(qual.operator, qual.value, label)
            if date_filter:
                filters.append(date_filter)

    @staticmethod
    def qual_to_attribute_filter(filters: list[Filter], filter_entity: Attribute, qual: Qual) -> None:
        _log_debug(f"extract_filters_from_quals: filter_column={filter_entity} is normal attribute")
        if isinstance(qual.operator, tuple):
            values = qual.value
            positive = qual.operator[1]
        else:
            values = [qual.value]
            positive = qual.operator == "="
        _log_debug(f"extract_filters_from_quals: values={values} positive={positive}")
        if positive:
            filters.append(PositiveAttributeFilter(filter_entity, values))
        else:
            filters.append(NegativeAttributeFilter(filter_entity, values))

    @staticmethod
    def _is_qual_date(qual: Qual) -> bool:
        return isinstance(qual.value, datetime.date) or (
            isinstance(qual.value, list) and isinstance(qual.value[0], datetime.date)
        )

    def extract_filters_from_quals(self, quals: list[Qual]) -> list[Filter]:
        """
        Convert quals to Attribute filters.
        Now only simple attribute filters are supported.

        :param quals: multicorn quals representing filters in SQL WHERE clause
        :return: Attribute filters
        """
        filters: list[Filter] = []
        for qual in quals:
            _log_info(
                f"extract_filters_from_quals: field_name={qual.field_name} operator={qual.operator} value={qual.value}"
            )
            filter_entity = self.get_computable_for_col_name(qual.field_name)
            if filter_entity:
                if isinstance(filter_entity, Attribute):
                    _log_debug(f"extract_filters_from_quals: filter_entity={filter_entity} is attribute")
                    if self._is_qual_date(qual):
                        self.qual_to_date_filter(filters, filter_entity, qual)
                    else:
                        self.qual_to_attribute_filter(filters, filter_entity, qual)
                else:
                    _log_info(
                        f"extract_filters_from_quals: field_name={qual.field_name} is not attribute, "
                        + f"but {type(filter_entity)}"
                    )
            else:
                _log_info(
                    f"extract_filters_from_quals: field_name={qual.field_name} not found in report columns, "
                    + "cannot push it down"
                )
        return filters

    def _execute_compute(  # type: ignore
        self, quals: list[Qual], columns: list[str], sortKeys: Optional[list[Any]] = None
    ):
        """
        Computes data for the 'compute' pseudo-table. The 'compute' table is special. It does not behave as other
        relational tables: the input columns determine what data will be calculated and the cardinality of the result
        fully depends on the input columns.
        """
        try:
            items = [self.get_computable_for_col_name(col_name) for col_name in columns]
            # TODO: push down more filters that are included in quals
            filters = self.extract_filters_from_quals(quals)
            table = self._sdk.tables.for_items(self._workspace, items, filters)
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

        for row in table.read_all():
            sanitized_row = {k: self._sanitize_value(k, v) for k, v in row.items()}
            _log_debug(f"ROW={sanitized_row}")
            yield sanitized_row

    def _execute_custom_report(  # type: ignore
        self, quals: list[Qual], columns: list[str], sortKeys: Optional[list[Any]] = None
    ):
        """
        Computes data for manually created table that maps to particular workspace and its columns map to label, fact or
        metric in that workspace. The mapping conventions are same as for the 'compute' pseudo-table. Compared to the
        pseudo-table though, the custom report execution always computes data for all columns - thus appears like
        any other relational table.
        """
        try:
            items = [_col_as_computable(col) for col in self._columns.values()]
            # TODO: pushdown more filters that are included in quals
            filters = self.extract_filters_from_quals(quals)
            table = self._sdk.tables.for_items(self._workspace, items, filters)
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

        for row in table.read_all():
            sanitized_row = {k: self._sanitize_value(k, v) for k, v in row.items()}
            yield sanitized_row

    def execute(self, quals: list[Qual], columns: list[str], sortkeys: Optional[list[Any]] = None):  # type: ignore
        _log_debug(f"query in fdw with options {self._options}; columns {columns}; quals={quals}")

        if self._insight:
            result = self._execute_insight(quals, columns, sortkeys)
        elif self._compute:
            result = self._execute_compute(quals, columns, sortkeys)
        else:
            result = self._execute_custom_report(quals, columns, sortkeys)
        return result

    @classmethod
    def import_schema(
        cls,
        schema: str,
        srv_options: dict[str, str],
        options: dict[str, str],
        restriction_type: Optional[str],
        restricts: list[str],
    ) -> list[TableDefinition]:  # type: ignore
        _log_info(
            f"import fdw {schema} (srv_options={srv_options}, "
            f"options={options}, restriction_type={restriction_type}, restricts={restricts})"
        )

        if "host" not in srv_options or "token" not in srv_options:
            raise ValueError("server OPTIONS must contain 'host' and 'token' keys.")

        if "object_type" not in options:
            raise ValueError(
                "gooddata_fdw: IMPORT SCHEMA OPTIONS must contain 'object_type' key "
                "to indicate type of object to be imported"
            )
        else:
            object_type = options["object_type"]
            if object_type not in ["insights", "compute", "all"]:
                raise ValueError(
                    f"gooddata_fdw: IMPORT SCHEMA OPTION 'object_type' unsupported value '{object_type}'."
                    + " Supported values are: 'insights', 'compute', 'all'"
                )
        if "numeric_max_size" in options:
            metric_digits_before_dec_point = options["numeric_max_size"]
        else:
            metric_digits_before_dec_point = METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT

        host = srv_options["host"]

        if not host.startswith("https://") and not host.startswith("http://"):
            raise ValueError(
                "gooddata_fdw: your server is not defined correctly. The host must start with https:// or http://"
            )

        tables = []
        # (Source) schema represents GoodData workspace
        # Insight name `compute` is not allowed and filtered out inside the import_insights_from_workspace()
        try:
            if object_type in ["insights", "all"]:
                tables += cls.import_insights_from_workspace(
                    schema, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
                )
            if object_type in ["compute", "all"]:
                tables += cls.import_semantic_layer_from_workspace(
                    schema, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
                )
            return tables
        except Exception as e:
            _log_error(traceback.format_exc())
            raise e

    @classmethod
    def import_insights_from_workspace(
        cls,
        workspace: str,
        srv_options: dict[str, str],
        options: dict[str, str],
        metric_digits_before_dec_point: str,
        restriction_type: Optional[str],
        restricts: list[str],
    ) -> list[TableDefinition]:
        table_naming = DefaultInsightTableNaming()

        _log_info(
            f"importing insights as tables from {srv_options['host']} workspace {workspace} "
            + f"headers_host={srv_options.get('headers_host')}"
        )
        _sdk = create_sdk(srv_options["host"], srv_options["token"], USER_AGENT, srv_options.get("headers_host"))
        _log_debug("loading full catalog")
        catalog = _sdk.catalog.get_full_catalog(workspace)
        _log_debug("loading all insights")
        insights = _sdk.insights.get_insights(workspace)

        tables = []

        for insight in insights:
            if not insight.are_relations_valid:
                _log_warn(f"Insight title={insight.title} id={insight.id} is invalid, we cannot import it.")
                continue
            table_name = table_naming.table_name_for_insight(insight)
            _log_info(f'creating table def "{table_name}" for insight "{insight.title}"')

            column_naming = DefaultInsightColumnNaming()
            columns = []

            for attr in insight.attributes:
                column_name = column_naming.col_name_for_attribute(attr)
                _log_debug(f'creating col def "{column_name}" for attribute "{attr.label_id}"')

                label_id = ObjId(id=attr.label_id, type="label")
                data_type = column_data_type_for(catalog.find_label_attribute(label_id))

                col = ColumnDefinition(
                    column_name=column_name,
                    type_name=data_type,
                    options=dict(id=f"label/{attr.label_id}", local_id=attr.local_id),
                )
                columns.append(col)

            for metric in insight.metrics:
                # TODO - distinguish facts and metrics better when loading insights
                if metric.format:
                    metric_obj_type = "fact"
                else:
                    metric_obj_type = "metric"
                metric_format = get_insight_metric_format(metric, catalog)
                data_type = metric_format_to_data_type(metric_format, metric_digits_before_dec_point)
                column_name = column_naming.col_name_for_metric(metric)
                _log_debug(
                    f'creating col def "{column_name}" for metric "{metric.title}(id={metric.item_id})" '
                    + f"format={metric_format} data_type={data_type}"
                )
                col = ColumnDefinition(
                    column_name=column_name,
                    type_name=data_type,
                    options=dict(id=f"{metric_obj_type}/{metric.item_id}", local_id=metric.local_id),
                )
                columns.append(col)

            if table_name == "compute":
                _log_warn("Insight name may not equal to `compute` used by import_semantic_layer_from_workspace()")
            else:
                table = TableDefinition(
                    table_name=table_name,
                    columns=columns,
                    options=dict(workspace=workspace, insight=insight.id),
                )
                tables.append(table)

        return tables

    @classmethod
    def import_semantic_layer_from_workspace(
        cls,
        workspace: str,
        srv_options: dict[str, str],
        options: dict[str, str],
        metric_digits_before_dec_point: str,
        restriction_type: Optional[str],
        restricts: list[str],
    ) -> list[TableDefinition]:
        _log_info(
            f"importing semantic layer as tables from {srv_options['host']} workspace {workspace} "
            + f"headers_host={srv_options.get('headers_host')}"
        )

        _sdk = create_sdk(srv_options["host"], srv_options["token"], USER_AGENT, srv_options.get("headers_host"))

        catalog = _sdk.catalog.get_full_catalog(workspace)
        columns = []
        naming = DefaultCatalogNamingStrategy()

        for metric in catalog.metrics:
            column_name = naming.col_name_for_metric(metric)
            metric_format = metric.format
            data_type = metric_format_to_data_type(metric_format, metric_digits_before_dec_point)

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
                        type_name=get_metric_data_type(
                            metric_digits_before_dec_point, METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT
                        ),
                        options=dict(id=f"fact/{fact.id}"),
                    )
                )

            for attribute in dataset.attributes:
                for label in attribute.labels:
                    column_name = naming.col_name_for_label(label, dataset)
                    data_type = column_data_type_for(attribute)

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
                options=dict(workspace=workspace, compute="pseudo-table"),
            )
        ]

    @property
    def rowid_column(self):  # type: ignore
        return super().rowid_column

    def insert(self, values):  # type: ignore
        return super().insert(values)

    def update(self, oldvalues, newvalues):  # type: ignore
        return super().update(oldvalues, newvalues)

    def delete(self, oldvalues):  # type: ignore
        return super().delete(oldvalues)
