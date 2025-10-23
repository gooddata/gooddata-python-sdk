# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_fdw.environment import ColumnDefinition


def validate_columns_in_table_def(table_columns: dict[str, ColumnDefinition], query_columns: list[str]) -> None:
    unknown_columns = [column for column in query_columns if column not in table_columns]
    if unknown_columns:
        raise ValueError(f"Table does not contain the following requested columns: {str(unknown_columns)}")


class ColumnValidator:
    def validate(self, column_name: str, column_def: ColumnDefinition) -> None:
        raise NotImplementedError()


class LocalIdOptionValidator(ColumnValidator):
    def validate(self, column_name: str, column_def: ColumnDefinition) -> None:
        if "local_id" not in column_def.options:
            raise ValueError(
                f"Foreign table column '{column_name}' is not defined correctly. "
                f"For tables that map GoodData.CN insight, the column OPTIONS must specify "
                f"'localId' which is localIdentifier of the Insight's bucket item. If you created "
                f"this table manually, please rather use the IMPORT FOREIGN SCHEMA and import "
                f"from the 'gooddata_insights' schema. The import will set everything correctly."
            )


class IdOptionValidator(ColumnValidator):
    def __init__(self, mandatory: bool):
        self._mandatory = mandatory

    def validate(self, column_name: str, column_def: ColumnDefinition) -> None:
        if "id" not in column_def.options:
            if self._mandatory:
                raise ValueError(
                    f"Foreign table column '{column_name}' is not defined correctly. "
                    f"For tables mapping to GoodData.CN semantic layer, the column OPTIONS must specify "
                    f"'id' in format: 'fact/your.fact.id', 'label/your.label.id', 'metric/your.metric.id'."
                )
        else:
            split = column_def.options["id"].split("/")

            if len(split) > 2 or split[0] not in ("fact", "label", "metric"):
                raise ValueError(
                    f"Foreign table column '{column_name}' is not defined correctly. "
                    f"OPTIONS 'id' expected format is: 'fact/your.fact.id', 'label/your.label.id', "
                    f"'metric/your.metric.id'. Instead got: {column_def.options['id']}"
                )
