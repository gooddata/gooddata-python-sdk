# (C) 2026 GoodData Corporation
"""AI Knowledge of the organization as a declarative layout: folders, their settings, and their documents.

`store_declarative_ai_knowledge` writes the folder tree to YAML (see `declarative_model`); edit it, add documents
with a local `path` or a `source` address, and `load_and_put_declarative_ai_knowledge` makes AI Knowledge match.
Document content never goes into the YAML: a file is uploaded in parts (any size) or imported by the server.
"""

from __future__ import annotations

import mimetypes
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
from attrs import define, field

from gooddata_sdk.catalog.ai_knowledge.declarative_model import (
    ALL_WORKSPACES,
    CatalogDeclarativeAIKnowledge,
    CatalogDeclarativeKnowledgeDocument,
    CatalogDeclarativeKnowledgeExtraction,
    CatalogDeclarativeKnowledgeFolder,
)
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.client import GoodDataApiClient

_BASE = "/api/v1/ai/organization/knowledge"
_PAGE_SIZE = 500
_PART_ATTEMPTS = 3


class AIKnowledgeApiError(RuntimeError):
    """AI Knowledge refused a request."""

    def __init__(self, response: requests.Response) -> None:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        super().__init__(f"{response.request.method} {response.url} -> HTTP {response.status_code}: {detail}")
        self.status_code = response.status_code


@define(kw_only=True)
class CatalogAIKnowledgeSyncResult:
    """What `put_declarative_ai_knowledge` changed."""

    folders_created: list[str] = field(factory=list)
    folders_updated: list[str] = field(factory=list)
    folders_deleted: list[str] = field(factory=list)
    documents_uploaded: list[str] = field(factory=list)
    documents_imported: list[str] = field(factory=list)
    documents_moved: list[str] = field(factory=list)
    documents_missing: list[str] = field(factory=list)
    """Listed in the layout without a `path` or `source`, and not in AI Knowledge."""


