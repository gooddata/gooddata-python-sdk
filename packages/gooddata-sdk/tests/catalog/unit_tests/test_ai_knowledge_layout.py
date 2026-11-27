# (C) 2026 GoodData Corporation
"""AI Knowledge as YAML: the folder tree on disk, and syncing it with the AI Knowledge API."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import requests
import yaml
from gooddata_sdk.catalog.ai_knowledge.declarative_model import (
    CatalogDeclarativeAIKnowledge,
    CatalogDeclarativeKnowledgeDocument,
    CatalogDeclarativeKnowledgeExtraction,
    CatalogDeclarativeKnowledgeField,
    CatalogDeclarativeKnowledgeFolder,
)
from gooddata_sdk.catalog.ai_knowledge.service import AIKnowledgeApiError, CatalogAIKnowledgeService

PART = 8


class FakeAIKnowledge:
    """The organization AI Knowledge API, in memory, as far as the service uses it."""

    def __init__(self) -> None:
        self.folders: dict[str, dict[str, Any]] = {}
        self.documents: dict[str, dict[str, Any]] = {}
        self.uploads: dict[str, dict[str, Any]] = {}
        self.imports: list[str] = []
        self.calls: list[str] = []

    def __call__(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        path = endpoint.removeprefix("/api/v1/ai/organization/knowledge")
        self.calls.append(f"{method} {path}")
        body = kwargs.get("json")
        if method == "GET" and path == "/folders":
            return _response(200, {"folders": [self._out(f) for f in self.folders.values()]})
        if method == "POST" and path == "/folders":
            if any(
                f["name"] == body["name"] and f.get("parentId") == body.get("parentId") for f in self.folders.values()
            ):
                return _response(409, {"detail": "exists"})
            folder = {"id": str(uuid.uuid4()), **body}
            self.folders[folder["id"]] = folder
            return _response(201, self._out(folder))
        if m := re.fullmatch(r"/folders/([^/]+)", path):
            if method == "PATCH":
                self.folders[m[1]].update(body)
                return _response(200, self._out(self.folders[m[1]]))
            if method == "DELETE":
                self.folders.pop(m[1])
                return _response(200, {"success": True})
        if method == "GET" and path == "/documents":
            return _response(200, {"documents": list(self.documents.values())})
        if m := re.fullmatch(r"/documents/([^/]+)", path):
            self.documents[m[1]].update(body)
            return _response(200, self.documents[m[1]])
        if method == "POST" and path == "/uploads":
            upload_id = uuid.uuid4().hex
            self.uploads[upload_id] = {**body, "parts": {}}
            return _response(
                201, {"uploadId": upload_id, "partSize": PART, "partCount": max(1, -(-body["size"] // PART))}
            )
        if m := re.fullmatch(r"/uploads/([^/]+)/parts/(\d+)", path):
            self.uploads[m[1]]["parts"][int(m[2])] = kwargs["data"]
            return _response(204, None)
        if m := re.fullmatch(r"/uploads/([^/]+)/complete", path):
            upload = self.uploads.pop(m[1])
            content = b"".join(upload["parts"][n] for n in sorted(upload["parts"]))
            return _response(
                200, self._document(upload["filename"], upload.get("folderId"), upload.get("title"), content)
            )
        if method == "POST" and path == "/imports":
            self.imports.append(body["url"])
            return _response(202, self._document(body["filename"], body.get("folderId"), body.get("title"), b""))
        raise AssertionError(f"unexpected {method} {path}")

    def _document(self, filename: str, folder_id: str | None, title: str | None, content: bytes) -> dict[str, Any]:
        existing = next((d for d in self.documents.values() if d["filename"] == filename), None)
        document = existing or {"id": str(uuid.uuid4()), "filename": filename}
        document.update({"folderId": folder_id, "title": title, "content": content.decode()})
        self.documents[document["id"]] = document
        return document

    def _out(self, folder: dict[str, Any]) -> dict[str, Any]:
        path, current = [], folder
        while current is not None:
            path.insert(0, current["name"])
            current = self.folders.get(current.get("parentId") or "")
        return {"extraction": {}, "access": None, **folder, "path": path}


def _response(status: int, body: Any) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(body).encode() if body is not None else b""
    response.request = requests.Request("GET", "http://test").prepare()
    return response


@pytest.fixture
def api() -> FakeAIKnowledge:
    return FakeAIKnowledge()


@pytest.fixture
def service(api: FakeAIKnowledge) -> CatalogAIKnowledgeService:
    client = MagicMock()
    client.request.side_effect = api
    return CatalogAIKnowledgeService(client)


def _layout(tmp_path: Path) -> CatalogDeclarativeAIKnowledge:
    contracts = tmp_path / "ai_knowledge" / "Contracts"
    (contracts / "files").mkdir(parents=True)
    (contracts / "files" / "acme.md").write_text("ACME renews every January and pays net 30.")
    (contracts / "Customers").mkdir()
    (contracts / "folder.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "Contracts",
                "extraction": {
                    "model": "gpt-4.1-mini",
                    "summary_instruction": "Commercial terms in three sentences.",
                    "fields": [{"name": "Renewal", "instruction": "When does it renew?"}],
                },
                "access": {"workspaces": ["sales"]},
            }
        )
    )
    (contracts / "documents.yaml").write_text(
        yaml.safe_dump(
            [
                {"file": "acme.md", "title": "ACME contract", "path": "files/acme.md"},
                {"file": "globex.pdf", "source": "https://files.example.com/globex.pdf"},
            ]
        )
    )
    (contracts / "Customers" / "folder.yaml").write_text(yaml.safe_dump({"name": "Customers"}))
    return CatalogDeclarativeAIKnowledge.load_from_disk(tmp_path)


def test_a_subfolder_inherits_unless_it_says_otherwise(tmp_path: Path) -> None:
    layout = _layout(tmp_path)

    contracts = layout.folders[0]
    customers = contracts.folders[0]
    assert contracts.extraction is not None
    assert contracts.extraction.fields == [
        CatalogDeclarativeKnowledgeField(name="Renewal", instruction="When does it renew?")
    ]
    assert contracts.access == ["sales"]
    assert (customers.inherits_extraction, customers.inherits_access) == (True, True)
    assert [path for path, _ in layout.walk()] == [("Contracts",), ("Contracts", "Customers")]


def test_a_top_level_folder_cannot_inherit(tmp_path: Path) -> None:
    folder = tmp_path / "ai_knowledge" / "Loose"
    folder.mkdir(parents=True)
    (folder / "folder.yaml").write_text(yaml.safe_dump({"name": "Loose", "extraction": "inherit"}))
    with pytest.raises(ValueError, match="top-level"):
        CatalogDeclarativeAIKnowledge.load_from_disk(tmp_path)


def test_put_creates_the_tree_and_sends_the_documents(
    service: CatalogAIKnowledgeService, api: FakeAIKnowledge, tmp_path: Path
) -> None:
    result = service.put_declarative_ai_knowledge(_layout(tmp_path))

    assert result.folders_created == ["Contracts", "Contracts/Customers"]
    contracts = next(f for f in api.folders.values() if f["name"] == "Contracts")
    customers = next(f for f in api.folders.values() if f["name"] == "Customers")
    assert contracts["extraction"]["model"] == "gpt-4.1-mini"
    assert contracts["access"] == {"workspaceIds": ["sales"]}
    assert (customers["parentId"], customers["inheritExtraction"], customers["inheritAccess"]) == (
        contracts["id"],
        True,
        True,
    )
    assert "access" not in customers and "extraction" not in customers
    assert result.documents_uploaded == ["acme.md"]
    assert result.documents_imported == ["globex.pdf"]
    acme = next(d for d in api.documents.values() if d["filename"] == "acme.md")
    assert (acme["content"], acme["folderId"], acme["title"]) == (
        "ACME renews every January and pays net 30.",
        contracts["id"],
        "ACME contract",
    )
    assert api.imports == ["https://files.example.com/globex.pdf"]


def test_put_again_changes_nothing_and_moves_a_document(
    service: CatalogAIKnowledgeService, api: FakeAIKnowledge, tmp_path: Path
) -> None:
    layout = _layout(tmp_path)
    service.put_declarative_ai_knowledge(layout)
    api.calls.clear()

    again = service.put_declarative_ai_knowledge(layout)
    assert (again.folders_created, again.folders_updated, again.documents_uploaded, again.documents_imported) == (
        [],
        [],
        [],
        [],
    )
    assert not [c for c in api.calls if c.startswith(("POST", "PATCH", "PUT"))]

    customers = layout.folders[0].folders[0]
    acme = layout.folders[0].documents.pop(0)
    customers.documents.append(CatalogDeclarativeKnowledgeDocument(file=acme.file))
    moved = service.put_declarative_ai_knowledge(layout)
    assert moved.documents_moved == ["acme.md"]


def test_store_writes_the_tree_and_keeps_local_paths(service: CatalogAIKnowledgeService, tmp_path: Path) -> None:
    layout = _layout(tmp_path)
    service.put_declarative_ai_knowledge(layout)

    service.get_declarative_ai_knowledge().store_to_disk(tmp_path)

    contracts = tmp_path / "ai_knowledge" / "Contracts"
    assert yaml.safe_load((contracts / "folder.yaml").read_text())["access"] == {"workspaces": ["sales"]}
    assert yaml.safe_load((contracts / "Customers" / "folder.yaml").read_text()) == {
        "name": "Customers",
        "extraction": "inherit",
        "access": "inherit",
    }
    documents = yaml.safe_load((contracts / "documents.yaml").read_text())
    assert {"file": "acme.md", "title": "ACME contract", "path": "files/acme.md"} in documents
    assert (contracts / "files" / "acme.md").is_file()
    assert CatalogDeclarativeAIKnowledge.load_from_disk(tmp_path).walk()[1][0] == ("Contracts", "Customers")


def test_a_document_without_file_or_source_is_reported(service: CatalogAIKnowledgeService, tmp_path: Path) -> None:
    layout = CatalogDeclarativeAIKnowledge(
        folders=[
            CatalogDeclarativeKnowledgeFolder(
                name="Notes",
                extraction=CatalogDeclarativeKnowledgeExtraction(),
                documents=[CatalogDeclarativeKnowledgeDocument(file="gone.md")],
            )
        ]
    )
    assert service.put_declarative_ai_knowledge(layout).documents_missing == ["gone.md"]


def test_delete_missing_removes_folders_not_in_the_layout(
    service: CatalogAIKnowledgeService, api: FakeAIKnowledge, tmp_path: Path
) -> None:
    layout = _layout(tmp_path)
    service.put_declarative_ai_knowledge(layout)
    layout.folders[0].folders.clear()

    assert service.put_declarative_ai_knowledge(layout).folders_deleted == []
    assert service.put_declarative_ai_knowledge(layout, delete_missing=True).folders_deleted == ["Contracts/Customers"]
    assert [f["name"] for f in api.folders.values()] == ["Contracts"]


def test_a_large_file_goes_in_parts(service: CatalogAIKnowledgeService, api: FakeAIKnowledge, tmp_path: Path) -> None:
    video = tmp_path / "call.mp4"
    video.write_bytes(b"0123456789abcdefXYZ")
    progress: list[int] = []

    service.upload_document(video, on_progress=lambda sent, total: progress.append(sent))

    assert len([c for c in api.calls if "/parts/" in c]) == 3
    assert next(iter(api.documents.values()))["content"] == "0123456789abcdefXYZ"
    assert max(progress) == 19


def test_an_api_error_says_what_failed() -> None:
    client = MagicMock()
    client.request.return_value = _response(409, {"detail": "Folder 'A' already exists here"})
    with pytest.raises(AIKnowledgeApiError, match="409: Folder 'A' already exists here"):
        CatalogAIKnowledgeService(client).list_folders()
