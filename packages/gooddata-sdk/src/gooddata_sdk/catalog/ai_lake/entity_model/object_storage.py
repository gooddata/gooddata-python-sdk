# (C) 2026 GoodData Corporation
"""SDK model for AI Lake ObjectStorage descriptors."""

from __future__ import annotations

from typing import Any

import attrs


@attrs.define(kw_only=True)
class CatalogObjectStorageInfo:
    """Descriptor of a registered AI Lake ObjectStorage.

    Provider credentials are stripped server-side — only safe descriptors
    (id, name, type, and provider-specific metadata like bucket/region) are
    returned.  Use :attr:`name` as ``source_storage_name`` when calling
    :py:meth:`~gooddata_sdk.catalog.ai_lake.service.CatalogAILakeService.create_pipe_table`,
    or pass :attr:`storage_id` to the ``storageIds`` list of a
    ``ProvisionDatabase`` request.
    """

    name: str
    """Human-readable name of the storage configuration."""

    storage_id: str
    """Stable UUID identifier of the storage configuration."""

    storage_type: str
    """Provider type (e.g. ``S3``, ``MINIO``, ``ADLS``)."""

    storage_config: dict[str, str] = attrs.field(factory=dict)
    """Provider-specific descriptors (bucket, region, endpoint, …).

    Credential references (keys ending in ``_env``) are stripped by the server.
    """

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CatalogObjectStorageInfo:
        """Construct from a snake_case dict as returned by the API client's ``to_dict()``."""
        return cls(
            name=data["name"],
            storage_id=data["storage_id"],
            storage_type=data["storage_type"],
            storage_config=data.get("storage_config") or {},
        )
