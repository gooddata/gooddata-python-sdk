# (C) 2023 GoodData Corporation
import json
from pathlib import Path

from gooddata_api_client.model.declarative_workspaces import DeclarativeWorkspaces
from gooddata_sdk import GoodDataSdk

_current_dir = Path(__file__).parent.absolute()


def _refresh_workspaces(sdk: GoodDataSdk) -> None:
    layout_api = sdk.client.layout_api
    with open(_current_dir / "expected" / "declarative_workspaces.json") as f:
        layout_api.set_workspaces_layout(DeclarativeWorkspaces.from_dict(json.load(f)))
