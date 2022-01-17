# (C) 2022 GoodData Corporation
import json
import os
import time
from pathlib import Path

import requests


def rest_op(op, host, token, headers, url_path, data_json_path=None, raise_ex=True):
    all_headers = {
        **{
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        **headers,
    }
    url = f"{host}/{url_path}"
    kwargs = {
        "url": url,
        "headers": all_headers,
    }
    if data_json_path:
        with open(data_json_path, "rt") as f:
            data = json.load(f)
        kwargs["json"] = data

    op_fnc = getattr(requests, op)
    response = op_fnc(**kwargs)

    if response.status_code < 200 or response.status_code > 299:
        if raise_ex:
            raise Exception(f"Upload of {str(data_json_path)} to {url} failed - {str(response)}")
        else:
            return None

    return response


def update_layout():
    fixtures_dir = Path(os.environ.get("FIXTURES_DIR"))
    host = os.environ.get("HOST", "http://localhost:3000")
    token = os.environ.get("TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")
    header_host = os.environ.get("HEADER_HOST", None)

    ds = fixtures_dir / "demo_ds.json"
    pdm = fixtures_dir / "demo_declarative_pdm.json"
    hierarchy = fixtures_dir / "demo_declarative_hierarchy.json"

    # TODO: use python-sdk support
    headers = {"Content-Type": "application/vnd.gooddata.api+json"}
    if header_host:
        headers["Host"] = header_host

    # wait till GD.CN is up and ready to receive requests
    print("Waiting till AIO GD.CN is up", flush=True)
    while True:
        try:
            result = rest_op("get", host, token, headers, "api/entities/admin/organizations/default", raise_ex=False)
            if result is not None:
                print("AIO GD.CN is up", flush=True)
                break
            print("AIO GD.CN metadata does not responding", flush=True)
        except requests.exceptions.ConnectionError:
            print("AIO GD.CN is not available", flush=True)
        time.sleep(4)

    print("Creating test DS for demo", flush=True)
    if not rest_op("get", host, token, headers, "api/entities/dataSources/demo-test-ds", raise_ex=False):
        rest_op("post", host, token, headers, "api/entities/dataSources", ds)

    headers["Content-Type"] = "application/json"

    print("Uploading test DS physical model for demo", flush=True)
    rest_op("put", host, token, headers, "api/layout/dataSources/demo-test-ds/physicalModel", pdm)

    print("Uploading demo workspaces", flush=True)
    rest_op("put", host, token, headers, "api/layout/workspaces", hierarchy)

    print("Layout configuration done successfully!", flush=True)


if __name__ == "__main__":
    update_layout()
