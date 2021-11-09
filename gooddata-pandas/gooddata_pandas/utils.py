# (C) 2021 GoodData Corporation
from __future__ import annotations
import uuid
from typing import Union, Dict
import pandas
from datetime import datetime, date

from gooddata_sdk import (
    Attribute,
    SimpleMetric,
    Metric,
    Filter,
    ObjId,
    InsightAttribute,
    InsightMetric,
)
from gooddata_sdk.utils import typed_value

LabelItemDef = Union[Attribute, ObjId, str]
DataItemDef = Union[Attribute, Metric, ObjId, str]
IndexDef = Union[LabelItemDef, Dict[str, LabelItemDef]]
ColumnsDef = Dict[str, DataItemDef]


def _unique_local_id():
    return uuid.uuid4().hex.replace("-", "")


def _try_obj_id(val):
    if isinstance(val, str):
        split = val.split("/")
        _type = split[0]

        if _type in ["label", "metric", "fact"]:
            return ObjId(id="/".join(split[1:]), type=_type)

    return val


def _to_attribute(val: LabelItemDef, local_id=None) -> Attribute:
    _val = _try_obj_id(val)
    if isinstance(_val, Attribute):
        return _val
    elif isinstance(_val, ObjId):
        return Attribute(local_id=local_id or _unique_local_id(), label=_val)
    elif isinstance(_val, str):
        return Attribute(local_id=local_id or _unique_local_id(), label=val)

    raise ValueError(f"Invalid attribute input: {val}")


def _to_filters(val: Union[Filter, list[Filter]]) -> list[Filter]:
    if isinstance(val, Filter):
        return [val]

    return val


def _to_item(val: DataItemDef, local_id=None) -> Union[Attribute, Metric]:
    _val = _try_obj_id(val)

    if isinstance(_val, (Attribute, Metric)):
        return val
    elif isinstance(_val, ObjId):
        if _val.type in ["fact", "metric"]:
            return SimpleMetric(local_id=local_id or _unique_local_id(), item=_val)
        else:
            return Attribute(local_id=local_id or _unique_local_id(), label=_val)

    raise ValueError(f"Invalid column_by item {val}")


def _typed_attribute_value(ct_attr, value):
    return _to_pandas_type(
        typed_value(ct_attr.dataset.data_type, ct_attr.granularity, value)
    )


def _to_pandas_type(val):
    if isinstance(
        val,
        (
            datetime,
            date,
        ),
    ):
        r = pandas.to_datetime(val)
        return r
    elif isinstance(
        val,
        (
            int,
            float,
        ),
    ):
        return pandas.to_numeric(val)
    else:
        return val


class DefaultInsightColumnNaming:
    def __init__(self):
        self._uniques = dict()

    def _ensure_unique(self, candidate):
        # ensure column name uniqueness - in a dumb way by appending some number
        if candidate in self._uniques:
            i = 1
            new_candidate = f"{candidate}_{i}"

            while new_candidate in self._uniques:
                i += 1
                new_candidate = f"{candidate}_{i}"

            return new_candidate

        return candidate

    def col_name_for_attribute(self, attr: InsightAttribute) -> str:
        return self._ensure_unique(attr.label_id)

    def col_name_for_metric(self, measure: InsightMetric) -> str:
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        id_to_use = (
            measure.item_id or measure.alias or measure.title or measure.local_id
        )

        return self._ensure_unique(id_to_use)
