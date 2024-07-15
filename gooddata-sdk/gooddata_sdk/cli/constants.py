# (C) 2024 GoodData Corporation
from pathlib import Path

DATA_SOURCES = "data_sources"
USER_GROUPS = "user_groups"
USERS = "users"
WORKSPACES_DATA_FILTERS = "workspaces_data_filters"
WORKSPACES = "workspaces"
WORKSPACE = "workspace"
DATA_SOURCE = "data_source"

CONFIG_FILE = "gooddata.yaml"
BASE_DIR = "analytics"

GD_ROOT = Path.home() / ".gooddata"
GD_COMMAND = GD_ROOT / "node_modules/.bin/gd"
GD_PACKAGE_JSON = GD_ROOT / "node_modules/@gooddata/code-cli/package.json"
