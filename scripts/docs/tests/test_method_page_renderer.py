# (C) 2026 GoodData Corporation
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS_DOCS = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _setup_path(monkeypatch: pytest.MonkeyPatch) -> None:
    if str(_SCRIPTS_DOCS) not in sys.path:
        monkeypatch.syspath_prepend(str(_SCRIPTS_DOCS))


@pytest.fixture()
def _mod():
    import method_page_renderer as mod

    return mod


# ---------------------------------------------------------------------------
# Sample data (mirrors json_builder output)
# ---------------------------------------------------------------------------

SAMPLE_DATA: dict = {
    "sdk": {
        "kind": "module",
        "catalog": {
            "kind": "module",
            "CatalogDataSourceService": {
                "kind": "class",
                "docstring": "Data source service.",
                "docstring_parsed": {
                    "short_description": "Data source service.",
                    "long_description": "",
                },
                "functions": {
                    "scan_sql": {
                        "kind": "function",
                        "docstring": "Analyze SELECT SQL query.",
                        "signature": {
                            "params": [
                                ["data_source_id: str", "str"],
                                ["sql_request: ScanSqlRequest", "ScanSqlRequest"],
                            ],
                            "return_annotation": "ScanSqlResponse",
                        },
                        "docstring_parsed": {
                            "short_description": "Analyze SELECT SQL query in a given request.",
                            "long_description": "Returns column names with types.",
                            "params": [
                                {
                                    "arg_name": "data_source_id",
                                    "type_name": "str",
                                    "description": "Data source identification string.",
                                },
                                {
                                    "arg_name": "sql_request",
                                    "type_name": "ScanSqlRequest",
                                    "description": "SELECT SQL query to analyze.",
                                },
                            ],
                            "returns": {
                                "type_name": "ScanSqlResponse",
                                "description": "SELECT query analysis result.",
                                "return_name": None,
                            },
                        },
                    },
                    "delete_data_source": {
                        "kind": "function",
                        "docstring": "Delete a data source.",
                        "signature": {
                            "params": [["data_source_id: str", "str"]],
                            "return_annotation": "None",
                        },
                        "docstring_parsed": {
                            "short_description": "Delete a data source by ID.",
                            "long_description": None,
                            "params": [
                                {
                                    "arg_name": "data_source_id",
                                    "type_name": "str",
                                    "description": "The data source ID.",
                                },
                            ],
                            "returns": None,
                        },
                    },
                    "no_docstring_method": {
                        "kind": "function",
                        "docstring": None,
                        "signature": {
                            "params": [["workspace_id: str", "str"]],
                            "return_annotation": "list[str]",
                        },
                        "docstring_parsed": None,
                    },
                },
            },
        },
    },
}


# ---------------------------------------------------------------------------
# build_links
# ---------------------------------------------------------------------------


class TestBuildLinks:
    def test_builds_links_from_nested_data(self, _mod):
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        assert "CatalogDataSourceService" in links
        assert links["CatalogDataSourceService"]["kind"] == "class"
        assert "/catalogdatasourceservice" in links["CatalogDataSourceService"]["path"]

    def test_includes_functions(self, _mod):
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        assert "scan_sql" in links
        assert links["scan_sql"]["kind"] == "function"

    def test_recurses_into_duplicate_module_names(self, _mod):
        """Modules with the same name at different levels should all be recursed into."""
        data = {
            "outer": {
                "kind": "module",
                "inner": {
                    "kind": "module",
                    "MyClass": {"kind": "class", "functions": {}},
                },
            },
            "other": {
                "kind": "module",
                "inner": {
                    "kind": "module",
                    "HiddenClass": {"kind": "class", "functions": {}},
                },
            },
        }
        links = _mod.build_links(data, "/api")
        assert "MyClass" in links
        assert "HiddenClass" in links

    def test_skips_private_functions(self, _mod):
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        for name in links:
            assert not name.startswith("_")


# ---------------------------------------------------------------------------
# resolve_method
# ---------------------------------------------------------------------------


class TestResolveMethod:
    def test_resolves_known_method(self, _mod):
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        assert func is not None
        assert func["kind"] == "function"

    def test_returns_none_for_unknown_class(self, _mod):
        assert _mod.resolve_method(SAMPLE_DATA, "Unknown.scan_sql") is None

    def test_returns_none_for_unknown_method(self, _mod):
        assert _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.unknown") is None

    def test_returns_none_for_bad_format(self, _mod):
        assert _mod.resolve_method(SAMPLE_DATA, "just_a_name") is None

    def test_returns_none_for_empty(self, _mod):
        assert _mod.resolve_method(SAMPLE_DATA, "") is None

    def test_returns_none_for_three_parts(self, _mod):
        assert _mod.resolve_method(SAMPLE_DATA, "A.B.C") is None


# ---------------------------------------------------------------------------
# LinkResolver
# ---------------------------------------------------------------------------


