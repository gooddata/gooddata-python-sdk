# (C) 2021 GoodData Corporation
from logging import ERROR, INFO, DEBUG, WARNING, CRITICAL
from operator import itemgetter

from multicorn import ForeignDataWrapper, TableDefinition, ColumnDefinition
from multicorn.utils import log_to_postgres

import gooddata_sdk as sdk

_IN_POSTGRES = True
_USER_AGENT = "gooddata-fdw/0.1"


def log_to_console():
    global _IN_POSTGRES
    _IN_POSTGRES = False


def _log_debug(msg):
    if not _IN_POSTGRES:
        print(f"DEBUG: gooddata_fdw: {msg}")
    else:
        log_to_postgres(f"gooddata_fdw: {msg}", level=DEBUG)


def _log_info(msg):
    if not _IN_POSTGRES:
        print(f"INFO: gooddata_fdw: {msg}")
    else:
        log_to_postgres(f"gooddata_fdw: {msg}", level=INFO)


def _log_warn(msg):
    if not _IN_POSTGRES:
        print(f"WARNING: gooddata_fdw: {msg}")
    else:
        log_to_postgres(f"gooddata_fdw: {msg}", level=WARNING)


def _log_error(msg):
    if not _IN_POSTGRES:
        print(f"ERROR: gooddata_fdw: {msg}")
    else:
        log_to_postgres(f"gooddata_fdw: {msg}", level=ERROR)


def _log_critical(msg):
    if not _IN_POSTGRES:
        print(f"CRITICAL: gooddata_fdw: {msg}")
    else:
        log_to_postgres(f"gooddata_fdw: {msg}", level=CRITICAL)


def _sanitize_str_for_postgres(string, used_names=None):
    # replace non-alpha-num stuff with underscores
    with_underscores = ''.join(char if char.isalnum() else '_' for char in string.lower())

    # then get rid of sequences of underscores
    candidate = '_'.join([s for s in with_underscores.split('_') if s != ''])

    if used_names is None:
        return candidate

    return _ensure_unique(candidate, used_names)


def _ensure_unique(candidate, used_names):
    # ensure column name uniqueness - in a dumb way by appending some number
    if candidate in used_names:
        i = 1
        new_candidate = f'{candidate}_{i}'

        while new_candidate in used_names:
            i += 1
            new_candidate = f'{candidate}_{i}'

        return new_candidate

    return candidate


#
# Column naming during IMPORT SCHEMA is delegated to strategies. The idea is that we may want to support
# different strategies and let user select the desired one through OPTIONS during import.
#

class InsightTableNamingStrategy:
    def table_name_for_insight(self, insight: sdk.Insight) -> str:
        raise NotImplementedError()


class DefaultInsightTableNaming(InsightTableNamingStrategy):
    def __init__(self):
        self._uniques = dict()

    def table_name_for_insight(self, insight: sdk.Insight) -> str:
        new_name = _sanitize_str_for_postgres(insight.title, self._uniques)
        self._uniques[new_name] = True

        return new_name


class InsightColumnNamingStrategy:
    def col_name_for_attribute(self, attr: sdk.InsightAttribute) -> str:
        raise NotImplementedError()

    def col_name_for_measure(self, attr: sdk.InsightAttribute) -> str:
        raise NotImplementedError()


class DefaultInsightColumnNaming(InsightColumnNamingStrategy):
    def __init__(self):
        self._uniques = dict()

    def col_name_for_attribute(self, attr: sdk.InsightAttribute) -> str:
        new_name = _sanitize_str_for_postgres(attr.label_id, self._uniques)
        self._uniques[new_name] = True

        return new_name

    def col_name_for_measure(self, measure: sdk.InsightMeasure) -> str:
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        # TODO: improve this heuristic to get better names for derived measures
        id_to_use = measure.item_id or measure.alias or measure.title or measure.local_id
        new_name = _sanitize_str_for_postgres(id_to_use, self._uniques)
        self._uniques[new_name] = True

        return new_name


class CatalogNamingStrategy:
    def col_name_for_label(self, attr: sdk.CatalogLabel) -> str:
        raise NotImplementedError()

    def col_name_for_fact(self, attr: sdk.CatalogFact) -> str:
        raise NotImplementedError()

    def col_name_for_metric(self, attr: sdk.CatalogMetric) -> str:
        raise NotImplementedError()