class CatalogAIKnowledgeService(CatalogServiceBase):
    """Folders and documents of the organization's AI Knowledge. Every call needs organization admin rights."""

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)

    # Declarative layout

    def get_declarative_ai_knowledge(self) -> CatalogDeclarativeAIKnowledge:
        """The folder tree with settings and the list of documents. Files are not downloaded."""
        folders = self.list_folders()
        by_id = {f["id"]: f for f in folders}
        nodes = {f["id"]: _folder_from_api(f) for f in folders}
        layout = CatalogDeclarativeAIKnowledge()
        for folder in sorted(folders, key=lambda f: str(f["name"]).lower()):
            node = nodes[folder["id"]]
            parent_id = folder.get("parentId")
            if parent_id and parent_id in nodes:
                nodes[parent_id].folders.append(node)
            else:
                layout.folders.append(node)
        for document in self.list_documents():
            item = CatalogDeclarativeKnowledgeDocument(file=document["filename"], title=document.get("title") or None)
            folder_id = document.get("folderId")
            if folder_id and folder_id in by_id:
                nodes[folder_id].documents.append(item)
            else:
                layout.documents.append(item)
        return layout

    def store_declarative_ai_knowledge(self, layout_root_path: Path = Path.cwd()) -> None:
        """Write the layout to `<root>/gooddata_layouts/<organization>/ai_knowledge/`."""
        self.get_declarative_ai_knowledge().store_to_disk(self.layout_organization_folder(layout_root_path))

    def load_declarative_ai_knowledge(self, layout_root_path: Path = Path.cwd()) -> CatalogDeclarativeAIKnowledge:
        return CatalogDeclarativeAIKnowledge.load_from_disk(self.layout_organization_folder(layout_root_path))

    def load_and_put_declarative_ai_knowledge(
        self,
        layout_root_path: Path = Path.cwd(),
        *,
        replace_documents: bool = False,
        delete_missing: bool = False,
    ) -> CatalogAIKnowledgeSyncResult:
        """Make AI Knowledge match the layout stored under `layout_root_path`. See `put_declarative_ai_knowledge`."""
        return self.put_declarative_ai_knowledge(
            self.load_declarative_ai_knowledge(layout_root_path),
            replace_documents=replace_documents,
            delete_missing=delete_missing,
        )

    def put_declarative_ai_knowledge(
        self,
        layout: CatalogDeclarativeAIKnowledge,
        *,
        replace_documents: bool = False,
        delete_missing: bool = False,
    ) -> CatalogAIKnowledgeSyncResult:
        """Create and update folders as in the layout, then upload, import or move the documents it lists.

        Folders are matched by their path of names. A document is matched by its file name: a missing one is
        uploaded from its `path` or imported from its `source`; one in another folder is moved. With
        `replace_documents`, documents that have a `path` or `source` are sent again even when they exist.

        With `delete_missing`, folders not in the layout are deleted with their documents and subfolders. Documents
        are never deleted otherwise.
        """
        result = CatalogAIKnowledgeSyncResult()
        existing = {tuple(f.get("path") or [f["name"]]): f for f in self.list_folders()}
        ids: dict[tuple[str, ...], str] = {}

        for path, folder in layout.walk():
            parent_id = ids.get(path[:-1]) if len(path) > 1 else None
            body = _folder_to_api(folder, parent_id)
            current = existing.get(path)
            if current is None:
                created = self._json("POST", "/folders", json=body)
                ids[path] = created["id"]
                result.folders_created.append("/".join(path))
            else:
                ids[path] = current["id"]
                if _folder_differs(current, body):
                    self._json("PATCH", f"/folders/{current['id']}", json=body)
                    result.folders_updated.append("/".join(path))

        documents = {d["filename"].lower(): d for d in self.list_documents()}
        work: list[tuple[CatalogDeclarativeKnowledgeDocument, str | None, Path | None]] = [
            (d, None, layout.directory) for d in layout.documents
        ]
        for path, folder in layout.walk():
            work += [(d, ids[path], folder.directory) for d in folder.documents]
        for document, folder_id, directory in work:
            current = documents.get(document.file.lower())
            has_content = bool(document.path or document.source)
            if current is not None and not (replace_documents and has_content):
                if (current.get("folderId") or None) != folder_id:
                    self._json("PATCH", f"/documents/{current['id']}", json={"folderId": folder_id})
                    result.documents_moved.append(document.file)
                if document.title and document.title != current.get("title"):
                    self._json("PATCH", f"/documents/{current['id']}", json={"title": document.title})
                continue
            if document.path:
                local = Path(document.path)
                if not local.is_absolute() and directory is not None:
                    local = directory / local
                self.upload_document(
                    local,
                    filename=document.file,
                    folder_id=folder_id,
                    title=document.title,
                    replace=current is not None,
                )
                result.documents_uploaded.append(document.file)
            elif document.source:
                self.import_document(
                    document.source,
                    filename=document.file,
                    folder_id=folder_id,
                    title=document.title,
                    replace=current is not None,
                )
                result.documents_imported.append(document.file)
            else:
                result.documents_missing.append(document.file)

        if delete_missing:
            wanted = set(ids)
            stale = [p for p in existing if p not in wanted and p[:-1] in wanted | {()}]
            for path in sorted(stale, key=len, reverse=True):
                self._request("DELETE", f"/folders/{existing[path]['id']}", params={"documents": "delete"})
                result.folders_deleted.append("/".join(path))
        return result

    # Folders and documents

    def list_folders(self) -> list[dict[str, Any]]:
        return list(self._json("GET", "/folders").get("folders", []))

    def list_documents(self) -> list[dict[str, Any]]:
        """Organization-level documents, every page."""
        documents: list[dict[str, Any]] = []
        token: str | None = None
        while True:
            params: dict[str, Any] = {"size": _PAGE_SIZE}
            if token:
                params["pageToken"] = token
            page = self._json("GET", "/documents", params=params)
            documents += page.get("documents", [])
            token = page.get("nextPageToken")
            if not token:
                return documents

    def upload_document(
        self,
        path: Path,
        *,
        filename: str | None = None,
        folder_id: str | None = None,
        title: str | None = None,
        content_type: str | None = None,
        replace: bool = False,
        parallel_parts: int = 3,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> dict[str, Any]:
        """Upload a local file of any size in parts. Returns the queued document (id, filename, processingStatus)."""
        name = filename or path.name
        size = path.stat().st_size
        upload = self._json(
            "POST",
            "/uploads",
            json={
                "filename": name,
                "contentType": content_type or mimetypes.guess_type(name)[0] or "application/octet-stream",
                "size": size,
                "title": title,
                "folderId": folder_id,
                "replace": replace,
            },
        )
        upload_id, part_size, part_count = upload["uploadId"], upload["partSize"], upload["partCount"]
        sent = [0]

        def send(number: int) -> None:
            with path.open("rb") as fh:
                fh.seek((number - 1) * part_size)
                data = fh.read(part_size)
            for attempt in range(_PART_ATTEMPTS):
                response = self._request("PUT", f"/uploads/{upload_id}/parts/{number}", data=data, check=False)
                if response.status_code < 400:
                    break
                if response.status_code < 500 or attempt == _PART_ATTEMPTS - 1:
                    raise AIKnowledgeApiError(response)
                time.sleep(2**attempt)
            sent[0] += len(data)
            if on_progress is not None:
                on_progress(sent[0], size)

        try:
            with ThreadPoolExecutor(max_workers=max(1, parallel_parts)) as pool:
                list(pool.map(send, range(1, part_count + 1)))
            return self._json("POST", f"/uploads/{upload_id}/complete")
        except Exception:
            self._request("DELETE", f"/uploads/{upload_id}", check=False)
            raise

    def import_document(
        self,
        url: str,
        *,
        filename: str | None = None,
        folder_id: str | None = None,
        title: str | None = None,
        replace: bool = False,
    ) -> dict[str, Any]:
        """Let the server copy a file from an https address on a public host. Returns the queued document."""
        return self._json(
            "POST",
            "/imports",
            json={"url": url, "filename": filename, "folderId": folder_id, "title": title, "replace": replace},
        )

    def put_transcript(self, document_id: str, path: Path) -> None:
        """Add a WebVTT or SubRip transcript to an audio or video document, which makes it searchable."""
        with path.open("rb") as fh:
            self._request("PUT", f"/documents/{document_id}/transcript", files={"file": (path.name, fh, "text/vtt")})

    # HTTP

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        check: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        response = self._client.request(method, f"{_BASE}{endpoint}", **kwargs)
        if check and response.status_code >= 400:
            raise AIKnowledgeApiError(response)
        return response

    def _json(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        response = self._request(method, endpoint, **kwargs)
        return response.json() if response.content else {}


def _folder_from_api(data: dict[str, Any]) -> CatalogDeclarativeKnowledgeFolder:
    access = data.get("access")
    top_level = not data.get("parentId")
    return CatalogDeclarativeKnowledgeFolder(
        name=data["name"],
        description=data.get("description") or None,
        purpose=data.get("purpose") or "documents",
        extraction=None
        if data.get("inheritExtraction") and not top_level
        else CatalogDeclarativeKnowledgeExtraction.from_api(data.get("extraction")),
        access="inherit"
        if data.get("inheritAccess") and not top_level
        else (ALL_WORKSPACES if access is None else list(access.get("workspaceIds") or [])),
    )


def _folder_to_api(folder: CatalogDeclarativeKnowledgeFolder, parent_id: str | None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "name": folder.name,
        "description": folder.description,
        "purpose": folder.purpose,
        "parentId": parent_id,
        "inheritExtraction": folder.inherits_extraction and parent_id is not None,
        "inheritAccess": folder.inherits_access and parent_id is not None,
    }
    if folder.extraction is not None:
        body["extraction"] = folder.extraction.to_api()
    if not folder.inherits_access:
        body["access"] = None if folder.access == ALL_WORKSPACES else {"workspaceIds": list(folder.access)}
    return body


def _folder_differs(current: dict[str, Any], body: dict[str, Any]) -> bool:
    for key in ("description", "purpose", "parentId", "inheritExtraction", "inheritAccess"):
        if (current.get(key) or None) != (body.get(key) or None):
            return True
    if "extraction" in body and CatalogDeclarativeKnowledgeExtraction.from_api(
        current.get("extraction")
    ) != CatalogDeclarativeKnowledgeExtraction.from_api(body["extraction"]):
        return True
    return "access" in body and (current.get("access") or None) != (body["access"] or None)
