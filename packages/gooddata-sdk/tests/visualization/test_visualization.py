# (C) 2021 GoodData Corporation
from __future__ import annotations

import json
import os

import pytest
from gooddata_sdk import Visualization
from gooddata_sdk.compute.model.execution import compute_model_to_api_model

from tests.visualization.fixtures import load_vis_obj

_current_dir = os.path.dirname(os.path.abspath(__file__))
_resources_dir = os.path.join(_current_dir, "resources")


def _visualization_filename_to_snapshot_name(absolute_path):
    return os.path.basename(absolute_path).replace(".json", ".snapshot.json")


@pytest.mark.parametrize("filename", [os.path.join(_resources_dir, d) for d in os.listdir(_resources_dir)])
def test_attribute_filters_to_api_model(filename, snapshot):
    vis_obj = load_vis_obj(filename)
    visualization = Visualization(vis_obj)

    # it is essential to define snapshot dir using absolute path, otherwise snapshots cannot be found when
    # running in tox
    snapshot.snapshot_dir = os.path.join(_current_dir, "snapshots")

    attributes = [a.as_computable() for a in visualization.attributes]
    metrics = [m.as_computable() for m in visualization.metrics]
    filters = [f.as_computable() for f in visualization.filters]

    afm = compute_model_to_api_model(attributes, metrics, filters)

    snapshot.assert_match(
        json.dumps(afm.to_dict(), indent=4, sort_keys=True),
        _visualization_filename_to_snapshot_name(filename),
    )