class DefaultCatalogNamingStrategy:
    def __init__(self):
        self._uniques = dict()

    def col_name_for_label(self, label: sdk.CatalogLabel, dataset: sdk.CatalogDataset) -> str:
        ds_prefix = f"{dataset.id}."
        # some of our tests project have convention where fact/label is as: dataset.dataset_something
        # that looks awkward in a table.. thus this funny stuff
        use_id = label.id if not label.id.startswith(f"{ds_prefix}{dataset.id}") else label.id[len(ds_prefix):]
        new_name = _sanitize_str_for_postgres(use_id, self._uniques)
        self._uniques[new_name] = True

        return new_name

    def col_name_for_fact(self, fact: sdk.CatalogFact, dataset: sdk.CatalogDataset) -> str:
        ds_prefix = f"{dataset.id}."
        # some of our tests project have convention where fact/label is as: dataset.dataset_something
        # that looks awkward in a table.. thus this funny stuff
        use_id = fact.id if not fact.id.startswith(f"{ds_prefix}{dataset.id}") else fact.id[len(ds_prefix):]
        new_name = _sanitize_str_for_postgres(use_id, self._uniques)
        self._uniques[new_name] = True

        return new_name

    def col_name_for_metric(self, metric: sdk.CatalogMetric) -> str:
        new_name = _sanitize_str_for_postgres(metric.id, self._uniques)
        self._uniques[new_name] = True

        return new_name


#
#
#

def _col_as_computable(col: ColumnDefinition):
    item_type, item_id = col.options['id'].split('/')

    # since all cols are from the compute table, the uniqueness of local_id is ensured...
    if item_type == 'label':
        return sdk.Attribute(local_id=col.column_name, label=item_id)
    else:
        aggregation = col.options['agg'] if 'agg' in col.options else None

        return sdk.SimpleMeasure(local_id=col.column_name, item=sdk.ObjId(item_id, item_type), aggregation=aggregation)


#
#
#

class GoodDataForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, options, columns):
        super(GoodDataForeignDataWrapper, self).__init__(options, columns)

        if 'host' not in options or 'token' not in options:
            raise ValueError("server OPTIONS must contain 'host' and 'token' keys.")

        if 'workspace' not in options:
            raise ValueError(
                "attempting to work with an incorrectly defined foreign table."
                "Table must contain both 'workspace'.")

        _log_debug(f'initializing (options={options}, columns={columns})')

        self._host, self._token, self._workspace = itemgetter('host', 'token', 'workspace')(
            options)
        self._options = options
        self._columns = columns
        self._insight = options['insight'] if 'insight' in options else None
        self._compute = options['compute'] if 'compute' in options else None
        self._sdk = sdk.GoodDataSdk(host=self._host, token=self._token, extra_user_agent=_USER_AGENT)

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
                if 'local_id' not in c.options:
                    raise ValueError(f"Foreign table column '{c.column_name}' is not defined correctly. "
                                     f"For tables that map GoodData.CN insight, the column OPTIONS must specify "
                                     f"'localId' which is localIdentifier of the Insight's bucket item. If you created "
                                     f"this table manually, please rather use the IMPORT FOREIGN SCHEMA and import "
                                     f"from the 'gooddata_insights' schema. The import will set everything correctly.")

            return

        for c in self._columns.values():
            if 'id' not in c.options:
                raise ValueError(f"Foreign table column '{c.column_name}' is not defined correctly. "
                                 f"For tables mapping to GoodData.CN semantic layer, the column OPTIONS must specify "
                                 f"'id' which in format: 'fact/your.fact.id', 'label/your.label.id', "
                                 f"'metric/your.metric.id'.")
            else:
                split = c.options['id'].split('/')

                if len(split) > 2 or split[0] not in ('fact', 'label', 'metric'):
                    raise ValueError(f"Foreign table column '{c.column_name}' is not defined correctly. "
                                     f"For tables mapping to GoodData.CN semantic layer, the column OPTIONS must "
                                     f"specify 'id' which in format: 'fact/your.fact.id', 'label/your.label.id', "
                                     f"'metric/your.metric.id'. Instead got: {c.options['id']}")

    def _execute_insight(self, quals, columns, sortKeys=None):
        """
        Computes data for table mapped to an insight. Note that this execution maintains insight's filters - the
        table is implicitly filtered.
        """
        # TODO add validation that the table columns are consistent with insight bucket items

        col_to_local_id = dict([(c.column_name, c.options['local_id']) for c in self._columns.values()])
        insight = self._sdk.insights.get_insight(self._workspace, self._insight)
        table = self._sdk.tables.for_insight(self._workspace, insight)

        for result_row in table.read_all():
            row = dict()

            # TODO: it is likely that conversion to DATE/TIMESTAMP will have to happen here if the column is of
            #  the respective type
            for column_name in columns:
                row[column_name] = result_row[col_to_local_id[column_name]]

            yield row

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

        # TODO: it is likely that this has to change to support DATE and TIMESTAMP. have mapping that need to be
        #  timestamp/date, instead of returning generator, iterate rows, convert to dates and yield the converted row
        return table.read_all()

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
        _log_debug(f'query in fdw with options {self._options}; columns {type(columns)}')

        if self._insight:
            return self._execute_insight(quals, columns, sortkeys)
        if self._compute:
            return self._execute_compute(quals, columns, sortkeys)

        return self._execute_custom_report(quals, columns, sortkeys)

    @classmethod
    def import_schema(cls, schema, srv_options, options, restriction_type, restricts):
        _log_info(
            f"import fdw schema {schema} (srv_options={srv_options}, "
            f"options={options}, restriction_type={restriction_type}, restricts={restricts})"
        )

        if 'host' not in srv_options or 'token' not in srv_options:
            raise ValueError("server OPTIONS must contain 'host' and 'token' keys.")

        if 'workspace' not in options:
            raise ValueError(
                "gooddata_fdw: IMPORT SCHEMA OPTIONS must contain 'workspace' key "
                "to indicate workspace from which to import.")

        host = srv_options['host']

        if not host.startswith('https://') and not host.startswith('http://'):
            raise ValueError('gooddata_fdw: your server is not defined correctly. '
                             'The host must start with https:// or http://')

        if schema == 'gooddata_insights':
            return cls.import_insights_from_workspace(schema, srv_options, options, restriction_type, restricts)
        elif schema == 'gooddata_compute':
            return cls.import_semantic_layer_from_workspace(schema, srv_options, options, restriction_type, restricts)

        raise NotImplementedError(
            f"This FDW does not support IMPORT FOREIGN SCHEMA for {schema}")

    @classmethod
    def import_insights_from_workspace(cls, schema, srv_options, options, restriction_type, restricts):
        workspace = options['workspace']
        table_naming = DefaultInsightTableNaming()

        _log_info(
            f"importing insights as tables from {srv_options['host']} workspace {options['workspace']}")

        _sdk = sdk.GoodDataSdk(host=srv_options['host'], token=srv_options['token'],
                               extra_user_agent=_USER_AGENT)

        # TODO catalog will be needed to correctly identify cols that contain date/timestamp; skipping for now
        # _log_debug(f"loading full catalog")
        # catalog_service = sdk.CatalogService(client)
        # catalog = catalog_service.get_full_catalog(workspace)

        _log_debug(f"loading all insights")
        insights = _sdk.insights.get_insights(workspace)

        tables = []

        for insight in insights:
            table_name = table_naming.table_name_for_insight(insight)
            _log_info(f"creating table def {table_name} for insight {insight.title}")

            column_naming = DefaultInsightColumnNaming()
            columns = []

            for attr in insight.attributes:
                column_name = column_naming.col_name_for_attribute(attr)
                _log_debug(f"creating col def {column_name} for attribute {attr}")

                col = ColumnDefinition(column_name=column_name, type_name='VARCHAR(256)',
                                       options=dict(local_id=attr.local_id))
                columns.append(col)

            for measure in insight.measures:
                column_name = column_naming.col_name_for_measure(measure)
                _log_debug(f"creating col def {column_name} for measure {measure}")

                col = ColumnDefinition(column_name=column_name, type_name='DECIMAL(15,5)',
                                       options=dict(local_id=measure.local_id))
                columns.append(col)

            table = TableDefinition(table_name=table_name, columns=columns,
                                    options=dict(workspace=workspace, insight=insight.id))
            tables.append(table)

        return tables

    @classmethod
    def import_semantic_layer_from_workspace(cls, schema, srv_options, options, restriction_type, restricts):
        workspace = options['workspace']

        _log_info(
            f"importing semantic layer as tables from {srv_options['host']} workspace {options['workspace']}")

        _sdk = sdk.GoodDataSdk(host=srv_options['host'], token=srv_options['token'],
                               extra_user_agent=_USER_AGENT)

        catalog = _sdk.catalog.get_full_catalog(workspace)
        columns = []
        naming = DefaultCatalogNamingStrategy()

        for metric in catalog.metrics:
            column_name = naming.col_name_for_metric(metric)

            _log_info(f"metric {metric.id} mapped to column {column_name}")

            columns.append(ColumnDefinition(column_name=column_name,
                                            type_name='DECIMAL(15,5)',
                                            options=dict(id=f'metric/{metric.id}')))

        for dataset in catalog.datasets:
            for fact in dataset.facts:
                column_name = naming.col_name_for_fact(fact, dataset)

                _log_info(f"fact {fact.id} mapped to column {column_name}")

                columns.append(ColumnDefinition(column_name=column_name,
                                                type_name='DECIMAL(15,5)',
                                                options=dict(id=f'fact/{fact.id}')))

            for attribute in dataset.attributes:
                # TODO: correctly identify cols that should be DATE or TIMESTAMP. skipping for now because
                #  can't be bothered doing the date conversions
                for label in attribute.labels:
                    column_name = naming.col_name_for_label(label, dataset)

                    _log_info(f"label {label.id} mapped to column {column_name}")

                    columns.append(ColumnDefinition(column_name=column_name,
                                                    type_name='VARCHAR(256)',
                                                    options=dict(id=f'label/{label.id}')))

        return [TableDefinition(table_name="compute",
                                columns=columns,
                                options=dict(workspace=workspace, compute="pseudo-table"))]

    @property
    def rowid_column(self):
        return super().rowid_column

    def insert(self, values):
        return super().insert(values)

    def update(self, oldvalues, newvalues):
        return super().update(oldvalues, newvalues)

    def delete(self, oldvalues):
        return super().delete(oldvalues)
