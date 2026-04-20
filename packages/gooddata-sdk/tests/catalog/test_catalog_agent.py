# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk.catalog.organization.entity_model.agent import (
    CatalogAgent,
    CatalogAgentAttributes,
    CatalogAgentDocument,
    CatalogAgentPatchDocument,
)

# ---------------------------------------------------------------------------
# Unit tests – no live server, no cassettes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario,agent_id,title,description,enabled,ai_knowledge,available_to_all,skills_mode,custom_skills,personality",
    [
        (
            "minimal",
            "agent-1",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "full",
            "agent-full",
            "Full Agent",
            "A fully configured agent",
            True,
            True,
            False,
            "custom",
            ["alert", "metric"],
            "helpful",
        ),
        (
            "skills_mode_all",
            "agent-all",
            "All Skills Agent",
            None,
            True,
            False,
            True,
            "all",
            None,
            None,
        ),
    ],
)
def test_catalog_agent_init(
    scenario,
    agent_id,
    title,
    description,
    enabled,
    ai_knowledge,
    available_to_all,
    skills_mode,
    custom_skills,
    personality,
):
    """Verify CatalogAgent.init() round-trips through as_api_model without errors."""
    agent = CatalogAgent.init(
        id=agent_id,
        title=title,
        description=description,
        enabled=enabled,
        ai_knowledge=ai_knowledge,
        available_to_all=available_to_all,
        skills_mode=skills_mode,
        custom_skills=custom_skills,
        personality=personality,
    )

    assert agent.id == agent_id
    assert agent.attributes is not None
    assert agent.attributes.title == title
    assert agent.attributes.description == description
    assert agent.attributes.enabled == enabled
    assert agent.attributes.ai_knowledge == ai_knowledge
    assert agent.attributes.available_to_all == available_to_all
    assert agent.attributes.skills_mode == skills_mode
    assert agent.attributes.custom_skills == custom_skills
    assert agent.attributes.personality == personality

    # Should not raise
    api_model = agent.to_api()
    assert api_model is not None
    assert api_model["id"] == agent_id


def test_catalog_agent_document_wraps_agent():
    """CatalogAgentDocument.to_api() must carry the inner agent data."""
    agent = CatalogAgent.init(id="doc-agent", title="Doc Agent", enabled=True)
    doc = CatalogAgentDocument(data=agent)
    api_doc = doc.to_api()
    assert api_doc["data"]["id"] == "doc-agent"


def test_catalog_agent_patch_document_wraps_agent():
    """CatalogAgentPatchDocument.to_api() must carry the inner agent data."""
    agent = CatalogAgent.init(id="patch-agent", title="Patched Title")
    patch_doc = CatalogAgentPatchDocument(data=agent)
    api_patch_doc = patch_doc.to_api()
    assert api_patch_doc["data"]["id"] == "patch-agent"


def test_catalog_agent_from_api_full():
    """CatalogAgent.from_api() correctly maps all camelCase API fields."""

    class _FakeAttrs:
        """Mimics OpenApiModel dict-like access."""

        def __init__(self, data):
            self._data = data

        def __getitem__(self, key):
            return self._data[key]

        def get(self, key, default=None):
            return self._data.get(key, default)

        def __contains__(self, key):
            return key in self._data

    fake_attrs = _FakeAttrs(
        {
            "title": "My Agent",
            "description": "desc",
            "ai_knowledge": True,
            "available_to_all": False,
            "custom_skills": ["alert", "metric"],
            "enabled": True,
            "personality": "friendly",
            "skills_mode": "custom",
        }
    )

    class _FakeEntity:
        def __getitem__(self, key):
            if key == "id":
                return "agent-from-api"
            if key == "attributes":
                return fake_attrs
            raise KeyError(key)

        def get(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                return default

    agent = CatalogAgent.from_api(_FakeEntity())
    assert agent.id == "agent-from-api"
    assert agent.attributes.title == "My Agent"
    assert agent.attributes.description == "desc"
    assert agent.attributes.ai_knowledge is True
    assert agent.attributes.available_to_all is False
    assert agent.attributes.custom_skills == ["alert", "metric"]
    assert agent.attributes.enabled is True
    assert agent.attributes.personality == "friendly"
    assert agent.attributes.skills_mode == "custom"


def test_catalog_agent_from_api_minimal():
    """CatalogAgent.from_api() handles missing optional attributes gracefully."""

    class _FakeEntity:
        def __getitem__(self, key):
            if key == "id":
                return "bare-agent"
            if key == "attributes":
                return {}
            raise KeyError(key)

        def get(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                return default

    agent = CatalogAgent.from_api(_FakeEntity())
    assert agent.id == "bare-agent"
    assert agent.attributes is not None
    assert agent.attributes.title is None
    assert agent.attributes.enabled is None
    assert agent.attributes.custom_skills is None


def test_catalog_agent_attributes_defaults():
    """CatalogAgentAttributes defaults to all-None when constructed empty."""
    attrs = CatalogAgentAttributes()
    assert attrs.title is None
    assert attrs.description is None
    assert attrs.ai_knowledge is None
    assert attrs.available_to_all is None
    assert attrs.custom_skills is None
    assert attrs.enabled is None
    assert attrs.personality is None
    assert attrs.skills_mode is None
