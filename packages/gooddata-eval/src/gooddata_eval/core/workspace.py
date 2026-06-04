# (C) 2026 GoodData Corporation
"""Resolve and activate the workspace LLM provider/model via the GoodData SDK."""

from dataclasses import dataclass, field

from gooddata_sdk import CatalogWorkspaceSetting, GoodDataSdk

# Default id used only when creating the setting for the first time. The backend
# enforces a single setting per *type* (ACTIVE_LLM_PROVIDER), and an existing
# setting may have been created with any id (e.g. by the UI), so reads and
# updates must locate it by type rather than by this id.
_SETTING_ID = "activeLlmProvider"
_SETTING_TYPE = "ACTIVE_LLM_PROVIDER"


@dataclass
class ActiveLlmProvider:
    provider_id: str
    default_model_id: str


@dataclass
class ResolvedModel:
    provider_id: str
    model_id: str
    switched: bool  # True when activation changed the workspace's active provider
    provider_name: str = field(default="")  # human-readable name, empty if not available


class ModelResolutionError(Exception):
    """Raised when the requested/default provider+model cannot be resolved for a workspace."""


def active_provider_content(provider_id: str, model_id: str) -> dict:
    """The `content` payload of the workspace's ACTIVE_LLM_PROVIDER setting."""
    return {"id": provider_id, "type": "llmProvider", "defaultModelId": model_id}


def resolve_model(requested: str | None, active: ActiveLlmProvider | None) -> tuple[str, str]:
    """Return (provider_id, model_id) for the default path (no explicit provider).

    - requested is None  -> use the workspace's current active model.
    - requested is given -> attach it to the workspace's current provider.

    Raises ModelResolutionError when no active provider exists to derive/attach a model.
    """
    if active is None:
        raise ModelResolutionError(
            "Workspace has no active LLM provider configured. "
            "Configure a model in the workspace, or pass --model/--provider."
        )
    model_id = requested or active.default_model_id
    if not model_id:
        raise ModelResolutionError("Could not determine a model id for the workspace.")
    return active.provider_id, model_id


def select_provider_and_model(
    requested_model: str | None,
    requested_provider: str | None,
    active: ActiveLlmProvider | None,
    providers_models: dict[str, list[str]],
) -> tuple[str, str]:
    """Pick (provider_id, model_id) given an already-resolved provider id and available models.

    `providers_models` maps provider id -> model ids it offers.
    `requested_provider` must already be resolved to an id (see _resolve_provider_ref).
    """
    known = sorted(providers_models)

    if requested_provider is not None:
        if requested_provider not in providers_models:
            raise ModelResolutionError(
                f"LLM provider '{requested_provider}' not found. Known providers: {', '.join(known) or '(none)'}."
            )
        offered = providers_models.get(requested_provider) or []
        model_id = requested_model
        if model_id is None:
            if active is not None and active.provider_id == requested_provider and active.default_model_id:
                model_id = active.default_model_id
            else:
                raise ModelResolutionError(
                    f"Pass --model when selecting provider '{requested_provider}' "
                    f"(it offers: {', '.join(sorted(offered)) or '(none listed)'})."
                )
        if offered and model_id not in offered:
            raise ModelResolutionError(
                f"Model '{model_id}' is not offered by provider '{requested_provider}'. "
                f"Available: {', '.join(sorted(offered))}."
            )
        return requested_provider, model_id

    if requested_model is not None:
        if active is not None and requested_model in (providers_models.get(active.provider_id) or []):
            return active.provider_id, requested_model
        candidates = sorted(pid for pid, models in providers_models.items() if requested_model in (models or []))
        if len(candidates) == 1:
            return candidates[0], requested_model
        if len(candidates) > 1:
            raise ModelResolutionError(
                f"Model '{requested_model}' is offered by multiple providers: {', '.join(candidates)}. "
                "Pass --provider to choose one."
            )
        available = sorted({m for models in providers_models.values() for m in (models or [])})
        raise ModelResolutionError(
            f"Model '{requested_model}' is not offered by any configured provider. "
            f"Available models: {', '.join(available) or '(none)'}."
        )

    return resolve_model(None, active)


