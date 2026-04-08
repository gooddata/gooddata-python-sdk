# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import yaml
from gooddata_sdk.catalog.workspace.aac import (
    aac_dataset_to_declarative,
    aac_date_dataset_to_declarative,
    aac_metric_to_declarative,
    aac_visualization_to_declarative,
    declarative_dataset_to_aac,
    declarative_metric_to_aac,
    declarative_visualization_to_aac,
    detect_yaml_format,
    load_aac_workspace_from_disk,
    store_aac_workspace_to_disk,
)
from gooddata_sdk.config import AacConfig

_FIXTURES_DIR = Path(__file__).parent / "unit_tests" / "aac_tests"


# ---------------------------------------------------------------------------
# Config alignment tests
# ---------------------------------------------------------------------------


class TestAacConfig:
    def test_parse_vscode_config(self) -> None:
        """VSCode plugin's gooddata.yaml should be parseable by AacConfig."""
        content = yaml.safe_load((_FIXTURES_DIR / "gooddata.yaml").read_text())
        assert AacConfig.can_structure(content)
        config = AacConfig.from_dict(content)
        assert config.default_profile == "default"
        assert config.source_dir == "analytics"
        profile = config.profiles["default"]
        assert profile.host == "https://test.gooddata.com"
        assert profile.workspace_id == "test-workspace"
        assert profile.data_source == "test-datasource"

    def test_config_without_access(self) -> None:
        """Config without 'access' field (VSCode style) should parse fine."""
        content = {
            "profiles": {"dev": {"host": "https://h", "token": "t"}},
            "default_profile": "dev",
        }
        assert AacConfig.can_structure(content)
        config = AacConfig.from_dict(content)
        assert config.access is None
        assert config.ds_credentials() == {}

    def test_config_with_source_dir(self) -> None:
        content = {
            "profiles": {"dev": {"host": "https://h", "token": "t"}},
            "default_profile": "dev",
            "source_dir": "my_analytics",
        }
        config = AacConfig.from_dict(content)
        assert config.source_dir == "my_analytics"


# ---------------------------------------------------------------------------
# Individual conversion tests
# ---------------------------------------------------------------------------


