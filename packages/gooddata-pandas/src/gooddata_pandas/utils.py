# (C) 2021 GoodData Corporation
from __future__ import annotations

import hashlib
import uuid
from typing import Any, Optional, Union

import pandas
from gooddata_sdk import (
    Attribute,
    CatalogAttribute,
    GoodDataSdk,
    Metric,
    ObjId,
    SimpleMetric,
    VisualizationAttribute,
    VisualizationMetric,
)
from gooddata_sdk.type_converter import AttributeConverterStore, DateConverter, DatetimeConverter, IntegerConverter
from gooddata_sdk.utils import filter_for_attributes_labels
from pandas import Index, MultiIndex

LabelItemDef = Union[Attribute, ObjId, str]
DataItemDef = Union[Attribute, Metric, ObjId, str]
IndexDef = Union[LabelItemDef, dict[str, LabelItemDef]]
ColumnsDef = dict[str, DataItemDef]

# register external pandas types to converters
IntegerConverter.set_external_fnc(lambda self, value: pandas.to_numeric(value))
DateConverter.set_external_fnc(lambda self, value: pandas.to_datetime(value))
DatetimeConverter.set_external_fnc(lambda self, value: pandas.to_datetime(value))


def get_catalog_attributes_for_extract(
    sdk: GoodDataSdk, workspace_id: str, attributes: list[Attribute], character_limit: int = 1500
) -> list[CatalogAttribute]:
    """
    Get catalog attributes for the given attributes.
    It uses the filter_for_attributes_labels function to get the
    RSQL queries for the attributes and then fetches the catalog attributes for the given workspace.
    This approach prevents loading all catalog attributes providing significant speed-up.
    """
    rsql_queries = filter_for_attributes_labels(attributes, character_limit)
    return [
        attr
        for query in rsql_queries
        for attr in sdk.catalog_workspace_content.get_attributes_catalog(
            workspace_id, include=["labels", "datasets"], rsql_filter=query
        )
    ]


def _unique_local_id() -> str:
    """
    Generate unique local ID of a DataItem without dashes.

    Returns:
        str: Unique local ID.
    """
    return uuid.uuid4().hex.replace("-", "")


def _val_to_hash(val: str) -> str:
    """
    Convert a value to its MD5 hexdigest.

    Args:
        val (str): Value to convert to a hash.

    Returns:
        str: Hexdigest of the value.
    """
    hash_object = hashlib.md5(val.encode())
    return hash_object.hexdigest()


def _str_to_obj_id(val: DataItemDef) -> Optional[ObjId]:
    """
    Convert a value to ObjId if it is in one of ["label", "metric", "fact"] types.

    Args:
        val (DataItemDef): Value to convert to ObjId.

    Returns:
        Optional[ObjId]: ObjId if the value can be converted, otherwise None.
    """
    if isinstance(val, str):
        split = val.split("/")
        _type = split[0]

        if _type in ["label", "metric", "fact"]:
            return ObjId(id="/".join(split[1:]), type=_type)
    return None


def _try_obj_id(val: DataItemDef) -> DataItemDef:
    """
    Convert a value to its ObjId if it can be converted.

    Args:
        val (DataItemDef): Value to convert to ObjId.

    Returns:
        DataItemDef: The ObjId for the given value, otherwise the value itself.
    """
    _obj_id = _str_to_obj_id(val)
    if _obj_id:
        return _obj_id
    else:
        return val


def _to_item(val: DataItemDef, local_id: Optional[str] = None) -> Union[Attribute, Metric]:
    """
    Convert a DataItemDef value to either an Attribute or a Metric based on its type.

    Args:
        val (DataItemDef): Value to convert.
        local_id (Optional[str], optional): Local ID of the input value. Defaults to None.

    Returns:
        Union[Attribute, Metric]: The resulting Attribute or Metric.
    """
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
    """
    Convert a LabelItemDef value to an Attribute.

    Args:
        val (LabelItemDef): Value to convert.
        local_id (Optional[str], optional): Local ID of the input value. Defaults to None.

    Returns:
        Attribute: The resulting Attribute.
    """
    _val = _to_item(val, local_id)
    if isinstance(_val, Attribute):
        return _val
    else:
        raise ValueError(f"Invalid attribute input: {val}")


def _typed_attribute_value(ct_attr: CatalogAttribute, value: Any) -> Any:
    """
    Convert an attribute value to its external type based on the CatalogAttribute.

    Args:
        ct_attr (CatalogAttribute): The catalog attribute.
        value (Any): The value to convert.

    Returns:
        Any: The converted value.
    """
    converter = AttributeConverterStore.find_converter(ct_attr.dataset.dataset_type, ct_attr.granularity)
    return converter.to_external_type(value)


def make_pandas_index(index: dict) -> Optional[Union[Index, MultiIndex]]:
    """
    Create a pandas index or multi-index based on the input index dictionary.

    Args:
        index (dict): The input index dictionary.

    Returns:
        Optional[Union[Index, MultiIndex]]: The resulting pandas index or multi-index, or None if empty index.
    """
    if len(index) == 1:
        index_key = list(index.keys())[0]
        _idx = pandas.Index(index[index_key], name=index_key)
    elif len(index) > 1:
        _idx = pandas.MultiIndex.from_arrays(list(index.values()), names=list(index.keys()))
    else:
        _idx = None
    return _idx


class DefaultVisualizationColumnNaming:
    def __init__(self) -> None:
        """
        Initialize a DefaultVisualizationColumnNaming instance with an empty dictionary for unique names.
        """
        self._uniques: dict[str, int] = dict()

    def _get_unique_candidate(self, candidate: str) -> str:
        """
        Find a unique candidate for a given column name.

        Args:
            candidate (str): Column name candidate.

        Returns:
            str: Unique candidate for the column name.
        """
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
        """
        Ensure a given candidate is unique in the current namespace.

        Args:
            candidate (str): Column name candidate.

        Returns:
            str: Unique column name.
        """
        unique_candidate = self._get_unique_candidate(candidate)
        self._uniques[unique_candidate] = 1
        return unique_candidate

    def col_name_for_attribute(self, attr: VisualizationAttribute) -> str:
        """
        Generate a unique column name for the given attribute.

        Args:
            attr (VisualizationAttribute): The attribute.

        Returns:
            str: The unique column name.
        """
        return self._ensure_unique(attr.label_id)

    def col_name_for_metric(self, measure: VisualizationMetric) -> str:
        """
        Generate a unique column name for the given metric.

        Args:
          measure (VisualizationMetric): The metric.

        Returns:
            str: The unique column name.
        """
        # if simple measure, use the item identifier (nice, readable)
        # otherwise try alias
        # otherwise try title
        # otherwise use local_id (arbitrary, AD created local_ids are messy)
        id_to_use = measure.item_id or measure.alias or measure.title or measure.local_id

        return self._ensure_unique(id_to_use)