class TestLinkResolver:
    def test_type_link_known(self, _mod):
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        result = resolver.type_link("CatalogDataSourceService")
        assert '<a href="' in result
        assert "CatalogDataSourceService" in result

    def test_type_link_unknown(self, _mod):
        resolver = _mod.LinkResolver({})
        assert resolver.type_link("Unknown") == "Unknown"

    def test_type_link_empty(self, _mod):
        resolver = _mod.LinkResolver({})
        assert resolver.type_link("") == ""

    def test_type_link_none(self, _mod):
        resolver = _mod.LinkResolver({})
        assert resolver.type_link(None) == ""

    def test_type_link_optional_wrapper(self, _mod):
        links = {"Foo": {"path": "/api/foo", "kind": "class"}}
        resolver = _mod.LinkResolver(links)
        result = resolver.type_link("Optional[Foo]")
        assert '<a href="/api/foo/">Foo</a>' in result
        assert "Optional[" in result

    def test_type_link_list_wrapper(self, _mod):
        links = {"Foo": {"path": "/api/foo", "kind": "class"}}
        resolver = _mod.LinkResolver(links)
        result = resolver.type_link("list[Foo]")
        assert '<a href="/api/foo/">Foo</a>' in result
        assert "list[" in result


# ---------------------------------------------------------------------------
# render_method_html
# ---------------------------------------------------------------------------