class TestIndividualConversions:
    def test_metric_round_trip(self) -> None:
        aac_input = {
            "id": "revenue",
            "title": "Revenue",
            "maql": "SELECT SUM({fact/amount})",
            "format": "#,##0",
        }
        declarative = aac_metric_to_declarative(aac_input)
        assert declarative["id"] == "revenue"
        assert declarative["title"] == "Revenue"
        assert declarative["content"]["maql"] == "SELECT SUM({fact/amount})"

        result = declarative_metric_to_aac(declarative)
        assert "json" in result
        assert "content" in result
        assert result["json"]["id"] == "revenue"
        assert result["json"]["maql"] == "SELECT SUM({fact/amount})"

    def test_dataset_to_declarative(self) -> None:
        """Test forward conversion: AAC dataset → declarative."""
        aac_input = {
            "type": "dataset",
            "id": "orders",
            "table_path": "orders",
            "title": "Orders",
            "primary_key": "order_id",
            "fields": {
                "order_id": {
                    "type": "attribute",
                    "source_column": "order_id",
                    "data_type": "STRING",
                    "title": "Order ID",
                },
            },
        }
        declarative = aac_dataset_to_declarative(aac_input)
        assert declarative["id"] == "orders"
        assert declarative["title"] == "Orders"

    def test_date_dataset_conversion(self) -> None:
        aac_input = {
            "type": "date",
            "id": "order_date",
            "title": "Order Date",
        }
        declarative = aac_date_dataset_to_declarative(aac_input)
        assert declarative["id"] == "order_date"
        assert declarative["title"] == "Order Date"

    def test_visualization_to_declarative(self) -> None:
        """Test forward conversion: AAC visualization → declarative."""
        aac_input = {
            "type": "table",
            "id": "my_table",
            "title": "My Table",
            "query": {
                "fields": {
                    "m1": {
                        "title": "Sum of Amount",
                        "aggregation": "SUM",
                        "using": "fact/amount",
                    },
                },
            },
            "metrics": [{"field": "m1", "format": "#,##0"}],
        }
        declarative = aac_visualization_to_declarative(aac_input)
        assert declarative["id"] == "my_table"
        assert declarative["title"] == "My Table"

    def test_metric_from_fixture(self) -> None:
        content = yaml.safe_load((_FIXTURES_DIR / "metrics" / "top_products.yaml").read_text())
        declarative = aac_metric_to_declarative(content)
        assert declarative["id"] == "top_products"
        assert declarative["title"] == "Top Products"

    def test_dataset_from_fixture(self) -> None:
        content = yaml.safe_load((_FIXTURES_DIR / "datasets" / "orders.yaml").read_text())
        declarative = aac_dataset_to_declarative(content)
        assert declarative["id"] == "orders"

    def test_visualization_from_fixture(self) -> None:
        content = yaml.safe_load((_FIXTURES_DIR / "visualisations" / "ratings.yaml").read_text())
        declarative = aac_visualization_to_declarative(content)
        assert declarative["id"] == "71bdc379-384a-4eac-9627-364ea847d977"

    def test_metric_declarative_to_aac(self) -> None:
        """Test the full round-trip on metrics (both directions work cleanly)."""
        aac_input = {
            "id": "budget",
            "title": "Budget",
            "maql": "SELECT SUM({fact/budget})",
            "format": "#,##0.00",
            "description": "Total budget",
            "tags": ["finance"],
        }
        declarative = aac_metric_to_declarative(aac_input)
        result = declarative_metric_to_aac(declarative)
        assert result["json"]["id"] == "budget"
        assert result["json"]["maql"] == "SELECT SUM({fact/budget})"
        assert isinstance(result["content"], str)
        assert "budget" in result["content"]

    def test_dataset_declarative_to_aac(self) -> None:
        """Test declarative → AAC for datasets using a fixture-converted dataset."""
        content = yaml.safe_load((_FIXTURES_DIR / "datasets" / "orders.yaml").read_text())
        declarative = aac_dataset_to_declarative(content)
        result = declarative_dataset_to_aac(declarative)
        assert result["json"]["id"] == "orders"
        assert isinstance(result["content"], str)

    def test_visualization_declarative_to_aac(self) -> None:
        """Test declarative → AAC for visualizations (round-trip from fixture)."""
        content = yaml.safe_load((_FIXTURES_DIR / "visualisations" / "ratings.yaml").read_text())
        declarative = aac_visualization_to_declarative(content)
        result = declarative_visualization_to_aac(declarative)
        assert result["json"]["id"] == "71bdc379-384a-4eac-9627-364ea847d977"
        assert isinstance(result["content"], str)
        assert "Ratings" in result["content"]

    def test_visualization_declarative_to_aac_inline(self) -> None:
        """Test declarative → AAC for a visualization built from inline data."""
        aac_input = {
            "type": "table",
            "id": "my_table",
            "title": "My Table",
            "query": {
                "fields": {
                    "m1": {
                        "title": "Sum of Amount",
                        "aggregation": "SUM",
                        "using": "fact/amount",
                    },
                },
            },
            "metrics": [{"field": "m1", "format": "#,##0"}],
        }
        declarative = aac_visualization_to_declarative(aac_input)
        result = declarative_visualization_to_aac(declarative)
        assert result["json"]["id"] == "my_table"
        assert isinstance(result["content"], str)
        assert "my_table" in result["content"]


# ---------------------------------------------------------------------------
# Format detection tests
# ---------------------------------------------------------------------------


class TestFormatDetection:
    def test_detect_aac_with_typed_subdirs(self, tmp_path: Path) -> None:
        (tmp_path / "datasets").mkdir()
        (tmp_path / "datasets" / "orders.yaml").write_text("type: dataset\nid: orders\n")
        assert detect_yaml_format(tmp_path) == "aac"

    def test_detect_aac_with_flat_files(self, tmp_path: Path) -> None:
        (tmp_path / "orders.yaml").write_text("type: dataset\nid: orders\n")
        assert detect_yaml_format(tmp_path) == "aac"

    def test_detect_declarative_with_workspaces_dir(self, tmp_path: Path) -> None:
        (tmp_path / "workspaces").mkdir()
        assert detect_yaml_format(tmp_path) == "declarative"

    def test_detect_declarative_with_ldm_dir(self, tmp_path: Path) -> None:
        (tmp_path / "ldm").mkdir()
        assert detect_yaml_format(tmp_path) == "declarative"


# ---------------------------------------------------------------------------
# Workspace-level load/store tests
# ---------------------------------------------------------------------------


