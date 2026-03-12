# (C) 2024 GoodData Corporation
"""Wipe all user-created resources from a staging environment.

Run `load-staging` afterward to restore the expected test state.
"""

import os

import requests

staging = os.environ.get("STAGING", "").lower() in ("1", "true", "yes")

_STAGING_HOST = "https://python-sdk-dex.dev-latest.stg11.panther.intgdc.com"
_STAGING_HEADER_HOST = "python-sdk-dex.dev-latest.stg11.panther.intgdc.com"

if staging:
    host = os.environ.get("HOST", _STAGING_HOST)
    token = os.environ["TOKEN"]
    header_host = os.environ.get("HEADER_HOST", _STAGING_HEADER_HOST)
else:
    host = os.environ.get("HOST", "http://localhost:3000")
    token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
    header_host = os.environ.get("HEADER_HOST", None)

api_version = "v1"


def rest_op(method, url_path, data=None):
    all_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if header_host:
        all_headers["Host"] = header_host
    url = f"{host}/api/{api_version}/{url_path}"
    resp = getattr(requests, method)(url=url, headers=all_headers, json=data)
    if resp.status_code >= 300:
        print(f"  WARNING: {method.upper()} {url_path} returned {resp.status_code}: {resp.text[:200]}")
    else:
        print(f"  OK: {method.upper()} {url_path}")


def clean():
    mode = "STAGING" if staging else "LOCAL"
    print(f"=== Cleaning environment ({mode}) ===", flush=True)

    # Order matters: permissions reference users/groups, workspaces reference data sources.
    # 1. Remove workspace permissions first
    print("Removing workspace permissions...", flush=True)
    rest_op("put", "layout/workspaces/demo/permissions", {"hierarchyPermissions": [], "permissions": []})

    # 2. Remove workspaces (removes all workspace content)
    print("Removing workspaces...", flush=True)
    rest_op("put", "layout/workspaces", {"workspaces": [], "workspaceDataFilters": []})

    # 3. Remove data sources
    print("Removing data sources...", flush=True)
    rest_op("put", "layout/dataSources", {"dataSources": []})

    # 4. Remove non-admin users (keep admin)
    print("Removing users (keeping admin)...", flush=True)
    rest_op(
        "put", "layout/users", {"users": [{"id": "admin", "userGroups": [{"id": "adminGroup", "type": "userGroup"}]}]}
    )

    # 5. Remove non-admin user groups (keep adminGroup)
    print("Removing user groups (keeping adminGroup)...", flush=True)
    rest_op("put", "layout/userGroups", {"userGroups": [{"id": "adminGroup"}]})

    print("=== Clean complete ===", flush=True)


if __name__ == "__main__":
    clean()