class TestRenderMethodHtml:
    def test_contains_signature(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "scan_sql" in html
        assert "data_source_id" in html
        assert "ScanSqlRequest" in html

    def test_contains_parameters_table(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "Parameters" in html
        assert "gd-docs-parameters-block" in html

    def test_contains_returns_table(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "Returns" in html
        assert "ScanSqlResponse" in html

    def test_none_return(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.delete_data_source")
        html = _mod.render_method_html("delete_data_source", func, resolver)
        assert "Returns" in html
        assert "<i>None</i>" in html

    def test_auto_generated_comment(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "AUTO-GENERATED FROM DOCSTRING" in html

    def test_description_short_and_long(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "Analyze SELECT SQL query in a given request." in html
        assert "Returns column names with types." in html

    def test_return_type_in_signature(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert "-&gt; ScanSqlResponse" in html

    def test_no_return_arrow_for_none(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.delete_data_source")
        html = _mod.render_method_html("delete_data_source", func, resolver)
        assert "-&gt;" not in html

    def test_no_docstring_fallback_to_signature(self, _mod):
        """When docstring_parsed is None, should fall back to signature params."""
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.no_docstring_method")
        html = _mod.render_method_html("no_docstring_method", func, resolver)
        assert "workspace_id" in html
        assert "No docs" in html or "gd-docs-parameters-block" in html

    def test_type_links_in_params(self, _mod):
        links = {"ScanSqlRequest": {"path": "/api/scansqlrequest", "kind": "class"}}
        resolver = _mod.LinkResolver(links)
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert '<a href="/api/scansqlrequest/">ScanSqlRequest</a>' in html

    def test_type_links_in_return(self, _mod):
        links = {"ScanSqlResponse": {"path": "/api/scansqlresponse", "kind": "class"}}
        resolver = _mod.LinkResolver(links)
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert '<a href="/api/scansqlresponse/">ScanSqlResponse</a>' in html

    def test_python_ref_wrapper(self, _mod):
        resolver = _mod.LinkResolver({})
        func = _mod.resolve_method(SAMPLE_DATA, "CatalogDataSourceService.scan_sql")
        html = _mod.render_method_html("scan_sql", func, resolver)
        assert '<div class="python-ref">' in html
        assert "</div>" in html


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    def test_basic(self, _mod):
        content = '---\ntitle: "test"\napi_ref: "Foo.bar"\n---\n\nBody text\n'
        fm_block, kv, rest = _mod.parse_frontmatter(content)
        assert kv["title"] == "test"
        assert kv["api_ref"] == "Foo.bar"
        assert "Body text" in rest

    def test_no_frontmatter(self, _mod):
        content = "Just some text\n"
        fm_block, kv, rest = _mod.parse_frontmatter(content)
        assert fm_block == ""
        assert kv == {}
        assert rest == content

    def test_quoted_api_ref(self, _mod):
        content = '---\napi_ref: "MyClass.my_method"\n---\nBody\n'
        _, kv, _ = _mod.parse_frontmatter(content)
        assert kv["api_ref"] == "MyClass.my_method"

    def test_preserves_frontmatter_block(self, _mod):
        content = '---\ntitle: "test"\nweight: 10\n---\nBody\n'
        fm_block, _, _ = _mod.parse_frontmatter(content)
        assert fm_block == '---\ntitle: "test"\nweight: 10\n---\n'

    def test_multiline_values(self, _mod):
        content = '---\ntitle: "a title"\nsuperheading: "service."\napi_ref: "Svc.method"\n---\n'
        _, kv, _ = _mod.parse_frontmatter(content)
        assert kv["superheading"] == "service."


# ---------------------------------------------------------------------------
# process_file (integration)
# ---------------------------------------------------------------------------


class TestProcessFile:
    def test_updates_file_with_api_ref(self, _mod, tmp_path):
        md = tmp_path / "test.md"
        md.write_text(
            '---\ntitle: "scan_sql"\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n'
            "Old content here\n\n## Example\n\n```python\nsdk.scan_sql()\n```\n"
        )
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        changed = _mod.process_file(md, SAMPLE_DATA, resolver)
        assert changed

        content = md.read_text()
        assert "AUTO-GENERATED FROM DOCSTRING" in content
        assert "## Example" in content
        assert "sdk.scan_sql()" in content
        assert "Old content here" not in content

    def test_preserves_example_section(self, _mod, tmp_path):
        md = tmp_path / "test.md"
        example = "## Example\n\n```python\nmy_example_code()\n```\n"
        md.write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\nOld stuff\n\n' + example)
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        _mod.process_file(md, SAMPLE_DATA, resolver)

        content = md.read_text()
        assert "my_example_code()" in content

    def test_preserves_h3_example(self, _mod, tmp_path):
        """### Example headings should also be preserved."""
        md = tmp_path / "test.md"
        md.write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\nOld\n\n### Example\n\nkept\n')
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        _mod.process_file(md, SAMPLE_DATA, resolver)

        content = md.read_text()
        assert "### Example" in content
        assert "kept" in content

    def test_strips_parameters_returns_headings(self, _mod, tmp_path):
        """## Parameters and ## Returns should NOT be preserved (they're auto-generated)."""
        md = tmp_path / "test.md"
        md.write_text(
            '---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n'
            "## Parameters\n\nold param table\n\n## Returns\n\nold return\n\n## Example\n\nkept\n"
        )
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        _mod.process_file(md, SAMPLE_DATA, resolver)

        content = md.read_text()
        assert "old param table" not in content
        assert "old return" not in content
        assert "## Example" in content
        assert "kept" in content

    def test_skips_file_without_api_ref(self, _mod, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("---\ntitle: test\n---\nBody\n")
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        changed = _mod.process_file(md, SAMPLE_DATA, resolver)
        assert not changed

    def test_warns_on_unresolvable_api_ref(self, _mod, tmp_path, capsys):
        md = tmp_path / "test.md"
        md.write_text('---\napi_ref: "Nonexistent.method"\n---\nBody\n')
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        changed = _mod.process_file(md, SAMPLE_DATA, resolver)
        assert not changed
        assert "WARN" in capsys.readouterr().out

    def test_dry_run_does_not_write(self, _mod, tmp_path):
        md = tmp_path / "test.md"
        original = '---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n## Example\ncode\n'
        md.write_text(original)
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        changed = _mod.process_file(md, SAMPLE_DATA, resolver, dry_run=True)
        assert changed
        assert md.read_text() == original

    def test_idempotent(self, _mod, tmp_path):
        """Running the renderer twice should produce identical output."""
        md = tmp_path / "test.md"
        md.write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n## Example\n\ncode\n')
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)

        _mod.process_file(md, SAMPLE_DATA, resolver)
        first_pass = md.read_text()

        changed = _mod.process_file(md, SAMPLE_DATA, resolver)
        assert not changed  # no change on second pass
        assert md.read_text() == first_pass

    def test_no_example_section(self, _mod, tmp_path):
        """Files without any ## heading should still render (no preserved section)."""
        md = tmp_path / "test.md"
        md.write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\nOld content\n')
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)

        changed = _mod.process_file(md, SAMPLE_DATA, resolver)
        assert changed
        content = md.read_text()
        assert "AUTO-GENERATED" in content
        assert "Old content" not in content

    def test_uses_links_json(self, _mod, tmp_path):
        """When links are provided via dict (simulating --links-json), type links work."""
        md = tmp_path / "test.md"
        md.write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n## Example\ncode\n')
        # Provide explicit links (as --links-json would)
        links = {"ScanSqlResponse": {"path": "/v1/api-reference/scansqlresponse", "kind": "class"}}
        resolver = _mod.LinkResolver(links)
        _mod.process_file(md, SAMPLE_DATA, resolver)

        content = md.read_text()
        assert '<a href="/v1/api-reference/scansqlresponse/">ScanSqlResponse</a>' in content


# ---------------------------------------------------------------------------
# process_directory
# ---------------------------------------------------------------------------


class TestProcessDirectory:
    def test_processes_matching_files(self, _mod, tmp_path):
        (tmp_path / "good.md").write_text(
            '---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n## Example\ncode\n'
        )
        (tmp_path / "skip.md").write_text("---\ntitle: skip\n---\nno api_ref\n")
        (tmp_path / "_index.md").write_text("---\ntitle: index\n---\n")

        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        count = _mod.process_directory(tmp_path, SAMPLE_DATA, resolver)
        assert count == 1

    def test_processes_subdirectories(self, _mod, tmp_path):
        sub = tmp_path / "section"
        sub.mkdir()
        (sub / "method.md").write_text('---\napi_ref: "CatalogDataSourceService.scan_sql"\n---\n\n## Example\ncode\n')
        links = _mod.build_links(SAMPLE_DATA, "/latest/api-reference")
        resolver = _mod.LinkResolver(links)
        count = _mod.process_directory(tmp_path, SAMPLE_DATA, resolver)
        assert count == 1
