# (C) 2022 GoodData Corporation
import json
import os
import time
from pathlib import Path

import requests
import yaml

fixtures_dir = Path(os.environ.get("FIXTURES_DIR", Path(os.path.curdir) / "fixtures"))
staging = os.environ.get("STAGING", "").lower() in ("1", "true", "yes")

# Staging defaults — only TOKEN must be provided via env var
_STAGING_HOST = "https://python-sdk-dex.dev-latest.stg11.panther.intgdc.com"
_STAGING_HEADER_HOST = "python-sdk-dex.dev-latest.stg11.panther.intgdc.com"

if staging:
    host = os.environ.get("HOST", _STAGING_HOST)
    token = os.environ["TOKEN"]  # required — no default for staging tokens
    header_host = os.environ.get("HEADER_HOST", _STAGING_HEADER_HOST)
else:
    host = os.environ.get("HOST", "http://localhost:3000")
    token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
    header_host = os.environ.get("HEADER_HOST", None)
content_type_jsonapi = "application/vnd.gooddata.api+json"
content_type_default = "application/json"
headers = {"Host": header_host}
api_version = "v1"

# Load data source connection details from unified test config
# In Docker: mounted at /app/gd_test_config.yaml. Locally: in the SDK tests directory.
_env_name = "staging" if staging else "local"
_config_path = Path(__file__).parent / "gd_test_config.yaml"
if not _config_path.exists():
    _config_path = Path(__file__).parent.parent / "gooddata-sdk" / "tests" / "gd_test_config.yaml"
with open(_config_path, encoding="utf-8") as _f:
    _test_config = yaml.safe_load(_f)
    _ds_config = _test_config["environments"][_env_name]


def rest_op(op, url_path, data=None, raise_ex=True):
    all_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        **headers,
    }
    url = f"{host}/{url_path}"
    kwargs = {
        "url": url,
        "headers": all_headers,
    }
    if data:
        kwargs["json"] = data

    op_fnc = getattr(requests, op)
    response = op_fnc(**kwargs)

    if response.status_code < 200 or response.status_code > 299:
        if raise_ex:
            raise Exception(f"Call to {url} failed - {str(response.text)}")
        else:
            return None

    if response.status_code == 200:
        return response.json()
    else:
        return None


def read_data_from_file(data_json_path):
    with open(data_json_path) as f:
        return json.load(f)


def rest_op_jsonapi(op, url_path, data_json_path=None, raise_ex=True):
    headers["Content-Type"] = content_type_jsonapi
    return rest_op(op, url_path, data_json_path, raise_ex)


def rest_op_default(op, url_path, data_json_path=None, raise_ex=True):
    headers["Content-Type"] = content_type_default
    return rest_op(op, url_path, data_json_path, raise_ex)


def get_org_id():
    """Return the organization ID — 'default' for local Docker, auto-discovered for staging."""
    if not staging:
        return "default"
    # On staging, org ID matches the hostname prefix (e.g. python-sdk-dex)
    org_id = os.environ.get("ORG_ID", "")
    if not org_id and header_host:
        org_id = header_host.split(".")[0]
    return org_id or "default"


def wait_platform_up():
    # wait till GoodData is up and ready to receive requests
    org_id = get_org_id()
    print(f"Waiting till GoodData is up (org={org_id})", flush=True)
    while True:
        try:
            result = rest_op_jsonapi("get", f"api/{api_version}/entities/admin/organizations/{org_id}", raise_ex=False)
            if result is not None:
                print("GoodData is up", flush=True)
                break
            print("GoodData metadata is not responding", flush=True)
        except requests.exceptions.ConnectionError:
            print("GoodData is not available", flush=True)
        time.sleep(4)


def create_entity(entity_id, entity_data, entity_type, api_path, action):
    print(f"Creating {entity_type} id={entity_id}", flush=True)
    result = action("get", f"{api_path}/{entity_id}", raise_ex=False)
    if not result:
        return action("post", f"{api_path}", entity_data)
    else:
        print(f"Entity {entity_type} already exists id={entity_id} result={result}")
        return result


def patch_data_sources_for_env(data_sources):
    """Patch data source fixtures with environment-specific connection details."""
    for ds in data_sources.get("dataSources", []):
        ds["url"] = _ds_config["ds_url"]
        ds["username"] = _ds_config["ds_username"]
        ds["password"] = _ds_config["ds_password"]
        print(f"  Patched DS '{ds['id']}': url={ds['url']}, username={ds['username']}", flush=True)
    return data_sources


