# (C) 2021 GoodData Corporation
import json
import os
import re
from operator import itemgetter

import gooddata_sdk as sdk
from gooddata_fdw.environment import ColumnDefinition, ForeignDataWrapper, TableDefinition
from gooddata_fdw.logging import _log_debug, _log_error, _log_info, _log_warn
from gooddata_fdw.naming import DefaultCatalogNamingStrategy, DefaultInsightColumnNaming, DefaultInsightTableNaming
from gooddata_sdk.catalog import Catalog
from gooddata_sdk.compute_model import ObjId
from gooddata_sdk.insight import InsightMetric

_USER_AGENT = "gooddata-fdw/0.1"
"""
Extra segment of the User-Agent header that will be appended to standard gooddata-sdk user agent.
"""

DEFAULT_ATTRIBUTE_DATATYPE = "VARCHAR(255)"
METRIC_DATA_TYPE = "DECIMAL"
METRIC_DIGITS_BEFORE_DEC_POINT_DEFAULT = "18"
METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT = "2"


def _col_as_computable(col: ColumnDefinition):
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


def _create_sdk(host, token):
    """Return GoodDataSdk instance."""
    headers = os.environ.get("GOODDATA_SDK_HTTP_HEADERS", None)
    if headers:
        try:
            headers = json.loads(headers)
            assert isinstance(headers, dict), "Not a dictionary"
        except (AssertionError, json.JSONDecodeError) as e:
            _log_error(
                "environment variable GOODDATA_SDK_HTTP_HEADERS contains data in bad format. Json object expected."
            )
            raise e
    client = sdk.client.GoodDataApiClient(host, token, custom_headers=headers, extra_user_agent=_USER_AGENT)
    return sdk.GoodDataSdk(client)


def column_data_type_for(attribute):
    """Determine what postgres type should be used for `attribute`."""
    declared_data_type = attribute.dataset.data_type
    granularity = attribute.granularity
    return {
        "DATE": date_granularity_to_data_type(granularity),
        "NORMAL": DEFAULT_ATTRIBUTE_DATATYPE,
    }.get(declared_data_type, DEFAULT_ATTRIBUTE_DATATYPE)


def date_granularity_to_data_type(granularity):
    """Determine what postgres type should be used for an attribute of type date based on `granularity`."""
    return {
        "MINUTE": "TIMESTAMP",  # No conversion needed
        "HOUR": "TIMESTAMP",  # Add minutes
        "DAY": "DATE",  # No conversion needed
        "WEEK": DEFAULT_ATTRIBUTE_DATATYPE,
        "MONTH": "DATE",  # Add day
        "QUARTER": DEFAULT_ATTRIBUTE_DATATYPE,
        "YEAR": "INTEGER",
    }.get(granularity, "INTEGER")


# InsightMetric do not contain format in case of stored metrics
def get_insight_metric_format(metric: InsightMetric, catalog: Catalog) -> str:
    metric_id = ObjId(id=metric.item_id, type="metric")
    full_metric = catalog.get_metric(metric_id)
    return metric.format or full_metric.format


def get_metric_data_type(metric_digits_before_dec_point: str, digits_after: str) -> str:
    return f"{METRIC_DATA_TYPE}({metric_digits_before_dec_point}, {digits_after})"


def metric_format_to_data_type(metric_format: str, metric_digits_before_dec_point: str) -> str:
    re_decimal_places = re.compile(r"^[^.]+\.([#0]+)")
    match = re_decimal_places.search(metric_format)
    if match:
        digits_after = str(len(match.group(1)))
    else:
        digits_after = METRIC_DIGITS_AFTER_DEC_POINT_DEFAULT
    return get_metric_data_type(metric_digits_before_dec_point, digits_after)


class GoodDataForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
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
        self._insight = options["insight"] if "insight" in options else None
        self._compute = options["compute"] if "compute" in options else None
        self._sdk = _create_sdk(self._host, self._token)

        self._validate()

    def _validate(self):
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

    def _execute_insight(self, quals, columns, sortKeys=None):
        """
        Computes data for table mapped to an insight. Note that this execution maintains insight's filters - the
        table is implicitly filtered.
        """
        # TODO add validation that the table columns are consistent with insight bucket items

        col_to_local_id = dict([(c.column_name, c.options["local_id"]) for c in self._columns.values()])
        insight = self._sdk.insights.get_insight(self._workspace, self._insight)
        table = self._sdk.tables.for_insight(self._workspace, insight)

        for result_row in table.read_all():
            row = dict()

            for column_name in columns:
                value = result_row[col_to_local_id[column_name]]
                sanitized = self._sanitize_value(column_name, value)
                row[column_name] = sanitized

            yield row

    def _sanitize_value(self, column_name, value):
        """Alter the value to comply with postgres data type"""
        type_name = self._columns[column_name].base_type_name

        sanitizations = {
            "date": self._sanitize_date,
            "timestamp without time zone": self._sanitize_timestamp,
            "timestamp": self._sanitize_timestamp,
        }
        if type_name in sanitizations:
            return sanitizations[type_name](value)
        else:
            return value

    def _sanitize_date(self, value):
        """Add first month and first date to incomplete iso date string.

        >>>assert self._sanitize_date("2021-01") == "2021-01-01"
        >>>assert self._sanitize_date("1992") == "1992-01-01"
        """
        parts = value.split("-")
        missing_count = 3 - len(parts)
        for i in range(0, missing_count):
            parts.append("01")
        return "-".join(parts)

    def _sanitize_timestamp(self, value):
        """Append minutes to incomplete datetime string.

        >>>assert self._sanitize_timestamp("2021-01-01 02") == "2021-01-01 02:00"
        >>>assert self._sanitize_timestamp("2021-01-01 12:34") == "2021-01-01 12:34"
        """
        parts = value.split(":")
        if len(parts) == 1:
            value = value + ":00"
        return value

    def get_computable_for_col_name(self, column_name):
        return _col_as_computable(self._columns[column_name])

    def _execute_compute(self, quals, columns, sortKeys=None):
        """
        Computes data for the 'compute' pseudo-table. The 'compute' table is special. It does not behave as other
        relational tables: the input columns determine what data will be calculated and the cardinality of the result
        fully depends on the input columns.
        """
        # TODO: pushdown some of the filters that are included in quals
        items = [self.get_computable_for_col_name(col_name) for col_name in columns]
        table = self._sdk.tables.for_items(self._workspace, items)

        for row in table.read_all():
            sanitized_row = {k: self._sanitize_value(k, v) for k, v in row.items()}
            yield sanitized_row

    def _execute_custom_report(self, quals, columns, sortKeys=None):
        """
        Computes data for manually created table that maps to particular workspace and its columns map to label, fact or
        metric in that workspace. The mapping conventions are same as for the 'compute' pseudo-table. Compared to the
        pseudo-table though, the custom report execution always computes data for all columns - thus appears like
        any other relational table.
        """
        # TODO: pushdown some of the filters that are included in quals
        items = [_col_as_computable(col) for col in self._columns.values()]
        table = self._sdk.tables.for_items(self._workspace, items)

        # TODO: it is likely that this has to change to support DATE and TIMESTAMP. have mapping that need to be
        #  timestamp/date, instead of returning generator, iterate rows, convert to dates and yield the converted row
        # note: no need to filter result rows to only those that are SELECTed.. multicorn/postgres takes care of
        # that
        return table.read_all()

    def execute(self, quals, columns, sortkeys=None):
        _log_debug(f"query in fdw with options {self._options}; columns {type(columns)}")

        if self._insight:
            return self._execute_insight(quals, columns, sortkeys)
        if self._compute:
            return self._execute_compute(quals, columns, sortkeys)

        return self._execute_custom_report(quals, columns, sortkeys)

    @classmethod
    def import_schema(cls, schema, srv_options, options, restriction_type, restricts):
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
        if object_type in ["insights", "all"]:
            tables += cls.import_insights_from_workspace(
                schema, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
            )
        if object_type in ["compute", "all"]:
            tables += cls.import_semantic_layer_from_workspace(
                schema, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
            )
        return tables

    @classmethod
    def import_insights_from_workspace(
        cls, workspace, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
    ):
        table_naming = DefaultInsightTableNaming()

        _log_info(f"importing insights as tables from {srv_options['host']} workspace {workspace}")
        _sdk = _create_sdk(srv_options["host"], srv_options["token"])
        _log_debug("loading full catalog")
        catalog = _sdk.catalog.get_full_catalog(workspace)
        _log_debug("loading all insights")
        insights = _sdk.insights.get_insights(workspace)

        tables = []

        for insight in insights:
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
                    options=dict(local_id=attr.local_id),
                )
                columns.append(col)

            for metric in insight.metrics:
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
                    options=dict(local_id=metric.local_id),
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
        cls, workspace, srv_options, options, metric_digits_before_dec_point, restriction_type, restricts
    ):
        _log_info(f"importing semantic layer as tables from {srv_options['host']} workspace {workspace}")

        _sdk = _create_sdk(srv_options["host"], srv_options["token"])

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
    def rowid_column(self):
        return super().rowid_column

    def insert(self, values):
        return super().insert(values)

    def update(self, oldvalues, newvalues):
        return super().update(oldvalues, newvalues)

    def delete(self, oldvalues):
        return super().delete(oldvalues)
