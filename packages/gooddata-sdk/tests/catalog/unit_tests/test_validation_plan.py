# (C) 2026 GoodData Corporation
"""What deploying a layout would do to a workspace.

Deploying the analytics model replaces it wholesale, so the deletions are the part worth
testing: they are silent, not undoable, and nobody asked for them.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.plan import build_deploy_plan


def _model(**collections: list[str]) -> CatalogDeclarativeAnalytics:
    payload: dict[str, Any] = {}
    for name, ids in collections.items():
        payload[name] = [{"id": object_id, "title": object_id, "content": {}} for object_id in ids]
    return CatalogDeclarativeAnalytics.from_dict({"analytics": payload}, camel_case=True)


def _plan(current: CatalogDeclarativeAnalytics, incoming: CatalogDeclarativeAnalytics):
    return build_deploy_plan(current, incoming, workspace_id="ws")


class TestPlan:
    def test_an_identical_layout_is_all_updates(self):
        plan = _plan(_model(metrics=["a", "b"]), _model(metrics=["a", "b"]))
        assert plan.deletes_anything is False
        assert plan.collections[0].updated == ["a", "b"]
        assert plan.collections[0].created == []

    def test_new_objects_are_creates(self):
        plan = _plan(_model(metrics=["a"]), _model(metrics=["a", "b"]))
        assert plan.collections[0].created == ["b"]
        assert plan.collections[0].updated == ["a"]

    def test_an_object_absent_from_the_layout_is_a_deletion(self):
        """The migration hazard: a partial export silently removes everything it omits."""
        plan = _plan(_model(metrics=["keep", "drop"]), _model(metrics=["keep"]))
        assert plan.deletes_anything is True
        assert plan.collections[0].deleted == ["drop"]
        assert plan.total_deleted == 1

    def test_an_empty_layout_deletes_everything_the_workspace_owns(self):
        plan = _plan(_model(metrics=["a", "b"], visualizationObjects=["v"]), _model())
        assert plan.total_deleted == 3

    def test_collections_that_do_not_change_are_left_out(self):
        plan = _plan(_model(metrics=["a"], visualizationObjects=[]), _model(metrics=["a", "b"]))
        assert [entry.collection for entry in plan.collections] == ["metrics"]

    def test_an_unchanged_workspace_reports_no_changes(self):
        assert "No changes" in _plan(_model(), _model()).format()


class TestFormatting:
    def test_deletions_are_stated_first_and_counted(self):
        """A plan that buries the deletions under two hundred routine updates is the plan
        nobody reads to the end."""
        text = _plan(_model(metrics=["a", "b", "c"]), _model(metrics=["a"])).format()
        assert text.index("DELETED") < text.index("metrics: 0 created")
        assert "2 object(s) exist in ws but not in this layout" in text

    def test_long_deletion_lists_are_sampled_with_a_count(self):
        current = _model(metrics=[f"m{i}" for i in range(20)])
        text = _plan(current, _model(metrics=["m0"])).format(sample=3)
        assert "(+16 more)" in text

    def test_a_pure_creation_plan_mentions_no_deletions(self):
        text = _plan(_model(), _model(metrics=["a"])).format()
        assert "DELETED" not in text
        assert "metrics: 1 created, 0 updated" in text
