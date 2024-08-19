# (C) 2023 GoodData Corporation
import json
import re
from typing import Optional

import attrs
from gooddata_sdk import CatalogDeclarativeMetric, CatalogDeclarativeModel

from gooddata_dbt.dbt.base import DBT_PATH_TO_MANIFEST, Base
from gooddata_dbt.dbt.tables import DbtModelBase

DBT_TO_GD_CALC_METHODS = {
    "count_distinct": "COUNT",
    "sum": "SUM",
    "average": "AVG",
    "min": "MIN",
    "max": "MAX",
}

DBT_TO_GD_FILTER_OPERATORS = {
    "!=": "<>",
    "is": "=",
    "is not": "<>",
}


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataMetricProps(Base):
    model_id: Optional[str] = None
    format: Optional[str] = None


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetaGoodDataMetric(Base):
    gooddata: DbtModelMetaGoodDataMetricProps = attrs.field(factory=DbtModelMetaGoodDataMetricProps)


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetricFilter(Base):
    field: str
    operator: str
    value: str


@attrs.define(auto_attribs=True, kw_only=True)
class DbtModelMetric(DbtModelBase):
    label: str
    meta: DbtModelMetaGoodDataMetric
    model: str
    calculation_method: str
    expression: str
    filters: Optional[list[DbtModelMetricFilter]] = None


class DbtModelMetrics:
    def __init__(self, model_ids: Optional[list[str]], ldm: CatalogDeclarativeModel) -> None:
        self.model_ids = model_ids
        self.ldm = ldm
        with open(DBT_PATH_TO_MANIFEST) as fp:
            self.dbt_catalog = json.load(fp)

    @property
    def metrics(self) -> list[DbtModelMetric]:
        result = [DbtModelMetric.from_dict(metric_def) for metric_def in self.dbt_catalog["metrics"].values()]
        # Return only gooddata labelled tables marked by model_id (if requested in args)
        return [
            r
            for r in result
            if r.meta.gooddata is not None and (not self.model_ids or r.meta.gooddata.model_id in self.model_ids)
        ]

    @staticmethod
    def extract_table_from_model(model: str) -> str:
        re_model = re.compile(r"ref\('([^']+)'\)")
        if (model_match := re_model.search(model)) is not None:
            return model_match.group(1)
        else:
            raise Exception("dbt model not specified by ref('xxx'), such breaking change not supported")

    def get_entity_type(self, table_name: str, expression_entity: str) -> str:
        result = None
        expression_entity_cmp = expression_entity.lower()
        if self.ldm.ldm is None:
            raise Exception("LDM cannot be None.")
        for dataset in self.ldm.ldm.datasets:
            table_id = dataset.data_source_table_id
            if table_id is not None and table_id.id.lower() == table_name.lower():
                attributes = dataset.attributes if dataset.attributes else []
                facts = dataset.facts if dataset.facts else []
                for attribute in attributes:
                    if attribute.source_column.lower() == expression_entity_cmp:
                        result = "label"
                    for label in attribute.labels:
                        if label.source_column.lower() == expression_entity_cmp:
                            result = "label"
                for fact in facts:
                    if fact.source_column.lower() == expression_entity_cmp:
                        result = "fact"
        for date_dataset in self.ldm.ldm.date_instances:
            if date_dataset.id.lower() == expression_entity_cmp:
                result = "date"
        if result:
            return result
        else:
            raise Exception(f"Unsupported entity type {table_name=} {expression_entity=}")

    def make_entity_id(self, table_name: str, token: str) -> Optional[str]:
        entity_type = self.get_entity_type(table_name, token)
        if not entity_type:
            return None
        full_entity_name = token
        final_entity_type = entity_type
        if entity_type == "date":
            # TODO - not sure how date dims are handled in dbt models, cannot find it in DOC
            full_entity_name = f"{token}.day"
            final_entity_type = "label"
        return f" {{{final_entity_type}/{full_entity_name}}}"

    def resolve_entities_in_expression(self, expression: str, table_name: str) -> str:
        re_split = re.compile(r"\s+")
        tokens = re_split.split(expression)
        result_tokens = []
        for token in tokens:
            entity_id = self.make_entity_id(table_name, token)
            result_tokens.append(entity_id or token)
        return " ".join(result_tokens)

    def make_gooddata_filter(self, table_name: str, dbt_filters: Optional[list[DbtModelMetricFilter]] = None) -> str:
        # TODO - Quite naive implementation
        #    e.g. missing polishing of values (e.g. SQL vs MAQL enclosers)
        gd_maql_filters = []
        dbt_filters = dbt_filters if dbt_filters is not None else []
        for dbt_filter in dbt_filters:
            entity_id = self.make_entity_id(table_name, dbt_filter.field)
            operator = DBT_TO_GD_FILTER_OPERATORS.get(dbt_filter.operator, dbt_filter.operator)
            gd_maql_filters.append(f"{entity_id} {operator} {dbt_filter.value}")
        if gd_maql_filters:
            return " WHERE " + " AND ".join(gd_maql_filters)
        else:
            return ""

    def make_gooddata_metrics(self) -> list[CatalogDeclarativeMetric]:
        gd_metrics = []
        for dbt_metric in self.metrics:
            calculation_method = DBT_TO_GD_CALC_METHODS.get(dbt_metric.calculation_method)
            if calculation_method:
                table_name = self.extract_table_from_model(dbt_metric.model)
                expression = self.resolve_entities_in_expression(dbt_metric.expression, table_name)
                gd_filter = self.make_gooddata_filter(table_name, dbt_metric.filters)

                gd_maql = f"SELECT {calculation_method}({expression}){gd_filter}"
                metric_dict = {
                    "id": dbt_metric.name,
                    "title": dbt_metric.label,
                    "description": dbt_metric.description,
                    "content": {
                        "format": dbt_metric.meta.gooddata.format,
                        "maql": gd_maql,
                    },
                    "tags": dbt_metric.tags,
                }
                gd_metrics.append(CatalogDeclarativeMetric.from_dict(metric_dict))
            else:
                raise Exception(f"Unsupported calculation method: {dbt_metric.calculation_method}")
        return gd_metrics
