# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional, Union

import gooddata_sdk as sdk
from gooddata_sdk import Attribute, CatalogAttribute, Metric
from gooddata_sdk.type_converter import AttributeConverterStore, Converter

from gooddata_fdw.environment import ColumnDefinition


def table_col_as_computable(col: ColumnDefinition) -> Union[Attribute, Metric]:
    item_type, item_id = col.options["id"].split("/")

    # since all cols are from the compute table, the uniqueness of local_id is ensured...
    if item_type == "label":
        return sdk.Attribute(local_id=col.column_name, label=item_id)
    else:
        aggregation = col.options.get("agg")

        return sdk.SimpleMetric(
            local_id=col.column_name,
            item=sdk.ObjId(item_id, item_type),
            aggregation=aggregation,
        )


def column_data_type_for(attribute: Optional[CatalogAttribute]) -> str:
    """
    Determine what postgres type should be used for `attribute`.

    :param attribute: catalog attribute instance
    """
    if not attribute:
        return Converter.DEFAULT_DB_DATA_TYPE

    converter = AttributeConverterStore.find_converter(attribute.dataset.dataset_type, attribute.granularity)
    return converter.db_data_type()
