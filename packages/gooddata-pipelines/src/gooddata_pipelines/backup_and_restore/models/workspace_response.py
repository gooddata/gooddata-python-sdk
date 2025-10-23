# (C) 2025 GoodData Corporation

from pydantic import (
    BaseModel,
    ConfigDict,
)
from pydantic.alias_generators import (
    to_camel,
)


class Page(BaseModel):
    size: int
    total_elements: int
    total_pages: int
    number: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Hierarchy(BaseModel):
    children_count: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Meta(BaseModel):
    page: Page | None = None
    hierarchy: Hierarchy | None = None


class Workspace(BaseModel):
    id: str
    meta: Meta | None = None


class Links(BaseModel):
    self: str
    next: str | None = None


class WorkspaceResponse(BaseModel):
    data: list[Workspace]
    links: Links
    meta: Meta
