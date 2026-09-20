# (C) 2026 GoodData Corporation
"""Logical-model checks.

The composite-key cases are the reason most of this exists. A dataset can legitimately be
joined on, and grained by, a column it does not declare itself, because that component
arrives through one of its own references -- and a validator that does not know this
reports ordinary joins as broken.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.ldm import (
    check_dataset_references,
    check_dataset_sources,
    check_duplicate_ldm_ids,
    check_grain,
    validate_ldm,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel


def _dataset(
    dataset_id: str,
    *,
    attributes: tuple[str, ...] = (),
    facts: tuple[str, ...] = (),
    grain: tuple[tuple[str, str], ...] = (),
    references: tuple[dict[str, Any], ...] = (),
    table: str | None = "T",
    sql: str | None = None,
) -> dict[str, Any]:
    dataset: dict[str, Any] = {
        "id": dataset_id,
        "title": dataset_id,
        "grain": [{"id": entry_id, "type": entry_type} for entry_id, entry_type in grain],
        "references": list(references),
        "attributes": [
            {"id": attribute, "title": attribute, "labels": [{"id": f"{attribute}.name", "title": attribute}]}
            for attribute in attributes
        ],
        "facts": [{"id": fact, "title": fact} for fact in facts],
    }
    if table is not None:
        dataset["dataSourceTableId"] = {"dataSourceId": "ds", "id": table, "type": "dataSource"}
    if sql is not None:
        dataset["sql"] = {"dataSourceId": "ds", "statement": sql}
    return dataset


def _reference(target: str, *sources: tuple[str, str]) -> dict[str, Any]:
    return {
        "identifier": {"id": target, "type": "dataset"},
        "multivalue": False,
        "sources": [
            {"column": column, "target": {"id": target_id, "type": "attribute"}} for target_id, column in sources
        ],
    }


def _model(datasets: list[dict[str, Any]], date_instances: tuple[str, ...] = ()) -> CatalogDeclarativeModel:
    return CatalogDeclarativeModel.from_dict(
        {
            "ldm": {
                "datasets": datasets,
                "dateInstances": [
                    {
                        "id": d,
                        "title": d,
                        "granularities": ["DAY"],
                        "granularitiesFormatting": {"titleBase": "", "titlePattern": "%titleBase"},
                    }
                    for d in date_instances
                ],
            }
        },
        camel_case=True,
    )


def _codes(findings: list[Any]) -> list[str]:
    return [f.code for f in findings]


class TestDatasetReferences:
    def test_a_join_to_a_declared_attribute_resolves(self):
        model = _model(
            [
                _dataset("dim", attributes=("code",)),
                _dataset("fact", references=(_reference("dim", ("code", "CODE")),)),
            ]
        )
        assert check_dataset_references(model) == []

    def test_a_reference_to_a_dataset_that_is_not_there_is_an_error(self):
        model = _model([_dataset("fact", references=(_reference("gone", ("code", "CODE")),))])
        findings = check_dataset_references(model)
        assert _codes(findings) == ["unresolved_dataset_reference"]
        assert findings[0].object_id == "fact"

    def test_a_join_on_a_column_the_target_does_not_have_is_an_error(self):
        model = _model(
            [
                _dataset("dim", attributes=("code",)),
                _dataset("fact", references=(_reference("dim", ("other", "OTHER")),)),
            ]
        )
        findings = check_dataset_references(model)
        assert _codes(findings) == ["unresolved_reference_source"]
        assert "does not declare" in findings[0].message

    def test_a_column_that_exists_in_some_other_dataset_does_not_count(self):
        """Resolution is against the dataset the reference names, not the whole model: a
        join to the wrong dataset still does not join."""
        model = _model(
            [
                _dataset("dim", attributes=("code",)),
                _dataset("elsewhere", attributes=("other",)),
                _dataset("fact", references=(_reference("dim", ("other", "OTHER")),)),
            ]
        )
        assert _codes(check_dataset_references(model)) == ["unresolved_reference_source"]

    def test_a_grain_component_inherited_through_a_reference_is_joinable(self):
        """The composite-key case. ``dim`` is grained on ``issuer`` but declares only
        ``code``; ``issuer`` arrives through its own reference. Joining to ``dim`` on
        ``issuer`` is ordinary and must not be reported."""
        model = _model(
            [
                _dataset("issuer_dim", attributes=("issuer",)),
                _dataset(
                    "dim",
                    attributes=("code",),
                    grain=(("issuer", "attribute"), ("code", "attribute")),
                    references=(_reference("issuer_dim", ("issuer", "ISSUER")),),
                ),
                _dataset("fact", references=(_reference("dim", ("issuer", "ISSUER"), ("code", "CODE")),)),
            ]
        )
        assert check_dataset_references(model) == []

    def test_a_reference_to_a_date_instance_resolves(self):
        model = _model([_dataset("fact", references=(_reference("d1"),))], date_instances=("d1",))
        assert check_dataset_references(model) == []

    def test_date_sources_are_not_resolved_against_attributes(self):
        """A date dataset's fields are granularities the platform generates, not attributes
        the model declares."""
        reference = {
            "identifier": {"id": "d1", "type": "dataset"},
            "multivalue": False,
            "sources": [{"column": "DT", "target": {"id": "d1", "type": "date"}}],
        }
        model = _model([_dataset("fact", references=(reference,))], date_instances=("d1",))
        assert check_dataset_references(model) == []


class TestGrain:
    def test_a_grain_on_a_declared_attribute_is_fine(self):
        assert check_grain(_model([_dataset("d", attributes=("a",), grain=(("a", "attribute"),))])) == []

    def test_a_grain_naming_nothing_is_an_error(self):
        model = _model([_dataset("d", attributes=("a",), grain=(("ghost", "attribute"),))])
        findings = check_grain(model)
        assert _codes(findings) == ["unresolved_grain"]
        assert "ghost" in findings[0].message

    def test_a_grain_component_reachable_through_a_reference_is_accepted(self):
        model = _model(
            [
                _dataset("parent", attributes=("issuer",)),
                _dataset(
                    "child",
                    attributes=("code",),
                    grain=(("issuer", "attribute"), ("code", "attribute")),
                    references=(_reference("parent", ("issuer", "ISSUER")),),
                ),
            ]
        )
        assert check_grain(model) == []

    def test_a_date_grain_entry_is_left_alone(self):
        assert check_grain(_model([_dataset("d", grain=(("process_date", "date"),))])) == []


class TestDuplicates:
    def test_two_datasets_with_one_id_are_reported(self):
        model = _model([_dataset("same"), _dataset("same")])
        assert "duplicate_dataset_id" in _codes(check_duplicate_ldm_ids(model))

    def test_one_attribute_id_in_two_datasets_is_reported(self):
        """A metric names a label by id alone, with no dataset to disambiguate it."""
        model = _model([_dataset("a", attributes=("shared",)), _dataset("b", attributes=("shared",))])
        codes = _codes(check_duplicate_ldm_ids(model))
        assert "duplicate_attribute_id" in codes
        assert "duplicate_label_id" in codes

    def test_a_fact_sharing_an_id_is_reported(self):
        model = _model([_dataset("a", facts=("f",)), _dataset("b", facts=("f",))])
        assert "duplicate_fact_id" in _codes(check_duplicate_ldm_ids(model))

    def test_distinct_ids_are_quiet(self):
        model = _model([_dataset("a", attributes=("x",)), _dataset("b", attributes=("y",))])
        assert check_duplicate_ldm_ids(model) == []


class TestDatasetSources:
    def test_a_table_backed_dataset_is_fine(self):
        assert check_dataset_sources(_model([_dataset("d")])) == []

    def test_a_sql_backed_dataset_is_fine(self):
        assert check_dataset_sources(_model([_dataset("d", table=None, sql="SELECT 1")])) == []

    def test_a_dataset_with_neither_is_a_warning(self):
        findings = check_dataset_sources(_model([_dataset("d", table=None)]))
        assert _codes(findings) == ["dataset_without_source"]
        assert findings[0].severity.value == "warning"

    def test_a_dataset_with_both_is_a_warning(self):
        assert _codes(check_dataset_sources(_model([_dataset("d", sql="SELECT 1")]))) == ["dataset_with_two_sources"]


class TestValidateLdm:
    def test_an_empty_model_is_quiet(self):
        assert validate_ldm(CatalogDeclarativeModel(ldm=None)) == []

    def test_every_check_runs(self):
        model = _model(
            [
                _dataset("a", attributes=("x",), grain=(("ghost", "attribute"),), table=None),
                _dataset("a", references=(_reference("gone"),)),
            ]
        )
        codes = set(_codes(validate_ldm(model)))
        assert {"duplicate_dataset_id", "unresolved_grain", "unresolved_dataset_reference"} <= codes
