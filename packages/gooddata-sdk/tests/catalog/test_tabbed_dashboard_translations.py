# (C) 2024 GoodData Corporation
"""Unit tests for tabbed dashboard layout support in translation methods.

Dashboards can have sections in two places:
  - content["layout"]["sections"]        (legacy flat layout)
  - content["tabs"][*]["layout"]["sections"]  (tabbed layout)

Some dashboards use only tabs (no top-level layout), some use only the
legacy layout (no tabs), and some have both.  These tests verify that
get_texts_to_translate and set_translated_texts handle all three cases.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gooddata_sdk.catalog.workspace.service import CatalogWorkspaceService

# ---------------------------------------------------------------------------
# Helpers to build minimal dashboard / workspace content fixtures
# ---------------------------------------------------------------------------


def _make_widget(title: str | None = None, description: str | None = None, widget_type: str = "insight"):
    w = {"type": widget_type, "localIdentifier": "loc1"}
    if title is not None:
        w["title"] = title
    if description is not None:
        w["description"] = description
    return w


def _make_section(widgets: list[dict], header: dict | None = None):
    section = {"items": [{"widget": w} for w in widgets]}
    if header is not None:
        section["header"] = header
    return section


def _make_dashboard(content: dict, dashboard_id: str = "dash1", title: str = "Dashboard", description: str = ""):
    d = MagicMock()
    d.id = dashboard_id
    d.title = title
    d.description = description
    d.content = content
    return d


def _make_workspace_content(dashboards: list | None = None, metrics: list | None = None):
    wc = MagicMock()
    wc.ldm = None
    analytics = MagicMock()
    analytics.metrics = metrics or []
    analytics.visualization_objects = []
    analytics.analytical_dashboards = dashboards or []
    analytics.filter_contexts = []
    wc.analytics = analytics
    return wc


def _make_workspace(name: str = "Test Workspace"):
    w = MagicMock()
    w.name = name
    return w


# ---------------------------------------------------------------------------
# _iter_dashboard_sections
# ---------------------------------------------------------------------------


class TestIterDashboardSections:
    """Test the _iter_dashboard_sections static method."""

    def test_legacy_layout_only(self):
        """Dashboards with only content.layout.sections."""
        content = {
            "layout": {
                "sections": [
                    _make_section([_make_widget("W1")]),
                    _make_section([_make_widget("W2")]),
                ],
            },
        }
        sections = list(CatalogWorkspaceService._iter_dashboard_sections(content))
        assert len(sections) == 2

    def test_tabs_only(self):
        """Dashboards with only content.tabs (no top-level layout)."""
        content = {
            "tabs": [
                {
                    "title": "Tab A",
                    "layout": {
                        "sections": [_make_section([_make_widget("T1")])],
                    },
                },
                {
                    "title": "Tab B",
                    "layout": {
                        "sections": [
                            _make_section([_make_widget("T2")]),
                            _make_section([_make_widget("T3")]),
                        ],
                    },
                },
            ],
        }
        sections = list(CatalogWorkspaceService._iter_dashboard_sections(content))
        assert len(sections) == 3

    def test_both_layout_and_tabs(self):
        """Dashboards with both top-level layout and tabs."""
        content = {
            "layout": {
                "sections": [_make_section([_make_widget("L1")])],
            },
            "tabs": [
                {
                    "title": "Tab",
                    "layout": {
                        "sections": [_make_section([_make_widget("T1")])],
                    },
                },
            ],
        }
        sections = list(CatalogWorkspaceService._iter_dashboard_sections(content))
        assert len(sections) == 2

    def test_empty_content(self):
        """Dashboard with no layout and no tabs yields nothing."""
        sections = list(CatalogWorkspaceService._iter_dashboard_sections({}))
        assert sections == []

    def test_tabs_without_layout_key(self):
        """Tabs that are missing a layout key are skipped gracefully."""
        content = {
            "tabs": [
                {"title": "Empty tab"},  # no layout key
                {
                    "title": "Good tab",
                    "layout": {"sections": [_make_section([_make_widget("W")])]},
                },
            ],
        }
        sections = list(CatalogWorkspaceService._iter_dashboard_sections(content))
        assert len(sections) == 1


# ---------------------------------------------------------------------------
# get_texts_to_translate — tabbed dashboard handling
# ---------------------------------------------------------------------------


class TestGetTextsToTranslateTabbed:
    """Test that get_texts_to_translate extracts texts from tabbed dashboards."""

    def _service(self):
        svc = CatalogWorkspaceService.__new__(CatalogWorkspaceService)
        return svc

    def test_tabs_only_dashboard(self):
        """Texts are extracted from a dashboard that only has tabs (no layout)."""
        dashboard = _make_dashboard(
            content={
                "tabs": [
                    {
                        "title": "Clearing",
                        "layout": {
                            "sections": [
                                _make_section(
                                    [_make_widget("Widget A", "Desc A")],
                                    header={"title": "Section Header"},
                                ),
                            ],
                        },
                        "dateFilterConfig": {"filterName": "Tab Date Filter"},
                    },
                ],
            },
            title="My Dashboard",
        )
        workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        svc = self._service()
        texts = svc.get_texts_to_translate(workspace, workspace_content, {})

        assert "WS" in texts
        assert "My Dashboard" in texts
        assert "Widget A" in texts
        assert "Desc A" in texts
        assert "Section Header" in texts
        assert "Clearing" in texts  # tab title
        assert "Tab Date Filter" in texts  # date filter inside tab

    def test_legacy_layout_dashboard(self):
        """Texts are still extracted from legacy layout dashboards."""
        dashboard = _make_dashboard(
            content={
                "layout": {
                    "sections": [
                        _make_section([_make_widget("Legacy Widget")]),
                    ],
                },
                "dateFilterConfig": {"filterName": "Top Date Filter"},
            },
            title="Legacy Dashboard",
        )
        workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        svc = self._service()
        texts = svc.get_texts_to_translate(workspace, workspace_content, {})

        assert "Legacy Widget" in texts
        assert "Top Date Filter" in texts

    def test_rich_text_in_tabs(self):
        """Rich text widget content is extracted from tabbed layouts."""
        rich_widget = _make_widget(widget_type="richText")
        rich_widget["content"] = "# Hello World"

        dashboard = _make_dashboard(
            content={
                "tabs": [
                    {
                        "title": "Tab",
                        "layout": {
                            "sections": [_make_section([rich_widget])],
                        },
                    },
                ],
            },
        )
        workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        svc = self._service()
        texts = svc.get_texts_to_translate(workspace, workspace_content, {})

        assert "# Hello World" in texts

    def test_visualization_switcher_in_tabs(self):
        """Visualization switcher titles are extracted from tabbed layouts."""
        vs_widget = _make_widget(widget_type="visualizationSwitcher")
        vs_widget["visualizations"] = [
            {"title": "Viz 1", "description": "Viz 1 desc"},
            {"title": "Viz 2"},
        ]

        dashboard = _make_dashboard(
            content={
                "tabs": [
                    {
                        "title": "Tab",
                        "layout": {
                            "sections": [_make_section([vs_widget])],
                        },
                    },
                ],
            },
        )
        workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        svc = self._service()
        texts = svc.get_texts_to_translate(workspace, workspace_content, {})

        assert "Viz 1" in texts
        assert "Viz 1 desc" in texts
        assert "Viz 2" in texts

    def test_already_translated_excluded(self):
        """Already-translated texts are excluded from the result."""
        dashboard = _make_dashboard(
            content={
                "tabs": [
                    {
                        "title": "Tab",
                        "layout": {
                            "sections": [_make_section([_make_widget("Keep Me"), _make_widget("Skip Me")])],
                        },
                    },
                ],
            },
        )
        workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        svc = self._service()
        texts = svc.get_texts_to_translate(workspace, workspace_content, {"Skip Me": "translated"})

        assert "Keep Me" in texts
        assert "Skip Me" not in texts


# ---------------------------------------------------------------------------
# set_translated_texts — tabbed dashboard handling
# ---------------------------------------------------------------------------


class TestSetTranslatedTextsTabbed:
    """Test that set_translated_texts applies translations in tabbed dashboards."""

    def _service(self):
        svc = CatalogWorkspaceService.__new__(CatalogWorkspaceService)
        return svc

    def test_translates_tab_titles(self):
        """Tab titles are translated."""
        import copy

        content = {
            "tabs": [
                {
                    "title": "Clearing",
                    "layout": {
                        "sections": [_make_section([_make_widget("W1")])],
                    },
                },
                {
                    "title": "Authorization",
                    "layout": {
                        "sections": [_make_section([_make_widget("W2")])],
                    },
                },
            ],
        }
        dashboard = _make_dashboard(content=copy.deepcopy(content), title="Dash")
        workspace = _make_workspace("WS")
        new_workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        translated = {
            "WS": "WS_cs",
            "Dash": "Přehled",
            "Clearing": "Zúčtování",
            "Authorization": "Autorizace",
            "W1": "W1_cs",
            "W2": "W2_cs",
        }

        svc = self._service()
        svc.set_translated_texts(workspace, new_workspace, workspace_content, "cs", translated)

        assert dashboard.content["tabs"][0]["title"] == "Zúčtování"
        assert dashboard.content["tabs"][1]["title"] == "Autorizace"

    def test_translates_widgets_in_tabs(self):
        """Widget titles/descriptions inside tabs are translated."""
        import copy

        content = {
            "tabs": [
                {
                    "title": "Tab",
                    "layout": {
                        "sections": [
                            _make_section(
                                [_make_widget("Original Title", "Original Desc")],
                                header={"title": "Header Title", "description": "Header Desc"},
                            ),
                        ],
                    },
                },
            ],
        }
        dashboard = _make_dashboard(content=copy.deepcopy(content), title="Dash")
        workspace = _make_workspace("WS")
        new_workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        translated = {
            "WS": "WS_cs",
            "Dash": "Přehled",
            "Tab": "Záložka",
            "Original Title": "Přeložený Název",
            "Original Desc": "Přeložený Popis",
            "Header Title": "Hlavička",
            "Header Desc": "Popis Hlavičky",
        }

        svc = self._service()
        svc.set_translated_texts(workspace, new_workspace, workspace_content, "cs", translated)

        section = dashboard.content["tabs"][0]["layout"]["sections"][0]
        assert section["items"][0]["widget"]["title"] == "Přeložený Název"
        assert section["items"][0]["widget"]["description"] == "Přeložený Popis"
        assert section["header"]["title"] == "Hlavička"
        assert section["header"]["description"] == "Popis Hlavičky"

    def test_legacy_layout_still_works(self):
        """Legacy layout dashboards still get their widgets translated."""
        import copy

        content = {
            "layout": {
                "sections": [_make_section([_make_widget("Widget", "Desc")])],
            },
        }
        dashboard = _make_dashboard(content=copy.deepcopy(content), title="Dash")
        workspace = _make_workspace("WS")
        new_workspace = _make_workspace("WS")
        workspace_content = _make_workspace_content(dashboards=[dashboard])

        translated = {
            "WS": "WS_cs",
            "Dash": "Přehled",
            "Widget": "Widget_cs",
            "Desc": "Desc_cs",
        }

        svc = self._service()
        svc.set_translated_texts(workspace, new_workspace, workspace_content, "cs", translated)

        section = dashboard.content["layout"]["sections"][0]
        assert section["items"][0]["widget"]["title"] == "Widget_cs"
        assert section["items"][0]["widget"]["description"] == "Desc_cs"


# ---------------------------------------------------------------------------
# _extract_dashboard_date_filter_titles — tab-level filters
# ---------------------------------------------------------------------------


class TestExtractDashboardDateFilterTitles:
    """Test date filter title extraction from both top-level and tab content."""

    def _service(self):
        return CatalogWorkspaceService.__new__(CatalogWorkspaceService)

    def test_top_level_date_filter(self):
        to_translate: set[str] = set()
        content = {"dateFilterConfig": {"filterName": "Time period"}}

        self._service()._extract_dashboard_date_filter_titles(to_translate, content)

        assert "Time period" in to_translate

    def test_tab_level_date_filter(self):
        to_translate: set[str] = set()
        content = {
            "tabs": [
                {"dateFilterConfig": {"filterName": "Tab Filter"}},
            ],
        }

        self._service()._extract_dashboard_date_filter_titles(to_translate, content)

        assert "Tab Filter" in to_translate

    def test_both_top_and_tab_date_filters(self):
        to_translate: set[str] = set()
        content = {
            "dateFilterConfig": {"filterName": "Top Filter"},
            "tabs": [
                {"dateFilterConfig": {"filterName": "Tab Filter 1"}},
                {
                    "dateFilterConfigs": [
                        {"config": {"filterName": "Tab Filter 2"}},
                    ],
                },
            ],
        }

        self._service()._extract_dashboard_date_filter_titles(to_translate, content)

        assert "Top Filter" in to_translate
        assert "Tab Filter 1" in to_translate
        assert "Tab Filter 2" in to_translate
