# tests-support

Internal, unpublished workspace package holding the cross-package test infrastructure for
the SDK's cassette-based suites. Its main module configures vcrpy with a custom serializer
and request/response hooks that rewrite recorded cassettes so they are both portable
between environments and deterministic across runs. It also carries the two scripts that
reset and reseed a staging or local organization.

Consumed through the `test` dependency groups of `gooddata-sdk`, `gooddata-pandas` and
`gooddata-fdw`. **Not published to PyPI** — it is absent from `COMPONENTS` in the release
workflows.

## Owns

- `src/tests_support/vcrpy_utils.py` — the VCR configuration and all cassette
  normalization
- `src/tests_support/compare_utils.py`, `file_utils.py` — deep-comparison and JSON-loading
  helpers, used only by `gooddata-sdk`'s tests
- `clean_staging.py`, `upload_demo_layout.py` — invoked by the root `make clean-staging`
  and `make load-staging`
- `fixtures/` — the default demo layout, read by `upload_demo_layout.py` and mounted into
  the docker-compose stack

## Does NOT Own

- Runtime code for any customer-facing package
- Package-specific test scenarios, which stay in `packages/*/tests/`
- Core SDK API behavior → `gooddata-sdk`

## What normalization actually does

This is the part worth understanding before touching the module. On top of the obvious
header filtering it performs several distinct rewrites:

- **Request headers**: `authorization` and `user-agent` are filtered out entirely.
- **Response headers**: a fixed set of infrastructure headers is stripped; `DATE`,
  `X-GDC-CANCEL-TOKEN` and `X-GDC-TRACE-ID` are blanked to a placeholder rather than
  removed, so their presence still round-trips.
- **Dynamic values in bodies and URIs**: `createdAt` timestamps, `traceId`,
  `authenticationId` / `authId`, `bearerToken`, `cacheId` and query-duration values are
  regex-substituted. Execution and export result hashes become indexed placeholders
  (`EXECUTION_NORMALIZED_1`, or format-named like `EXPORT_NORMALIZED_CSV`), re-indexed from
  cassette content at serialize time.
- **Secrets in request bodies**: `password`, `token`, `url`, `username`, `privateKey`,
  `client_secret` and `private_key_passphrase` are stripped before body *matching* — this
  affects the comparison, not the stored body.
- **Environment identity**: staging hostnames, organization ids and database credentials
  are replaced with canonical localhost/`default` values, which is what lets a cassette
  recorded against staging replay in CI.
- **Sorting is a narrow allowlist, not general.** Only `referenceProperties`,
  `workspaceDataFilterColumns`, `workspaceDataFilterReferences`, `edges` and `userGroups`
  are sorted (recursively within that scope). Everything else deliberately keeps the
  server's original order, so replay matches recording — a code comment says so
  explicitly. Do not "fix" an unsorted array by widening this list without understanding
  why the order is being preserved.

## Gotchas

**Editing this module requires recreating the consumers' tox environments, or your change
silently does nothing.** `tests_support` is installed as a wheel into each consumer's `.tox`
environment, so a reused environment keeps serving the old code. Clear the build cache, then
have tox rebuild:

```bash
uv cache clean tests-support --force
RECREATE_ENVS=1 make -C packages/<name> test     # RECREATE_ENVS=1 adds tox -r
```

Do that for every consumer whose suite you rely on, not just one. The module's own docstring
names `rm -rf packages/gooddata-sdk/.tox` alone, which is incomplete: `gooddata-pandas` and
`gooddata-fdw` install the wheel too, so clearing only the SDK's environment leaves those two
suites running the previous normalization.

**A normalization change is a repo-wide re-record event.** Placeholders are re-indexed from
cassette content at serialize time, so changing the regexes or the sort allowlist changes
the bytes written into every cassette in `gooddata-sdk`, `gooddata-pandas` and
`gooddata-fdw`. There is no per-package opt-out.

**`configure_normalization()` must run before any recording.** State is process-global and
built once per session; there is a hard `RuntimeError` guard for calling it too late.

**`vcrpy` and `deepdiff` are imported but not declared here.** This package depends only on
`orjson`, `pyyaml` and `requests`; the test libraries come from whichever consuming
package's `test` group is active. `deepdiff` is only present via `gooddata-sdk`, so
`compare_utils.deep_eq` would `ImportError` if used from the pandas or fdw suites. This is
also why the package cannot be tested standalone as-is.

**Not every consumer uses every module.** All three consumers import `vcrpy_utils`; only
`gooddata-sdk` imports `compare_utils` and `file_utils`. So a `vcrpy_utils` change needs
re-verification across all three, while a `compare_utils` change does not.

**The staging scripts hardcode a default host.** Both default to a specific
`python-sdk-dex` staging host, overridable via the `HOST`, `HEADER_HOST` and `TOKEN`
environment variables — override rather than editing them in place.

## Conventions

Add a helper here only once at least two packages need it.
