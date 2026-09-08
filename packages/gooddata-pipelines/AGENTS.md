# gooddata-pipelines

A lifecycle-automation library on top of `gooddata-sdk`, covering three independent areas:
provisioning users, groups, permissions and workspaces; backing up and restoring workspace
metadata to local disk, S3 or Azure Blob; and extending an existing workspace's logical
data model with custom datasets and fields. Each area is entered through a small set of
manager or provisioner classes.

## Owns

- Provisioning flows for users, user groups, permissions, user data filters, and workspace
  hierarchies, with pydantic-validated inputs
- Backup and restore of workspace metadata across local, S3 and Azure Blob targets
- LDM extension for child workspaces

## Does NOT Own

- Core platform API and service abstractions → `gooddata-sdk`
- dbt metadata conversion → `gooddata-dbt`
- Flight RPC runtime → `gooddata-flight-server`

## Architecture

| Module | Role |
|---|---|
| `provisioning/` | `UserProvisioner`, `UserGroupProvisioner`, `PermissionProvisioner`, `WorkspaceProvisioner`, `UserDataFilterProvisioner` |
| `backup_and_restore/` | `BackupManager`, `RestoreManager`, plus `storage/` backends |
| `ldm_extension/` | `LdmExtensionManager` |
| `api/`, `utils/`, `logger/` | supporting HTTP, helpers and the log observer |

**Depends on**: `gooddata-sdk`, `pydantic`, `requests`, `boto3`, `azure-storage-blob`,
`azure-identity`.

### Construction

Managers and provisioners are built through classmethods, not `__init__`:

```python
provisioner = UserProvisioner.create(host, token)
# or
provisioner = UserProvisioner.create_from_profile(profile="default")
```

Each exposes a `.logger` (`LogObserver`) that a stdlib logger can `.subscribe()` to.

Provisioning is also reachable generically via `provision(data, workflow_type, host,
token)` driven by `WorkflowType`, intended for config- or orchestration-driven callers.

## Gotchas

**`full_load()` deletes.** Full load treats the list you pass as the complete desired
state: it diffs your input against what exists upstream and deletes everything not present
(`ids_to_delete = panther_id.difference(source_id)`). `incremental_load()` instead applies
only the explicit create/update/delete entries you provide and leaves everything else
alone. Confusing the two is the easiest way to write accidentally destructive code in this
repo — when in doubt, use incremental.

**`attrs` and `pyyaml` are used but not declared.** Both are imported throughout this
package yet appear in neither its dependencies; they arrive transitively through
`gooddata-sdk`. Fine today, silently broken if the SDK's dependency set ever changes.

**Backups are zip archives with a fixed internal layout.** A backup is written per
organization and workspace as `gooddata_layouts.zip`, containing the declarative layout
plus `user_data_filters/`, `filter_views/` and `automations/`. Restore expects exactly that
shape, so anything that changes the archive layout breaks restore of existing backups.

**LDM extension is additive, not a general LDM editor.** `LdmExtensionManager.process()`
adds custom datasets and fields validated through `CustomDatasetDefinition` /
`CustomFieldDefinition`, optionally merging into the existing LDM. It can also prune
previously-managed datasets carrying its `management_tag` when they are absent from the
current call. It has an optional relations-integrity check that reverts the change if it
would break more references than it fixes — do not remove that safety net casually.

**Backup batching, rate limiting and retry are configurable and load-bearing.**
`BackupRestoreConfig` carries `batch_size` and `api_calls_per_second`; a failed batch is
retried with exponential backoff up to `BackupSettings.MAX_RETRIES` before the whole run
aborts. These are the knobs for backup reliability and speed.

**`UserDataFilterProvisioner` is not wired into the generic path.** It is provisioned
directly rather than through `PROVISIONING_CONFIG` / `WorkflowType`, so do not assume
feature parity across provisioners.

**CSV input is backup-only.** `CSVReader.read_backup_csv` (a single-column list of
workspace ids) serves `BackupManager` only. Provisioning takes validated pydantic model
lists that the caller builds from whatever source they like.

**Input models forbid unknown keys and want real lists.** `UserFullLoad` and friends set
`extra="forbid"`, so a stray CSV column raises `ValidationError`, and `user_groups` is a
`list[str]` — a delimited CSV cell has to be split before validating. The models' only
alternate constructor is `from_sdk_obj`; there is no `from_list_of_dicts` helper, so the
caller builds the list. The README shows the working shape.

## Testing

Package-local pytest suites under `tests/`. Cloud storage targets are exercised with
`moto` rather than live buckets.
