# (C) 2022 GoodData Corporation
from __future__ import annotations

from enum import Enum

# Use typing collection types to support python < py3.9
ValidObjects = dict[str, set[str]]


class UpsertOutcome(str, Enum):
    """Which branch a ``create_or_update*`` method took.

    The outcome is best-effort: it reports the branch the SDK chose after its
    existence check, and that check is not atomic with the write that follows.
    A concurrent actor can create or delete the entity in between, so treat the
    value as informational rather than as an authoritative audit record.
    """

    CREATED = "created"
    UPDATED = "updated"

    # Match StrEnum's str() (the value, not "UpsertOutcome.CREATED") so moving
    # to StrEnum once py3.10 support is dropped is a no-op for callers.
    __str__ = str.__str__
