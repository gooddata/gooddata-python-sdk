# (C) 2022 GoodData Corporation
from __future__ import annotations

import datetime
import re
from typing import Union

from gooddata_sdk import AbsoluteDateFilter, Attribute, Filter, NegativeAttributeFilter, ObjId, PositiveAttributeFilter

from gooddata_fdw import column_utils
from gooddata_fdw.environment import ColumnDefinition, Qual
from gooddata_fdw.pg_logging import _log_debug, _log_info

# Once AbsoluteDateFilter supports empty from/to, remove this workaround
MIN_DATE = "0001-01-01"
MAX_DATE = "2999-01-01"


def _date_to_str(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")


def _is_qual_date(qual: Qual) -> bool:
    return isinstance(qual.value, datetime.date) or (
        isinstance(qual.value, list) and isinstance(qual.value[0], datetime.date)
    )


def _get_date_filter(operator: str, value: datetime.date, label: ObjId) -> Union[Filter, None]:
    date_from = MIN_DATE
    date_to = MAX_DATE
    add_filter = True
    # AbsoluteDateFilter supports only day granularity
    # date_to must equal to qual.value + 1 day, if qual.value day is to be included
    if operator == ">=":
        date_from = _date_to_str(value)
    elif operator == "<=":
        date_to = _date_to_str(value + datetime.timedelta(days=1))
    elif operator == ">":
        date_from = _date_to_str(value + datetime.timedelta(days=1))
    elif operator == "<":
        date_to = _date_to_str(value)
    elif operator == "=":
        date_from = _date_to_str(value)
        date_to = _date_to_str(value + datetime.timedelta(days=1))
    else:
        add_filter = False

    if add_filter:
        date_filter = AbsoluteDateFilter(label, date_from, date_to)
        _log_debug(f"extract_filters_from_quals: date_filter={date_filter.__dict__}")
        return date_filter
    else:
        return None


def _qual_to_date_filter(filter_entity: Attribute, qual: Qual) -> Union[Filter, None]:
    _log_debug(f"extract_filters_from_quals: filter_column={filter_entity} is date attribute")
    # Hack - Absolute date filter requires <date_dataset>.day label, but user can limit e.g. month granularity
    re_day = re.compile(r"(.*)\.[^.]+$")
    label = ObjId(re_day.sub(r"\1", filter_entity.label.id), "dataset")
    if isinstance(qual.operator, tuple):
        # Can't be implemented by multiple filters, because local GoodData instance does not support OR between filters
        _log_debug("extract_filters_from_quals: IN (date1, date2, ..) is not supported")
        return None
    else:
        return _get_date_filter(qual.operator, qual.value, label)


def _qual_to_attribute_filter(filter_entity: Attribute, qual: Qual) -> Union[Filter, None]:
    _log_debug(f"extract_filters_from_quals: filter_column={filter_entity} is normal attribute")
    if isinstance(qual.operator, tuple):
        values = qual.value
        positive = qual.operator[1]
    else:
        values = [qual.value]
        positive = qual.operator == "="
    _log_debug(f"extract_filters_from_quals: values={values} positive={positive}")

    if positive:
        return PositiveAttributeFilter(filter_entity, values)
    else:
        return NegativeAttributeFilter(filter_entity, values)


def extract_filters_from_quals(quals: list[Qual], table_columns: dict[str, ColumnDefinition]) -> list[Filter]:
    """
    Convert quals to filters.
    Now only simple attribute filters are supported.

    :param quals: multicorn quals representing filters in SQL WHERE clause
    :param table_columns: list of table columns
    :return: list of filters
    """
    filters: list[Filter] = []
    for qual in quals:
        _log_info(
            f"extract_filters_from_quals: field_name={qual.field_name} operator={qual.operator} value={qual.value}"
        )
        table_column = table_columns.get(qual.field_name)
        if not table_column:
            _log_info(
                f"extract_filters_from_quals: field_name={qual.field_name} not found in report columns, "
                f"cannot push it down"
            )
            continue

        filter_entity = column_utils.table_col_as_computable(table_column)
        new_filter = None
        if isinstance(filter_entity, Attribute):
            _log_debug(f"extract_filters_from_quals: filter_entity={filter_entity} is attribute")
            if _is_qual_date(qual):
                new_filter = _qual_to_date_filter(filter_entity, qual)
            else:
                new_filter = _qual_to_attribute_filter(filter_entity, qual)
        else:
            _log_info(
                f"extract_filters_from_quals: field_name={qual.field_name} is not attribute, but {type(filter_entity)}"
            )
        if new_filter:
            filters.append(new_filter)

    return filters