class TestWorkspaceLoadStore:
    def test_load_aac_workspace_from_fixtures(self) -> None:
        """Load fixtures excluding dashboards (WASM crypto limitation)."""
        # Use a temp dir with only datasets, metrics, visualizations
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for subdir in ("datasets", "metrics", "visualisations"):
                src = _FIXTURES_DIR / subdir
                if src.exists():
                    shutil.copytree(src, tmp_path / subdir)

            model = load_aac_workspace_from_disk(tmp_path)
            model_dict = model.to_dict(camel_case=True)

            ldm = model_dict.get("ldm", {})
            analytics = model_dict.get("analytics", {})

            # 2 datasets + 1 date dataset in fixtures
            assert len(ldm.get("datasets", [])) == 2
            assert len(ldm.get("dateInstances", [])) == 1

            # 1 metric
            assert len(analytics.get("metrics", [])) == 1

            # 2 visualizations
            assert len(analytics.get("visualizationObjects", [])) == 2

    def test_store_and_reload_metrics(self, tmp_path: Path) -> None:
        """Store metric AAC files, then reload and compare."""
        # Create a workspace model with just metrics (clean round-trip)

        aac_metrics = [
            {"id": "m1", "title": "Metric 1", "maql": "SELECT 1", "format": "#,##0"},
            {"id": "m2", "title": "Metric 2", "maql": "SELECT 2", "format": "#,##0.00"},
        ]
        metrics_declarative = [aac_metric_to_declarative(m) for m in aac_metrics]

        model_dict = {"analytics": {"metrics": metrics_declarative}}
        from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
            CatalogDeclarativeWorkspaceModel,
        )

        model = CatalogDeclarativeWorkspaceModel.from_dict(model_dict)
        store_aac_workspace_to_disk(model, tmp_path)

        # Verify files were created
        metric_files = list((tmp_path / "metrics").glob("*.yaml"))
        assert len(metric_files) == 2

        # Reload
        reloaded = load_aac_workspace_from_disk(tmp_path)
        reloaded_dict = reloaded.to_dict(camel_case=True)
        assert len(reloaded_dict.get("analytics", {}).get("metrics", [])) == 2

    def test_store_and_reload_visualizations(self, tmp_path: Path) -> None:
        """Store visualization AAC files via store_aac_workspace_to_disk, then reload."""
        aac_vis = {
            "type": "table",
            "id": "test_vis",
            "title": "Test Visualization",
            "query": {
                "fields": {
                    "m1": {
                        "title": "Sum of Amount",
                        "aggregation": "SUM",
                        "using": "fact/amount",
                    },
                },
            },
            "metrics": [{"field": "m1", "format": "#,##0"}],
        }
        vis_declarative = [aac_visualization_to_declarative(aac_vis)]

        model_dict = {"analytics": {"visualizationObjects": vis_declarative}}
        from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import (
            CatalogDeclarativeWorkspaceModel,
        )

        model = CatalogDeclarativeWorkspaceModel.from_dict(model_dict)
        store_aac_workspace_to_disk(model, tmp_path)

        # Verify files were created
        vis_files = list((tmp_path / "visualisations").glob("*.yaml"))
        assert len(vis_files) == 1

        # Reload
        reloaded = load_aac_workspace_from_disk(tmp_path)
        reloaded_dict = reloaded.to_dict(camel_case=True)
        assert len(reloaded_dict.get("analytics", {}).get("visualizationObjects", [])) == 1

    def test_store_and_reload_from_fixtures(self, tmp_path: Path) -> None:
        """Load fixtures, store to disk, reload — full round-trip."""
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            fixture_path = Path(tmp)
            for subdir in ("datasets", "metrics", "visualisations"):
                src = _FIXTURES_DIR / subdir
                if src.exists():
                    shutil.copytree(src, fixture_path / subdir)

            model = load_aac_workspace_from_disk(fixture_path)

        store_aac_workspace_to_disk(model, tmp_path)

        # Verify visualization files exist
        vis_files = list((tmp_path / "visualisations").glob("*.yaml"))
        assert len(vis_files) == 2

        # Reload and verify counts match
        reloaded = load_aac_workspace_from_disk(tmp_path)
        reloaded_dict = reloaded.to_dict(camel_case=True)
        assert len(reloaded_dict.get("analytics", {}).get("visualizationObjects", [])) == 2
        assert len(reloaded_dict.get("analytics", {}).get("metrics", [])) == 1

    def test_load_ignores_non_workspace_dirs(self, tmp_path: Path) -> None:
        """Ensure load skips declarative non-workspace directories."""
        # Create AAC file
        datasets_dir = tmp_path / "datasets"
        datasets_dir.mkdir()
        (datasets_dir / "orders.yaml").write_text(
            "type: dataset\nid: orders\ntable_path: orders\ntitle: Orders\nprimary_key: order_id\n"
            "fields:\n  order_id:\n    type: attribute\n    source_column: order_id\n    data_type: STRING\n"
        )
        # Create declarative non-workspace dir (should be ignored)
        users_dir = tmp_path / "users"
        users_dir.mkdir()
        (users_dir / "users.yaml").write_text("- id: admin\n  authenticationId: admin\n")

        model = load_aac_workspace_from_disk(tmp_path)
        model_dict = model.to_dict(camel_case=True)
        assert len(model_dict.get("ldm", {}).get("datasets", [])) == 1