def update_layout():
    org_id = get_org_id()
    mode = "STAGING" if staging else "LOCAL"
    print(f"=== Running in {mode} mode (org={org_id}) ===", flush=True)

    user_groups = read_data_from_file(fixtures_dir / "user_groups.json")
    demo_user_auth = read_data_from_file(fixtures_dir / "demo_user_auth.json")
    demo_user = read_data_from_file(fixtures_dir / "demo_user.json")
    demo2_user_auth = read_data_from_file(fixtures_dir / "user_auth.json")
    demo2_user = read_data_from_file(fixtures_dir / "user.json")
    data_sources = read_data_from_file(fixtures_dir / "demo_data_sources.json")
    hierarchy = read_data_from_file(fixtures_dir / "demo_declarative_hierarchy.json")
    permissions = read_data_from_file(fixtures_dir / "workspace_permissions.json")

    # Patch data source connection details for current environment
    print(f"Patching data sources for {_env_name}...", flush=True)
    data_sources = patch_data_sources_for_env(data_sources)

    # TODO: use python-sdk support
    wait_platform_up()

    # Enable feature flags required for SDK tests (user management, scheduling, etc.)
    # IMPORTANT: Use PATCH instead of PUT to avoid overwriting the identityProvider relationship
    # PUT would overwrite the entire organization entity, removing the identity provider link
    print("Enabling feature flags on organization...", flush=True)
    org_update = {
        "data": {
            "id": org_id,
            "type": "organization",
            "attributes": {
                "earlyAccessValues": [
                    "enableUserManagement",
                    "enableScheduling",
                    "enableAlerting",
                    "enableSmtp",
                    "enableCompositeGrain",
                    "enableRawExports",
                    "enableFlexibleDashboardLayout",
                    "enablePreAggregationDatasets",
                ],
            },
        }
    }
    rest_op_jsonapi("patch", f"api/{api_version}/entities/admin/organizations/{org_id}", org_update)

    print("Uploading userGroups", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/userGroups", user_groups)

    users_to_create = [
        ("demo", demo_user_auth, demo_user),
        ("demo2", demo2_user_auth, demo2_user),
    ]
    for user_label, user_auth, user in users_to_create:
        if staging:
            # On staging with DEX, user creation may not work (DEX manages auth).
            # Try anyway but don't fail the entire upload.
            try:
                response = create_entity(
                    user_auth["email"], user_auth, "user auth", f"api/{api_version}/auth/users", rest_op_default
                )
                user["data"]["attributes"]["authenticationId"] = response["authenticationId"]
                create_entity(user["data"]["id"], user, "user", f"api/{api_version}/entities/users", rest_op_jsonapi)
            except Exception as e:
                print(f"WARNING: User '{user_label}' creation failed on staging (expected with DEX): {e}", flush=True)
        else:
            response = create_entity(
                user_auth["email"], user_auth, "user auth", f"api/{api_version}/auth/users", rest_op_default
            )
            user["data"]["attributes"]["authenticationId"] = response["authenticationId"]
            create_entity(user["data"]["id"], user, "user", f"api/{api_version}/entities/users", rest_op_jsonapi)

    print("Uploading test DS with physical model for demo", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/dataSources", data_sources)

    # Verify data sources were uploaded with permissions
    print("Verifying data source permissions...", flush=True)
    result = rest_op_default("get", f"api/{api_version}/layout/dataSources", raise_ex=False)
    if result:
        for ds in result.get("dataSources", []):
            ds_id = ds.get("id")
            perms = ds.get("permissions", [])
            print(f"  Data source '{ds_id}' has {len(perms)} permissions", flush=True)
            if ds_id == "demo-test-ds" and len(perms) == 0:
                print("  WARNING: demo-test-ds missing permissions, retrying upload...", flush=True)
                rest_op_default("put", f"api/{api_version}/layout/dataSources", data_sources)

    print("Uploading demo workspaces", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces", hierarchy)

    print("Uploading permissions for demo workspace", flush=True)
    rest_op_default("put", f"api/{api_version}/layout/workspaces/demo/permissions", permissions)

    print("Layout configuration done successfully!", flush=True)


if __name__ == "__main__":
    update_layout()
