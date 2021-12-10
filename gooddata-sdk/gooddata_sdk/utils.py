# (C) 2021 GoodData Corporation
from __future__ import annotations

from collections import namedtuple
from datetime import date

from dateutil.parser import parse

from gooddata_metadata_client import ApiAttributeError
from gooddata_sdk.compute_model import ObjId


def id_obj_to_key(id_obj):
    """
    Given an object containing an id+type pair, this function will return a string key.

    For convenience, this also recognizes the `ref` format used by GoodData.UI SDK. In that format, the id+type
    are wrapped in 'identifier'.

    :param id_obj: id object
    :return: string that can be used as key
    """
    unwrapped = id_obj
    if isinstance(id_obj, str):
        return id_obj
    elif isinstance(id_obj, ObjId):
        return str(id_obj)
    elif "identifier" in id_obj:
        # items in insight have id object in format {identifier: { id, type }}; unwrap them for convenience
        unwrapped = id_obj["identifier"]

    if "id" not in unwrapped or "type" not in unwrapped:
        raise KeyError(
            f"Invalid id object used to find sideloaded entity: {str(id_obj)}. Need dict with 'id' and 'type' keys"
        )

    return f"{unwrapped['type']}/{unwrapped['id']}"


AllPagedEntities = namedtuple("PagedResult", ["data", "included"])


def load_all_entities(get_page_func, page_size=500):
    """
    Loads all entities from a paged resource. The primary input to this function is a partial function that is setup
    with all the fixed parameters. Given this the function will get entities page-by-page and merge them into a single
    'pseudo-response' containing data and included attributes.

    An example usage:

    >>> import functools
    >>> import gooddata_metadata_client.apis as metadata_apis
    >>> get_func = functools.partial(metadata_apis.get_all_entities_visualization_objects, 'some-workspace-id',
    >>>                              include=["ALL"], _check_return_type=False)
    >>> vis_objects = load_all_entities(get_func)

    :param get_page_func: an API controller from the metadata client
    :param page_size: optionally specify page length, default is 500
    :return:
    """
    all_paged_entities = AllPagedEntities(data=[], included=[])
    current_page = 0

    while True:
        result = get_page_func(page=current_page, size=page_size)

        all_paged_entities.data.extend(result.data)

        try:
            all_paged_entities.included.extend(result.included)
        except ApiAttributeError:
            pass

        if len(result.data) < page_size:
            break

        current_page += 1

    return all_paged_entities


def typed_value(data_type, granularity, value):
    """Return typed value based on declared data_type and granularity.

    >>> assert(typed_value("DATE", "MINUTE", '2020-01-20 00:00') == datetime(2020, 1, 20, 0, 0))
    """
    if data_type == "DATE":
        return {
            "MINUTE": _sanitize_timestamp,
            "HOUR": _sanitize_timestamp,
            "DAY": _sanitize_date,
            "WEEK": str,
            "MONTH": _sanitize_date,
            "QUARTER": str,
            "YEAR": _sanitize_date,
        }.get(granularity, int)(value)
    else:  # NORMAL
        return value


def _sanitize_date(value):
    """Add first month and first date to incomplete iso date string.

    >>> assert _sanitize_date("2021-01") == date(2021, 1 1)
    >>> assert _sanitize_date("1992") == date(1992, 1, 1)
    """
    parts = value.split("-")
    missing_count = 3 - len(parts)
    parts.extend([1 for _ in range(0, missing_count)])
    parts = map(int, parts)
    return date(*parts)


def _sanitize_timestamp(value):
    """Append minutes to incomplete datetime string.

    >>> assert _sanitize_timestamp("2021-01-01 02") == datetime(2021, 1, 1, 2, 0)
    >>> assert _sanitize_timestamp("2021-01-01 12:34") == datetime(2021, 1, 1, 12, 34)
    """
    parts = value.split(":")
    if len(parts) == 1:
        value = value + ":00"
    return parse(value)


class Sideloads:
    def __init__(self, objs):
        self._objects = dict([(f"{o['type']}/{o['id']}", o) for o in objs])

    def find(self, id_obj):
        id_obj_key = id_obj_to_key(id_obj)

        if id_obj_key not in self._objects:
            return None

        return self._objects[id_obj_key]

    def all_for_type(self, obj_type):
        return [o for o in self._objects.values() if o["type"] == obj_type]

    def __str__(self):
        return str(self._objects)

    def __repr__(self):
        return f"Sideloads({','.join(self._objects.keys())})"

    def __len__(self):
        return len(self._objects)
