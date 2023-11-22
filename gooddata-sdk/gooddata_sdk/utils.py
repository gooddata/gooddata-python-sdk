# (C) 2021 GoodData Corporation
from __future__ import annotations

import functools
import os
import re
from collections.abc import KeysView
from pathlib import Path
from shutil import rmtree
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, Union, cast, no_type_check

import yaml

from gooddata_api_client import ApiAttributeError
from gooddata_api_client.model_utils import OpenApiModel
from gooddata_sdk.compute.model.base import ObjId

# Use typing collection types to support python < py3.9
IdObjType = Union[str, ObjId, Dict[str, Dict[str, str]], Dict[str, str]]

PROFILES_FILE = "profiles.yaml"
PROFILES_DIRECTORY = ".gooddata"
PROFILES_FILE_PATH = Path.home() / PROFILES_DIRECTORY / PROFILES_FILE
SDK_PROFILE_MANDATORY_KEYS = ["host", "token"]
SDK_PROFILE_KEYS = SDK_PROFILE_MANDATORY_KEYS + ["custom_headers", "extra_user_agent"]


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
    >>> import gooddata_api_client as api_client
    >>> import gooddata_api_client.apis as apis
    >>> api = apis.EntitiesApi(api_client.ApiClient())
    >>> get_func = functools.partial(api.get_all_entities_visualization_objects, 'some-workspace-id',
    >>>                              include=["ALL"], _check_return_type=False)
    >>> vis_objects = load_all_entities(get_func)

    :param get_page_func: an API controller from the metadata client
    :param page_size: optionally specify page length, default is 500
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


def load_all_entities_dict(
    get_page_func: functools.partial[Any], page_size: int = 500, camel_case: bool = False
) -> dict[str, Any]:
    all_entities = load_all_entities(get_page_func, page_size)
    all_entities_dict = {"data": all_entities.data, "included": all_entities.included}
    return all_entities_dict if camel_case else change_case(all_entities_dict, camel_to_snake)


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


def recreate_directory(path: Path) -> None:
    if os.path.exists(path):
        rmtree(path)
    os.makedirs(path)


class IndentDumper(yaml.SafeDumper):
    @no_type_check
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super(IndentDumper, self).increase_indent(flow, False)


def write_layout_to_file(path: Path, content: Union[dict[str, Any], list[dict]]) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        yaml.dump(content, fp, indent=2, Dumper=IndentDumper, allow_unicode=True)


def read_layout_from_file(path: Path) -> Any:
    if not os.path.isfile(path):
        raise ValueError(f"There is no file in the given path {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ValueError(f"File [{path}] has wrong yaml format. Following exception was raised during loading: {exc}")


def camel_to_snake(camel_case_str: str) -> str:
    return re.sub(r"([A-Z]+)", r"_\1", camel_case_str).lower()


def snake_to_camel(snake_case_str: str) -> str:
    components = snake_case_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def change_case_helper(value: Union[list, dict, str], case: Callable[[str], str]) -> Union[list, dict, str]:
    if isinstance(value, list):
        return [change_case_helper(v, case) for v in value]
    elif isinstance(value, dict):
        return change_case(value, case)
    else:
        return value


def change_case(dictionary: dict, case: Callable[[str], str]) -> dict:
    temp = dict()
    for k, v in dictionary.items():
        temp[case(k)] = change_case_helper(v, case)
    return temp


def mandatory_profile_content_check(profile: str, profile_content_keys: KeysView) -> None:
    """Check, whether the mandatory profile content is valid.

    Args:
        profile (str):
            Profile name
        profile_content_keys (KeysView):
            Dictionary keys from loaded configuration file under specific profile.

    Retruns:
        None

    Raises:
        ValueError:
            Missing mandatory parameter or parameters.
    """
    missing = []
    for mandatory_parameter in SDK_PROFILE_MANDATORY_KEYS:
        if mandatory_parameter not in profile_content_keys:
            missing.append(mandatory_parameter)
    if missing:
        missing_str = " and ".join(missing)
        raise ValueError(f"Profile {profile} is missing mandatory parameter or parameters {missing_str}.")


def profile_content(profile: str = "default", profiles_path: Path = PROFILES_FILE_PATH) -> dict[str, Any]:
    """Get the profile content from a given file.

    Args:
        profile (str, optional):
            Profile name. Defaults to "default".
        profiles_path (Path, optional):
            File path for the profiles. Defaults to PROFILES_FILE_PATH.

    Raises:
        ValueError:
            There is no profile file located for the given path.
        ValueError:
            Profile file does not contain the specified profile.

    Returns:
        dict[str, Any]:
            Profile content as a dictionary.
    """
    if not profiles_path.exists():
        raise ValueError(f"There is no profiles file located for path {profiles_path}.")
    content = read_layout_from_file(profiles_path)
    if not content.get(profile):
        raise ValueError(f"Profiles file does not contain profile {profile}.")
    mandatory_profile_content_check(profile, content[profile].keys())
    return {key: content[profile][key] for key in content[profile] if key in SDK_PROFILE_KEYS}


def good_pandas_profile_content(
    profile: str = "default", profiles_path: Path = PROFILES_FILE_PATH
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Load the profiles for GoodPandas

    This is workaround for GoodPandas. We should only use profile_content in the future.
    For that we need to unify GoodPandas and GoodDataSdk interface.

    Args:
        profile (str, optional):
            Profile name. Defaults to "default".
        profiles_path (Path, optional):
            File path for the profiles. Defaults to PROFILES_FILE_PATH.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]:
            The content and custom Headers.
    """
    content = profile_content(profile, profiles_path)
    custom_headers = content.pop("custom_headers", {})
    content.pop("extra_user_agent", None)
    return content, custom_headers


def safeget(var: Any, path: List[str]) -> Any:
    if len(path) == 0:
        # base case: we have reached the innermost key
        return var
    elif not isinstance(var, (dict, OpenApiModel)):
        # base case: var is not a dictionary, so we can't proceed
        # in this repository, we also use OpenApiModel objects, which support "to_dict"
        return None
    else:
        # recursive case: we still have keys to traverse
        key = path[0]
        if key in var:
            return safeget(var[key], path[1:])
        else:
            return None


def safeget_list(var: Any, path: List[str]) -> List[Any]:
    result = safeget(var, path)
    if isinstance(result, list):
        return result
    elif result is None:
        return []
    else:
        raise Exception("safeget_list: result is not iterable! result={0}".format(result))
