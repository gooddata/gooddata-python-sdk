# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Type

import attr
from gooddata_api_client.model.assignee_rule import AssigneeRule

from gooddata_sdk.catalog.base import Base, value_in_allowed


@attr.s(auto_attribs=True, kw_only=True)
class CatalogAssigneeRule(Base):
    type: str = attr.field(validator=value_in_allowed)

    @staticmethod
    def client_class() -> Type[AssigneeRule]:
        return AssigneeRule
