# (C) 2021 GoodData Corporation
from __future__ import annotations

import hashlib
import uuid
from typing import Any, Dict, Optional, Union

import pandas
from pandas import Index, MultiIndex

from gooddata_sdk import Attribute, CatalogAttribute, InsightAttribute, InsightMetric, Metric, ObjId, SimpleMetric
from gooddata_sdk.type_converter import AttributeConverterStore, DateConverter, DatetimeConverter, IntegerConverter

LabelItemDef = Union[Attribute, ObjId, str]
DataItemDef = Union[Attribute, Metric, ObjId, str]
IndexDef = Union[LabelItemDef, Dict[str, LabelItemDef]]
ColumnsDef = Dict[str, DataItemDef]


# register external pandas types to converters
IntegerConverter.set_external_fnc(lambda self, value: pandas.to_numeric(value))
DateConverter.set_external_fnc(lambda self, value: pandas.to_datetime(value))
DatetimeConverter.set_external_fnc(lambda self, value: pandas.to_datetime(value))


def _unique_local_id() -> str:
    return uuid.uuid4().hex.replace("-", "")


def _val_to_hash(val: str) -> str:
    hash_object = hashlib.md5(val.encode())
    return hash_object.hexdigest()


def _str_to_obj_id(val: DataItemDef) -> Optional[ObjId]:
    if isinstance(val, str):
        split = val.split("/")
        _type = split[0]

        if _type in ["label", "metric", "fact"]:
            return ObjId(id="/".join(split[1:]), type=_type)
    return None


def _try_obj_id(val: DataItemDef) -> DataItemDef:
    _obj_id = _str_to_obj_id(val)
    if _obj_id:
        return _obj_id
    else:
        return val


def _to_item(val: DataItemDef, local_id: Optional[str] = None) -> Union[Attribute, Metric]:
    _val = _try_obj_id(val)
    if isinstance(_val, (Attribute, Metric)):
        return _val
    elif isinstance(_val, ObjId):
        # local_id can contain only [.A-Za-z0-9_-]
        # We have to transform it into its hash.
        _local_id = local_id or _val_to_hash(str(val))
        if _val.type in ["fact", "metric"]:
            return SimpleMetric(local_id=_local_id, item=_val)
        else:
            return Attribute(local_id=_local_id, label=_val)

    raise ValueError(f"Invalid column_by item {val}")


def _to_attribute(val: LabelItemDef, local_id: Optional[str] = None) -> Attribute:
    _val = _to_item(val, local_id)
    if isinstance(_val, Attribute):
        return _val
    else:
        raise ValueError(f"Invalid attribute input: {val}")


def _typed_attribute_value(ct_attr: CatalogAttribute, value: Any) -> Any:
    converter = AttributeConverterStore.find_converter(ct_attr.dataset.dataset_type, ct_attr.granularity)
    return converter.to_external_type(value)


def make_pandas_index(index: dict) -> Optional[Union[Index, MultiIndex]]:
    if len(index) == 1:
        index_key = list(index.keys())[0]
        _idx = pandas.Index(index[index_key], name=index_key)
    elif len(index) > 1:
        _idx = pandas.MultiIndex.from_arrays(list(index.values()), names=list(index.keys()))
    else:
        _idx = None
    return _idx


class DefaultInsightColumnNaming:
    def __init__(self) -> None:
        self._uniques: dict[str, int] = dict()

    def _get_unique_candidate(self, candidate: str) -> str:
        # ensure column name uniqueness - in a dumb way by appending some number
        if candidate in self._uniques:
            i = 1
            new_candidate = f"{candidate}_{i}"

            while new_candidate in self._uniques:
                i += 1
                new_candidate = f"{candidate}_{i}"

            return new_candidate

        return candidate

    def _ensure_unique(self, candidate: str) -> str:
        unique_candidate = self._get_unique_candidate(candidate)
        self._uniques[unique_candidate] = 1
        return unique_candidate

    def col_name_for_attribute(self, attr: InsightAttribute) -> str:
        return self._ensure_unique(attr.label_id)

    def col_name_for_metric(self, measure: InsightMetric) -> str:
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        id_to_use = measure.item_id or measure.alias or measure.title or measure.local_id

        return self._ensure_unique(id_to_use)
