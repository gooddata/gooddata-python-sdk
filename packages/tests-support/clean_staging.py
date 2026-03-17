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
    return resp


def delete_all_entities(entity_type, entity_path):
    """List all entities of a type and delete them one by one."""
    resp = rest_op("get", f"entities/{entity_path}?size=500")
    if resp.status_code != 200:
        return
    items = resp.json().get("data", [])
    if not items:
        print(f"  No {entity_type} to remove")
        return
    for item in items:
        rest_op("delete", f"entities/{entity_path}/{item['id']}")


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

    # 6. Remove organization settings
    print("Removing organization settings...", flush=True)
    delete_all_entities("organization settings", "organizationSettings")

    # 7. Remove JWKs
    print("Removing JWKs...", flush=True)
    delete_all_entities("JWKs", "jwks")

    # 8. Remove CSP directives
    print("Removing CSP directives...", flush=True)
    delete_all_entities("CSP directives", "cspDirectives")

    # 9. Remove notification channels
    print("Removing notification channels...", flush=True)
    rest_op("put", "layout/notificationChannels", {"notificationChannels": []})

    print("=== Clean complete ===", flush=True)


if __name__ == "__main__":
    clean()
