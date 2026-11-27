# (C) 2026 GoodData Corporation
"""AI Knowledge as files: one directory per folder, nested like the folders.

Layout under `gooddata_layouts/<organization id>/ai_knowledge/`::

    documents.yaml                  # documents not in any folder
    contracts/
      folder.yaml                   # name, description, purpose, extraction, access
      documents.yaml                # the folder's documents
      files/pricing.pdf             # optional: a document's file, referenced by `path`
      customers/
        folder.yaml                 # a subfolder: inherits extraction and access unless it sets its own
        documents.yaml

A directory is a folder when it holds `folder.yaml`; other directories (such as `files/`) are ignored. The folder's
name is the `name` in `folder.yaml`; the directory name is only a file-system safe form of it.

`folder.yaml`::

    name: Contracts
    description: Signed customer contracts
    purpose: documents                 # documents | business_context | investigations
    extraction:                        # or `inherit` in a subfolder
      model: gpt-4.1-mini              # optional: the LLM to use; the organization default otherwise
      summary_instruction: Summarise the commercial terms in three sentences.
      instruction: Focus on obligations of the customer.
      labels: [contract, legal]
      fields:
        - name: Renewal date
          instruction: When does the contract renew? ISO date.
    access: all                        # all | inherit | {workspaces: [sales, finance]}

`documents.yaml` lists documents, never their content::

    - file: pricing-policy.pdf         # the document's name in AI Knowledge
      title: Pricing policy            # optional
      path: files/pricing-policy.pdf   # optional: upload this file, relative to the folder's directory
      source: https://example.com/p.pdf  # optional: let the server import the file from this address

A document with neither `path` nor `source` is only described: it must already be in AI Knowledge.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Literal

from attrs import define, field

from gooddata_sdk.utils import read_layout_from_file, write_layout_to_file

AI_KNOWLEDGE_FOLDER = "ai_knowledge"
FOLDER_FILE = "folder.yaml"
DOCUMENTS_FILE = "documents.yaml"

INHERIT = "inherit"
ALL_WORKSPACES = "all"

FolderPurpose = Literal["documents", "business_context", "investigations"]


@define(kw_only=True)
class CatalogDeclarativeKnowledgeField:
    """A section the LLM writes for every document of a folder."""

    name: str
    instruction: str = ""


@define(kw_only=True)
class CatalogDeclarativeKnowledgeExtraction:
    """What the LLM writes about each document of a folder, and with which model."""

    model: str | None = None
    summary_instruction: str = ""
    instruction: str = ""
    labels: list[str] = field(factory=list)
    fields: list[CatalogDeclarativeKnowledgeField] = field(factory=list)

    def to_yaml(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if self.model:
            data["model"] = self.model
        if self.summary_instruction:
            data["summary_instruction"] = self.summary_instruction
        if self.instruction:
            data["instruction"] = self.instruction
        if self.labels:
            data["labels"] = list(self.labels)
        if self.fields:
            data["fields"] = [{"name": f.name, "instruction": f.instruction} for f in self.fields]
        return data

    @classmethod
    def from_yaml(cls, data: dict[str, Any] | None) -> CatalogDeclarativeKnowledgeExtraction:
        data = data or {}
        return cls(
            model=data.get("model") or None,
            summary_instruction=str(data.get("summary_instruction") or ""),
            instruction=str(data.get("instruction") or ""),
            labels=[str(label) for label in data.get("labels") or []],
            fields=[
                CatalogDeclarativeKnowledgeField(name=str(f["name"]), instruction=str(f.get("instruction") or ""))
                for f in data.get("fields") or []
            ],
        )

    def to_api(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "summaryInstruction": self.summary_instruction,
            "instruction": self.instruction,
            "labels": list(self.labels),
            "fields": [{"name": f.name, "instruction": f.instruction} for f in self.fields],
        }

    @classmethod
    def from_api(cls, data: dict[str, Any] | None) -> CatalogDeclarativeKnowledgeExtraction:
        data = data or {}
        return cls(
            model=data.get("model") or None,
            summary_instruction=str(data.get("summaryInstruction") or ""),
            instruction=str(data.get("instruction") or ""),
            labels=[str(label) for label in data.get("labels") or []],
            fields=[
                CatalogDeclarativeKnowledgeField(name=str(f["name"]), instruction=str(f.get("instruction") or ""))
                for f in data.get("fields") or []
            ],
        )


@define(kw_only=True)
class CatalogDeclarativeKnowledgeDocument:
    """A document of AI Knowledge, described by its name; its file is optional."""

    file: str
    title: str | None = None
    #: A local file to upload, relative to the directory of the folder's `documents.yaml`.
    path: str | None = None
    #: An https address the server imports the file from.
    source: str | None = None

    def to_yaml(self) -> dict[str, Any]:
        data: dict[str, Any] = {"file": self.file}
        for key in ("title", "path", "source"):
            if getattr(self, key):
                data[key] = getattr(self, key)
        return data

    @classmethod
    def from_yaml(cls, data: dict[str, Any] | str) -> CatalogDeclarativeKnowledgeDocument:
        if isinstance(data, str):
            return cls(file=data)
        return cls(
            file=str(data["file"]),
            title=data.get("title") or None,
            path=data.get("path") or None,
            source=data.get("source") or None,
        )


@define(kw_only=True)
class CatalogDeclarativeKnowledgeFolder:
    """A folder of AI Knowledge with its documents and subfolders.

    `extraction` None and `access` "inherit" take the parent's; a top-level folder cannot inherit.
    """

    name: str
    description: str | None = None
    purpose: FolderPurpose = "documents"
    extraction: CatalogDeclarativeKnowledgeExtraction | None = None
    #: "all", "inherit", or the ids of the workspaces that see the folder (with their child workspaces).
    access: str | list[str] = ALL_WORKSPACES
    documents: list[CatalogDeclarativeKnowledgeDocument] = field(factory=list)
    folders: list[CatalogDeclarativeKnowledgeFolder] = field(factory=list)
    #: The directory the folder was loaded from; local document paths are relative to it.
    directory: Path | None = field(default=None, eq=False)

    @property
    def inherits_extraction(self) -> bool:
        return self.extraction is None

    @property
    def inherits_access(self) -> bool:
        return self.access == INHERIT

    def walk(
        self, parent_path: tuple[str, ...] = ()
    ) -> list[tuple[tuple[str, ...], CatalogDeclarativeKnowledgeFolder]]:
        """This folder and every subfolder with its path of names, parents first."""
        path = (*parent_path, self.name)
        result = [(path, self)]
        for child in self.folders:
            result += child.walk(path)
        return result

    def folder_yaml(self) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name}
        if self.description:
            data["description"] = self.description
        if self.purpose != "documents":
            data["purpose"] = self.purpose
        data["extraction"] = INHERIT if self.extraction is None else self.extraction.to_yaml()
        data["access"] = self.access if isinstance(self.access, str) else {"workspaces": list(self.access)}
        return data

    @classmethod
    def from_folder_yaml(
        cls, data: dict[str, Any], *, top_level: bool, directory: Path | None = None
    ) -> CatalogDeclarativeKnowledgeFolder:
        if not data or not data.get("name"):
            raise ValueError(f"{directory or 'folder'}/{FOLDER_FILE} needs a name")
        extraction_data = data.get("extraction", {} if top_level else INHERIT)
        extraction = (
            None
            if extraction_data == INHERIT
            else CatalogDeclarativeKnowledgeExtraction.from_yaml(extraction_data or {})
        )
        access_data = data.get("access", ALL_WORKSPACES if top_level else INHERIT)
        access: str | list[str]
        if isinstance(access_data, dict):
            access = [str(w) for w in access_data.get("workspaces") or []]
        elif isinstance(access_data, list):
            access = [str(w) for w in access_data]
        elif access_data in (ALL_WORKSPACES, INHERIT):
            access = str(access_data)
        else:
            raise ValueError(f"{directory}/{FOLDER_FILE}: access is all, inherit or {{workspaces: [...]}}")
        if top_level and (extraction is None or access == INHERIT):
            raise ValueError(f"{directory}/{FOLDER_FILE}: a top-level folder has no parent to inherit from")
        return cls(
            name=str(data["name"]),
            description=data.get("description") or None,
            purpose=data.get("purpose") or "documents",
            extraction=extraction,
            access=access,
            directory=directory,
        )

    def store_to_disk(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        write_layout_to_file(directory / FOLDER_FILE, self.folder_yaml())
        _write_documents(directory, self.documents)
        _store_folders(directory, self.folders)

    @classmethod
    def load_from_disk(cls, directory: Path, *, top_level: bool) -> CatalogDeclarativeKnowledgeFolder:
        folder = cls.from_folder_yaml(
            read_layout_from_file(directory / FOLDER_FILE), top_level=top_level, directory=directory
        )
        folder.documents = _read_documents(directory)
        folder.folders = _load_folders(directory)
        return folder


@define(kw_only=True)
class CatalogDeclarativeAIKnowledge:
    """The AI Knowledge of an organization: its folder tree and the documents in no folder."""

    folders: list[CatalogDeclarativeKnowledgeFolder] = field(factory=list)
    documents: list[CatalogDeclarativeKnowledgeDocument] = field(factory=list)
    directory: Path | None = field(default=None, eq=False)

    def walk(self) -> list[tuple[tuple[str, ...], CatalogDeclarativeKnowledgeFolder]]:
        result: list[tuple[tuple[str, ...], CatalogDeclarativeKnowledgeFolder]] = []
        for folder in self.folders:
            result += folder.walk()
        return result

    def store_to_disk(self, organization_folder: Path) -> None:
        """Write the layout. Files of documents (`path`) and other files in the directories are kept."""
        directory = organization_folder / AI_KNOWLEDGE_FOLDER
        directory.mkdir(parents=True, exist_ok=True)
        _write_documents(directory, self.documents)
        _store_folders(directory, self.folders)

    @classmethod
    def load_from_disk(cls, organization_folder: Path) -> CatalogDeclarativeAIKnowledge:
        directory = organization_folder / AI_KNOWLEDGE_FOLDER
        if not directory.is_dir():
            raise ValueError(f"No AI Knowledge layout in {directory}")
        return cls(
            folders=_load_folders(directory, top_level=True), documents=_read_documents(directory), directory=directory
        )


def directory_name(name: str) -> str:
    """A file-system safe directory name for a folder name."""
    safe = re.sub(r"[^\w.-]+", "_", name.strip(), flags=re.UNICODE).strip("._") or "folder"
    return safe[:100]


def _store_folders(directory: Path, folders: list[CatalogDeclarativeKnowledgeFolder]) -> None:
    used: set[str] = set()
    keep: set[str] = set()
    for folder in folders:
        name = directory_name(folder.name)
        candidate, n = name, 2
        while candidate.lower() in used:
            candidate, n = f"{name}_{n}", n + 1
        used.add(candidate.lower())
        keep.add(candidate)
        folder.store_to_disk(directory / candidate)
    # A folder deleted since the last store: drop its layout files, keep any other file a user put there.
    for child in directory.iterdir():
        if child.is_dir() and child.name not in keep and (child / FOLDER_FILE).is_file():
            _remove_layout(child)


def _remove_layout(directory: Path) -> None:
    for child in directory.iterdir():
        if child.is_dir() and (child / FOLDER_FILE).is_file():
            _remove_layout(child)
    for name in (FOLDER_FILE, DOCUMENTS_FILE):
        (directory / name).unlink(missing_ok=True)
    if not any(directory.iterdir()):
        directory.rmdir()


def _load_folders(directory: Path, *, top_level: bool = False) -> list[CatalogDeclarativeKnowledgeFolder]:
    return [
        CatalogDeclarativeKnowledgeFolder.load_from_disk(child, top_level=top_level)
        for child in sorted(directory.iterdir())
        if child.is_dir() and (child / FOLDER_FILE).is_file()
    ]


def _write_documents(directory: Path, documents: list[CatalogDeclarativeKnowledgeDocument]) -> None:
    path = directory / DOCUMENTS_FILE
    # The server knows no local file or import address: keep the ones already written for the same document.
    known = {d.file.lower(): d for d in _read_documents(directory)}
    for document in documents:
        previous = known.get(document.file.lower())
        if previous is not None:
            document.path = document.path or previous.path
            document.source = document.source or previous.source
    if documents:
        write_layout_to_file(path, [d.to_yaml() for d in sorted(documents, key=lambda d: d.file.lower())])
    else:
        path.unlink(missing_ok=True)


def _read_documents(directory: Path) -> list[CatalogDeclarativeKnowledgeDocument]:
    path = directory / DOCUMENTS_FILE
    if not path.is_file():
        return []
    return [CatalogDeclarativeKnowledgeDocument.from_yaml(item) for item in read_layout_from_file(path) or []]
