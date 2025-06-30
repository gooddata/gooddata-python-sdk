# (C) 2025 GoodData Corporation

from enum import Enum


class InputType(Enum):
    """Input type for the backup."""

    LIST_OF_WORKSPACES = "list-of-workspaces"
    HIERARCHY = "list-of-parents"
    ORGANIZATION = "entire-organization"
