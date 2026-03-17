# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import pytest
from gooddata_sdk import (
    CatalogCreateKnowledgeDocumentRequest,
    CatalogPatchKnowledgeDocumentRequest,
    CatalogUpsertKnowledgeDocumentRequest,
    GoodDataSdk,
)
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"

_WORKSPACE_ID = "demo"
_FILENAME = "test_document.txt"


@gd_vcr.use_cassette(str(_fixtures_dir / "test_list_documents.yaml"))
def test_list_documents(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    result = sdk.catalog_knowledge.list_documents(workspace_id=_WORKSPACE_ID)
    assert result is not None
    assert isinstance(result.documents, list)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_search_knowledge.yaml"))
def test_search_knowledge(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    result = sdk.catalog_knowledge.search_knowledge(workspace_id=_WORKSPACE_ID, query="test query")
    assert result is not None
    assert isinstance(result.results, list)
    assert result.statistics is not None


@gd_vcr.use_cassette(str(_fixtures_dir / "test_create_document.yaml"))
def test_create_document(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    request = CatalogCreateKnowledgeDocumentRequest(
        content="Test content for knowledge document.",
        filename=_FILENAME,
    )
    try:
        result = sdk.catalog_knowledge.create_document(workspace_id=_WORKSPACE_ID, request=request)
        assert result is not None
        assert result.success is True
        assert result.filename == _FILENAME
    finally:
        sdk.catalog_knowledge.delete_document(workspace_id=_WORKSPACE_ID, filename=_FILENAME)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_upsert_document.yaml"))
def test_upsert_document(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    request = CatalogUpsertKnowledgeDocumentRequest(
        content="Upserted content for knowledge document.",
        filename=_FILENAME,
    )
    try:
        result = sdk.catalog_knowledge.upsert_document(workspace_id=_WORKSPACE_ID, request=request)
        assert result is not None
        assert result.success is True
        assert result.filename == _FILENAME
    finally:
        sdk.catalog_knowledge.delete_document(workspace_id=_WORKSPACE_ID, filename=_FILENAME)


@gd_vcr.use_cassette(str(_fixtures_dir / "test_get_document.yaml"))
def test_get_document(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    result = sdk.catalog_knowledge.get_document(workspace_id=_WORKSPACE_ID, filename=_FILENAME)
    assert result is not None
    assert result.filename == _FILENAME


@gd_vcr.use_cassette(str(_fixtures_dir / "test_patch_document.yaml"))
def test_patch_document(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    patch_request = CatalogPatchKnowledgeDocumentRequest(title="Updated Title")
    result = sdk.catalog_knowledge.patch_document(
        workspace_id=_WORKSPACE_ID, filename=_FILENAME, request=patch_request
    )
    assert result is not None
    assert result.filename == _FILENAME


@gd_vcr.use_cassette(str(_fixtures_dir / "test_delete_document.yaml"))
def test_delete_document(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    result = sdk.catalog_knowledge.delete_document(workspace_id=_WORKSPACE_ID, filename=_FILENAME)
    assert result is not None
    assert result.success is True
