# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins

from attrs import define, field
from gooddata_api_client.model.assignee_rule import AssigneeRule

from gooddata_sdk.catalog.base import Base, value_in_allowed


@define(kw_only=True)
class CatalogAssigneeRule(Base):
    type: str = field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> builtins.type[AssigneeRule]:
        return AssigneeRule