def _resolve_provider_ref(ref: str, provider_info: dict[str, dict]) -> str:
    """Resolve a provider name-or-id to its id.

    Tries exact id match first, then case-insensitive name match.
    Raises ModelResolutionError with a human-readable list (name + id) when not found.
    """
    if ref in provider_info:
        return ref

    ref_lower = ref.lower()
    name_matches = [pid for pid, info in provider_info.items() if (info.get("name") or "").lower() == ref_lower]
    if len(name_matches) == 1:
        return name_matches[0]
    if len(name_matches) > 1:
        raise ModelResolutionError(
            f"Multiple providers share the name '{ref}': {', '.join(name_matches)}. "
            "Pass the provider id to disambiguate."
        )

    known = sorted(f"{info.get('name') or pid} ({pid})" for pid, info in provider_info.items())
    raise ModelResolutionError(
        f"LLM provider '{ref}' not found by id or name. Known providers: {', '.join(known) or '(none)'}."
    )


class WorkspaceModelController:
    """Reads and sets the workspace's active LLM provider/model through the GoodData SDK."""

    def __init__(self, host: str, token: str, workspace_id: str):
        self._workspace_id = workspace_id
        self._sdk = GoodDataSdk.create(host, token)

    def _active_setting(self) -> CatalogWorkspaceSetting | None:
        """Find the workspace's ACTIVE_LLM_PROVIDER setting by type (id may vary)."""
        for setting in self._sdk.catalog_workspace.list_workspace_settings(self._workspace_id):
            if setting.setting_type == _SETTING_TYPE:
                return setting
        return None

    def get_active(self) -> ActiveLlmProvider | None:
        setting = self._active_setting()
        if setting is None:
            return None
        content = setting.content or {}
        return ActiveLlmProvider(
            provider_id=content.get("id", ""),
            default_model_id=content.get("defaultModelId", ""),
        )

    def _provider_info(self) -> dict[str, dict]:
        """Map provider id -> {name, models} from the SDK."""
        providers = self._sdk.catalog_organization.list_llm_providers()
        result: dict[str, dict] = {}
        for p in providers:
            attrs = p.attributes
            models = (attrs.models if attrs else None) or []
            result[p.id] = {
                "name": (attrs.name if attrs else None) or p.id,
                "models": [m.id for m in models],
            }
        return result

    def all_provider_models(self) -> dict[str, list[str]]:
        """Map each configured LLM provider id to the model ids it offers."""
        return {pid: info["models"] for pid, info in self._provider_info().items()}

    def activate(self, provider_id: str, model_id: str) -> None:
        # Reuse the existing setting's id so create_or_update performs an UPDATE.
        # Creating a second ACTIVE_LLM_PROVIDER setting (under a different id)
        # would be rejected by the backend with HTTP 409 (one per type).
        existing = self._active_setting()
        setting = CatalogWorkspaceSetting(
            id=existing.id if existing is not None else _SETTING_ID,
            setting_type=_SETTING_TYPE,
            content=active_provider_content(provider_id, model_id),
        )
        self._sdk.catalog_workspace.create_or_update_workspace_setting(self._workspace_id, setting)

    def resolve_and_activate(self, requested_model: str | None, requested_provider: str | None = None) -> ResolvedModel:
        """Resolve provider+model (by name or id), activate them, and report what was chosen."""
        active = self.get_active()
        if requested_model is None and requested_provider is None:
            provider_id, model_id = resolve_model(None, active)
            provider_name = ""
        else:
            info = self._provider_info()
            providers_models = {pid: d["models"] for pid, d in info.items()}
            resolved_provider = None
            if requested_provider is not None:
                resolved_provider = _resolve_provider_ref(requested_provider, info)
            provider_id, model_id = select_provider_and_model(
                requested_model, resolved_provider, active, providers_models
            )
            provider_name = info.get(provider_id, {}).get("name", "")
        switched = active is None or provider_id != active.provider_id
        self.activate(provider_id, model_id)
        return ResolvedModel(
            provider_id=provider_id,
            model_id=model_id,
            switched=switched,
            provider_name=provider_name,
        )
