# (C) 2026 GoodData Corporation
"""``gdc validate``.

Exit codes are the contract here: a pipeline needs to tell "your content is broken" from
"you pointed me at the wrong thing", and both from success.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pytest
from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.service import WorkspaceValidationReport
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel
from gooddata_sdk.cli import validate as validate_module
from gooddata_sdk.cli.validate import validate


def _content(**overrides: Any) -> dict[str, Any]:
    content: dict[str, Any] = {
        "version": "2",
        "visualizationUrl": "local:column",
        "buckets": [
            {
                "localIdentifier": "measures",
                "items": [
                    {
                        "measure": {
                            "localIdentifier": "m1",
                            "definition": {
                                "measureDefinition": {"item": {"identifier": {"id": "rev", "type": "metric"}}}
                            },
                        }
                    }
                ],
            }
        ],
        "filters": [],
        "sorts": [],
    }
    content.update(overrides)
    return content


def _layout(tmp_path: Path, *contents: dict[str, Any]) -> Path:
    model = CatalogDeclarativeAnalytics.from_dict(
        {
            "analytics": {
                "visualizationObjects": [
                    {"id": f"v{i}", "title": f"v{i}", "content": c} for i, c in enumerate(contents)
                ]
            }
        },
        camel_case=True,
    )
    model.store_to_disk(tmp_path)
    return tmp_path


def _args(**kwargs: Any) -> argparse.Namespace:
    kwargs.setdefault("workspace", None)
    kwargs.setdefault("json", False)
    kwargs.setdefault("plan", False)
    kwargs.setdefault("check_filter_values", False)
    return argparse.Namespace(**kwargs)


class TestOfflineMode:
    def test_a_clean_layout_exits_zero(self, tmp_path):
        assert validate(_layout(tmp_path, _content()), _args()) == 0

    def test_a_broken_layout_exits_one(self, tmp_path):
        broken = _content()
        del broken["version"]
        assert validate(_layout(tmp_path, _content(), broken), _args()) == 1

    def test_warnings_alone_still_exit_zero(self, tmp_path):
        """An unknown chart type must not fail a build: it usually means the SDK is older
        than the platform, not that the content is wrong."""
        assert validate(_layout(tmp_path, _content(version="3")), _args()) == 0

    def test_no_credentials_are_needed(self, tmp_path, monkeypatch):
        """The point of the offline mode is that it runs on a pull request."""
        monkeypatch.delenv("GOODDATA_HOST", raising=False)
        monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
        assert validate(_layout(tmp_path, _content()), _args()) == 0

    def test_it_says_what_it_did_not_check(self, tmp_path, capsys):
        validate(_layout(tmp_path, _content()), _args())
        assert "Pass --workspace" in capsys.readouterr().out


class TestOfflineCatalogResolution:
    """A layout carrying its logical model can answer whether the objects it names exist,
    with no server -- which is what lets the full check run on a pull request."""

    @staticmethod
    def _layout_with_ldm(tmp_path: Path, *, metric_maql: str) -> Path:
        CatalogDeclarativeAnalytics.from_dict(
            {"analytics": {"metrics": [{"id": "m", "title": "m", "content": {"maql": metric_maql}}]}},
            camel_case=True,
        ).store_to_disk(tmp_path)
        CatalogDeclarativeModel.from_dict(
            {
                "ldm": {
                    "datasets": [
                        {
                            "id": "sales",
                            "title": "sales",
                            "grain": [],
                            "references": [],
                            "attributes": [{"id": "region", "title": "region", "labels": []}],
                            "facts": [{"id": "amount", "title": "amount"}],
                        }
                    ],
                    "dateInstances": [],
                }
            },
            camel_case=True,
        ).store_to_disk(tmp_path)
        return tmp_path

    def test_a_reference_the_logical_model_declares_resolves(self, tmp_path, capsys):
        path = self._layout_with_ldm(tmp_path, metric_maql="SELECT SUM({fact/amount})")
        assert validate(path, _args()) == 0
        assert "against the layout's own logical model" in capsys.readouterr().out

    def test_a_reference_nothing_declares_is_reported_without_a_server(self, tmp_path, capsys):
        path = self._layout_with_ldm(tmp_path, metric_maql="SELECT SUM({fact/ghost})")
        assert validate(path, _args()) == 1
        out = capsys.readouterr().out
        assert "fact/ghost" in out
        assert "this layout's logical model" in out

    def test_an_implicit_label_resolves(self, tmp_path):
        """`region` declares no labels, so `label/region` exists only by the implicit rule."""
        path = self._layout_with_ldm(tmp_path, metric_maql="SELECT COUNT({label/region})")
        assert validate(path, _args()) == 0

    def test_a_layout_without_a_logical_model_says_what_it_could_not_check(self, tmp_path, capsys):
        assert validate(_layout(tmp_path, _content()), _args()) == 0
        assert "carries no logical model" in capsys.readouterr().out


class TestPathGuards:
    """``load_from_disk`` creates the layout's folders as it walks, so an unguarded run on
    the wrong path writes directories, finds nothing in them and reports success -- the one
    failure mode a validator must not have, because it is indistinguishable from passing."""

    def test_a_path_that_does_not_exist_is_a_usage_error(self, tmp_path, capsys):
        assert validate(tmp_path / "nope", _args()) == 2
        assert "does not exist" in capsys.readouterr().out

    def test_a_directory_that_is_not_a_layout_is_a_usage_error(self, tmp_path, capsys):
        assert validate(tmp_path, _args()) == 2
        assert "not a layout directory" in capsys.readouterr().out

    def test_nothing_is_written_when_the_path_is_rejected(self, tmp_path):
        validate(tmp_path, _args())
        assert list(tmp_path.iterdir()) == []

    def test_a_layout_with_no_visualizations_says_so_instead_of_reporting_success(self, tmp_path, capsys):
        (tmp_path / "analytics_model").mkdir()
        assert validate(tmp_path, _args()) == 0
        assert "Nothing to validate" in capsys.readouterr().out

    def test_the_object_count_is_reported(self, tmp_path, capsys):
        validate(_layout(tmp_path, _content(), _content()), _args())
        assert "2 object(s) checked." in capsys.readouterr().out


class TestJsonOutput:
    """Exit codes say whether a run passed; they cannot say what failed. Anything that
    annotates a pull request or counts findings by code needs the findings themselves, and
    parsing the human output would make its wording an API."""

    def test_a_clean_run_emits_parsable_json(self, tmp_path, capsys):
        assert validate(_layout(tmp_path, _content()), _args(json=True)) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is True
        assert payload["findings"] == []
        assert payload["objectsChecked"] == 1
        assert payload["workspace"] is None

    def test_findings_carry_their_code_and_location(self, tmp_path, capsys):
        broken = _content()
        del broken["version"]
        assert validate(_layout(tmp_path, broken), _args(json=True)) == 1
        finding = json.loads(capsys.readouterr().out)["findings"][0]
        assert finding["code"] == "missing_required_key"
        assert finding["severity"] == "error"
        assert finding["location"] == "content.version"

    def test_nothing_but_json_is_printed(self, tmp_path, capsys):
        """It goes through a pipe: the advisory line and the colour codes would break it."""
        validate(_layout(tmp_path, _content()), _args(json=True))
        out = capsys.readouterr().out
        json.loads(out)
        assert "Pass --workspace" not in out
        assert "\033[" not in out

    def test_an_empty_layout_still_emits_json(self, tmp_path, capsys):
        (tmp_path / "analytics_model").mkdir()
        assert validate(tmp_path, _args(json=True)) == 0
        assert json.loads(capsys.readouterr().out)["objectsChecked"] == 0


class TestSingleFile:
    def test_one_visualization_file_can_be_validated_on_its_own(self, tmp_path):
        layout = _layout(tmp_path, _content())
        one = next(layout.rglob("visualization_objects/*.yaml"))
        assert validate(one, _args()) == 0

    def test_a_broken_single_file_exits_one(self, tmp_path):
        broken = _content()
        del broken["buckets"]
        layout = _layout(tmp_path, broken)
        one = next(layout.rglob("visualization_objects/*.yaml"))
        assert validate(one, _args()) == 1

    def test_a_file_that_is_not_a_visualization_is_a_usage_error(self, tmp_path, capsys):
        """Every object kind is stored in the same shape, so a metric loads as a
        visualization and then reports all of its structure as missing. Exit 2 rather than
        1 keeps "you pointed at the wrong file" distinguishable from "the content is bad"."""
        metrics_dir = tmp_path / "analytics_model" / "metrics"
        metrics_dir.mkdir(parents=True)
        (metrics_dir / "m.yaml").write_text("id: m\ntitle: m\ncontent:\n  maql: SELECT 1\n")
        assert validate(metrics_dir / "m.yaml", _args()) == 2
        assert "not a visualization object" in capsys.readouterr().out


class TestWorkspaceMode:
    def test_without_any_way_to_connect_it_is_a_usage_error(self, tmp_path, monkeypatch, capsys):
        monkeypatch.delenv("GOODDATA_HOST", raising=False)
        monkeypatch.delenv("GOODDATA_TOKEN", raising=False)
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "no-home")
        assert validate(_layout(tmp_path, _content()), _args(workspace="ws")) == 2
        assert "Drop --workspace" in capsys.readouterr().out

    def test_environment_variables_are_enough_to_connect(self, tmp_path, monkeypatch):
        """A layout checked out on its own has no gooddata.yaml beside it, which is exactly
        the CI case."""
        monkeypatch.setenv("GOODDATA_HOST", "https://example.gooddata.com")
        monkeypatch.setenv("GOODDATA_TOKEN", "token")
        created: list[tuple[str, str]] = []

        class _Sdk:
            @staticmethod
            def create(host: str, token: str) -> str:
                created.append((host, token))
                return "sdk"

        monkeypatch.setattr(validate_module, "GoodDataSdk", _Sdk)
        monkeypatch.setattr(
            validate_module,
            "ValidationService",
            lambda sdk: pytest.fail("should not be reached") if sdk != "sdk" else _StubService(),
        )
        assert validate(_layout(tmp_path, _content()), _args(workspace="ws")) == 0
        assert created == [("https://example.gooddata.com", "token")]


class _StubService:
    def validate_analytics_model(self, workspace_id: str, model: Any, **kwargs: Any) -> WorkspaceValidationReport:
        return WorkspaceValidationReport(objects_checked=1)


class TestFilterValueCheckIsOptIn:
    """It queries the data source rather than the metadata, so it has to be asked for and
    it has to have somewhere to ask."""

    def test_asking_for_it_without_a_workspace_is_a_usage_error(self, tmp_path):
        """Not silently ignored: that would report a clean run for a check that never ran."""
        layout = _layout(tmp_path)
        assert validate(layout, _args(check_filter_values=True)) == 2

    def test_the_refusal_says_what_to_do_about_it(self, tmp_path, capsys):
        validate(_layout(tmp_path), _args(check_filter_values=True))
        assert "--check-filter-values needs --workspace" in capsys.readouterr().out

    def test_a_plain_offline_run_is_unaffected(self, tmp_path):
        assert validate(_layout(tmp_path), _args()) == 0
