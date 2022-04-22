# (C) 2021 GoodData Corporation
from __future__ import annotations

import functools
import os
from pathlib import Path
from typing import Any, Dict, NamedTuple, Union, cast

import yaml

from gooddata_metadata_client import ApiAttributeError
from gooddata_sdk.compute.model.base import ObjId

# Use typing collection types to support python < py3.9
IdObjType = Union[str, ObjId, Dict[str, Dict[str, str]], Dict[str, str]]


def id_obj_to_key(id_obj: IdObjType) -> str:
    """
    Given an object containing an id+type pair, this function will return a string key.

    For convenience, this also recognizes the `ref` format used by GoodData.UI SDK. In that format, the id+type
    are wrapped in 'identifier'.

    :param id_obj: id object
    :return: string that can be used as key
    """
    if isinstance(id_obj, str):
        return id_obj
    elif isinstance(id_obj, ObjId):
        return str(id_obj)

    try:
        unwrapped_id = id_obj["identifier"]
        if isinstance(unwrapped_id, str):
            raise ValueError(
                f'Invalid value type "{type(id_obj)}" for key "identifier" in id object. Expected dict[str, str]'
            )
        # let type checking rule out str type after accessing key "identifier"
        unwrapped = unwrapped_id
    except KeyError:
        # make sure id_obj is of type dict[str, str], eliminate dict[str, dict[str, str]]
        value_item = list(id_obj.values())[0]
        if isinstance(value_item, dict):
            raise ValueError(f'Invalid value type "{type(id_obj)}" of id object. Expected dict[str, str]')
        # Use typing collection types to support python < py3.9
        unwrapped = cast(Dict[str, str], id_obj)

    if "id" not in unwrapped or "type" not in unwrapped:
        raise KeyError(
            f"Invalid id object used to find side loaded entity: {str(id_obj)}. Need dict with 'id' and 'type' keys"
        )

    return f"{unwrapped['type']}/{unwrapped['id']}"


class AllPagedEntities(NamedTuple):
    data: list[Any]
    included: list[Any]


# Use functools.partial instead of Protocol because Protocol is available starting by py3.8
def load_all_entities(get_page_func: functools.partial[Any], page_size: int = 500) -> AllPagedEntities:
    """
    Loads all entities from a paged resource. The primary input to this function is a partial function that is setup
    with all the fixed parameters. Given this the function will get entities page-by-page and merge them into a single
    'pseudo-response' containing data and included attributes.

    An example usage:

    >>> import functools
    >>> import gooddata_metadata_client as metadata_client
    >>> import gooddata_metadata_client.apis as metadata_apis
    >>> api = metadata_apis.EntitiesApi(metadata_client.ApiClient())
    >>> get_func = functools.partial(api.get_all_entities_visualization_objects, 'some-workspace-id',
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


class SideLoads:
    def __init__(self, objs: list[Any]) -> None:
        self._objects = dict([(f"{o['type']}/{o['id']}", o) for o in objs])

    def find(self, id_obj: IdObjType) -> Union[Any, None]:
        id_obj_key = id_obj_to_key(id_obj)

        if id_obj_key not in self._objects:
            return None

        return self._objects[id_obj_key]

    def all_for_type(self, obj_type: str) -> list[Any]:
        return [o for o in self._objects.values() if o["type"] == obj_type]

    def __str__(self) -> str:
        return str(self._objects)

    def __repr__(self) -> str:
        return f"SideLoads({','.join(self._objects.keys())})"

    def __len__(self) -> int:
        return len(self._objects)


def get_sorted_yaml_files(folder: Path) -> list[Path]:
    return sorted([p for p in folder.glob("*.yaml")], key=lambda x: x.stem)


def create_directory(path: Path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def write_layout_to_file(path: Path, content: Union[dict[str, Any], list[dict]]) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        yaml.safe_dump(content, fp, indent=2)


def read_layout_from_file(path: Path) -> Any:
    if not os.path.isfile(path):
        raise ValueError(f"There is no file in the given path {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"File [{path}] has wrong yaml format. Following exception was raised during loading: {exc}")
