# (C) 2021 GoodData Corporation
import uuid
from typing import Union

from gooddata_sdk import (
    Attribute,
    SimpleMeasure,
    Measure,
    Filter,
    ObjId,
    InsightAttribute,
    InsightMeasure,
)

LabelItemDef = Union[Attribute, ObjId, str]
DataItemDef = Union[Attribute, Measure, ObjId, str]
IndexDef = Union[LabelItemDef, dict[str, LabelItemDef]]
ColumnsDef = dict[str, DataItemDef]


def _unique_local_id():
    return uuid.uuid4().hex.replace("-", "")


def _try_obj_id(val):
    if isinstance(val, str):
        split = val.split("/")
        _type = split[0]

        if _type in ["label", "metric", "fact"]:
            return ObjId(id="/".join(split[1:]), type=_type)

    return val


def _to_attribute(val: LabelItemDef) -> Attribute:
    _val = _try_obj_id(val)

    if isinstance(_val, Attribute):
        return _val
    elif isinstance(_val, ObjId):
        return Attribute(local_id=_unique_local_id(), label=_val)
    elif isinstance(_val, str):
        return Attribute(local_id=_unique_local_id(), label=val)

    raise ValueError(f"Invalid attribute input: {val}")


def _to_simple_metric(val: Union[SimpleMeasure, str, ObjId]) -> SimpleMeasure:
    _val = _try_obj_id(val)

    if isinstance(_val, SimpleMeasure):
        return _val
    elif isinstance(_val, ObjId):
        return SimpleMeasure(local_id=_unique_local_id(), item=_val)
    elif isinstance(_val, str):
        return SimpleMeasure(local_id=_unique_local_id(), item=ObjId(_val, "metric"))

    raise ValueError(f"Invalid metric input: {val}")


def _to_filters(val: Union[Filter, list[Filter]]) -> list[Filter]:
    if isinstance(val, Filter):
        return [val]

    return val


def _to_item(val: DataItemDef) -> Union[Attribute, Measure]:
    _val = _try_obj_id(val)

    if isinstance(_val, (Attribute, Measure)):
        return val
    elif isinstance(_val, ObjId):
        if _val.type in ["fact", "metric"]:
            return SimpleMeasure(local_id=_unique_local_id(), item=_val)
        else:
            return Attribute(local_id=_unique_local_id(), label=_val)

    raise ValueError(f"Invalid column_by item {val}")


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

    def col_name_for_measure(self, measure: InsightMeasure) -> str:
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        id_to_use = (
            measure.item_id or measure.alias or measure.title or measure.local_id
        )

        return self._ensure_unique(id_to_use)
