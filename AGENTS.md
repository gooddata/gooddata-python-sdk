# gooddata-python-sdk

Monorepo for the GoodData Cloud Python SDK: nine published distributions plus shared test
helpers, managed as one `uv` workspace on a single shared version number.

## Tech Stack

- **Python** — `>=3.10` is the published floor; develop on 3.14. Tests run py310–py314.
- **uv** workspace (`uv ~= 0.12`) — one lock file at the root covers every package.
- **ruff** — lint and format. Line length 120, Google docstring convention.
- **ty** — type checking. Not mypy; `make type-check` runs `uv run ty check`.
- **tox + pytest** — per-package test matrix. **vcrpy** records HTTP against a real backend.
- **pre-commit** — ruff, copyright headers, `uv lock`, gitlint.

Every package carries the same version, bumped together by `tbump`. See `MAINTENANCE.md`
for the release process and `CONTRIBUTING.md` for first-time setup.

## Repository Layout

| Path | Contents |
|---|---|
| `packages/gooddata-*` | The published packages — each has its own `AGENTS.md` |
| `packages/tests-support` | Shared test helpers. Workspace member, **not** published |
| `gooddata-api-client/` | Generated from the OpenAPI spec — never hand-edit |
| `schemas/` | OpenAPI specs the client is generated from |
| `scripts/` | Client generation, copyright, docs builders, release helpers |
| `docs/` | Hugo site for the public documentation |
| `docker-compose.yaml` | Full local GoodData stack, needed to record VCR cassettes |

## Build Commands

Run from the workspace root; every target also exists per package via
`make -C packages/<name> <target>`.

| Target | Effect |
|---|---|
| `make dev` | `uv sync --all-groups` + install pre-commit and commit-msg hooks |
| `make format` / `make format-fix` | ruff format, check-only / rewriting |
| `make lint` / `make lint-fix` | ruff check, report-only / autofixing |
| `make type-check` | `ty check` (alias: `make types`) |
| `make test` | tox → pytest across every supported Python version |
| `make test-ci` | the same suite inside the CI Docker images |

Test runs are controlled by environment variables rather than flags:

```bash
TEST_ENVS=py314 make test                    # one interpreter instead of all five
ADD_ARGS="-k test_catalog" make test         # pass args through to pytest
RECREATE_ENVS=1 make test                    # force tox to rebuild its venvs
```

Never invoke bare `python` or `pip` — this is a `uv` workspace, so use `uv run`, and prefer
the `make` targets, which already wrap it.

## Validation Workflow

Run this before reporting a change complete, and again before pushing. Do not predict the
result — run the commands and read the output.

### 1. Work out what you touched

| Changed | Validate with |
|---|---|
| `packages/<name>/**` | the per-package sequence below, once for each package touched |
| `scripts/**` or root config | `make format-fix lint-fix` from the workspace root |
| `scripts/docs/**` | also `make test-docs-scripts` |
| `gooddata-api-client/**` | nothing — see the note below |

The generated client is excluded from `make lint`, `make format` and pre-commit, and no
`ty` target covers it. Do not point ruff at it directly to "check" it —
`ruff check gooddata-api-client` bypasses the exclude and reports around 17k errors in
generated code. There is nothing to fix there; regenerate instead.

### 2. Before committing — format, lint, types

```bash
make -C packages/<name> format-fix lint-fix type-check
```

Fix the first failure before looking at anything after it; a later step's output is
meaningless once an earlier one has failed.

### 3. Before pushing — add the tests

```bash
TEST_ENVS=py314 make -C packages/<name> test
```

`py314` is the fastest useful signal. Drop `TEST_ENVS` to run the full py310–py314 matrix
the way CI does — slow, and worth it only when the change could be version-sensitive.

### 4. If a shared package changed, validate a consumer

`gooddata-sdk` is a dependency of every other package except `gooddata-flight-server` and
`tests-support`, and `gooddata-flight-server` is a dependency of `gooddata-flexconnect`. A
change to either means validating at least one consumer as well, not just the package you
edited.

### Rules

- The `*-fix` targets rewrite files, and whatever they rewrite has to be committed. CI runs
  the check-only `make format` and `make lint`, which fail on anything left unformatted.
- Never describe a change as validated without having run these commands in this session.
  If you skipped a step because it was slow, say which one you skipped.
- `make test` is verbose. Capture it and watch a tail:
  `make -C packages/<name> test 2>&1 | tee /tmp/sdk-test.log | tail -40`. On failure read
  the log — do not re-run the command to see more output.
- A test failing on a recorded HTTP response is a cassette to re-record, never an assertion
  to loosen. See the cassette section above.
- Do not add a `# type: ignore`, a ruff `noqa`, or an entry to a `ty` allowed-unresolved
  list to get a step to pass. Fix the cause, or say why you cannot.

CI runs `make format`, `make lint`, `make type-check`, `make test-ci` and
`make test-docs-scripts` — the check-only variants are what gate the merge. Nothing in CI
validates commit messages; that is local only, via the commit-msg hook.

## Testing

### VCR cassettes

Most tests replay recorded HTTP traffic through [vcrpy] rather than calling a live backend.
Cassettes live in `packages/*/tests/**/fixtures/*.yaml` and are by far the highest-churn
files in the repository — treat re-recording as a routine, deliberate step, not an accident.

Recording requires the local stack from `docker-compose.yaml`:

```bash
aws ecr get-login-password | docker login --username AWS --password-stdin \
  020413372491.dkr.ecr.us-east-1.amazonaws.com
mkdir -p build && echo "<license-key>" > build/license   # auth-service reads this
docker compose up -d
docker compose wait layout-uploader                      # blocks until bootstrap finishes
make remove-cassettes                                    # or delete just the ones you need
make test
```

`docker compose wait` returns when the one-shot bootstrap container exits, and its exit code
is the bootstrap's. Do not substitute `docker compose logs -f` to watch for the "Layout upload
completed successfully!" line — `logs -f` follows indefinitely and never returns, so it hangs
rather than proceeding to the next step.

The API is then at `http://localhost:3000`, admin token `YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz`.
`gooddata-fdw` tests need one extra service: `docker compose --profile fdw up -d`.

The data-loader runs with `--no-schema-versioning` on purpose. Without it, schema and
fixture names get hash suffixes and the recorded cassettes stop being reproducible.

When a backend change alters a response, **re-record the cassette** — never loosen the
assertion or bypass VCR to make a test pass against a live host. A cassette is the
snapshot that lets everyone else run the suite offline; skipping it moves the failure
onto the next person. Full fixture inventory, including the layouts that some catalog
tests *replace* rather than read, is documented at the end of `CONTRIBUTING.md`.

### Staging tests

`GD_TEST_ENV=staging` points the suite at a shared deployment instead of docker-compose,
which is how cassettes and the generated client get refreshed against a real backend.
Locally these need `STAGING_ADMIN_TOKEN` and `STAGING_DS_PASSWORD`, read from a gitignored
`.env` at the root or passed on the command line:

```bash
make clean-staging      # drop the previous run's data
make load-staging       # upload the demo layout
make test-staging       # TEST_ENVS= and ADD_ARGS= work here too
```

On a PR, the same run is triggered by the `test-staging` label or a `/test-staging`
comment. Only one staging run executes at a time and it does not cancel in progress.

The CI workflow currently exports only `TOKEN`, not the two names the Makefile requires, so
a triggered run fails at its first step; recent runs have been skipped rather than executed,
which is why nobody has hit it. `CONTRIBUTING.md` has the details. Until that is fixed,
staging runs are effectively local-only.

### Testing practices

Extend the existing tests when a change is incremental — a new field, enum value or
property belongs in the fixture and assertions that already cover that round trip. A new
test file is for genuinely new behavior. Cover null/empty inputs, boundary values and the
error paths, not only the happy one.

## Generated API Client

`gooddata-api-client/` is generated by the OpenAPI generator and must never be hand-edited;
the next regeneration would silently discard the change. To refresh it:

```bash
make api-client                 # download specs from localhost:3000, then generate
make api-client STAGING=1       # download from staging instead
make api-client-local           # regenerate from the specs already in schemas/
```

Regeneration usually needs a follow-up commit adapting `gooddata-sdk` to the new surface.
Generator config and custom templates are under `.openapi-generator/`; that directory's
README covers version upgrades and per-client invocation.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

jira: <TICKET-ID>
risk: nonprod|low|high
```

- **type** — one of `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`,
  `revert`, `ci`, `build`.
- **scope** — optional, but when given it must come from the allowed list in `.gitlint`:
  a package name, or `ci` / `docs` / `repo` for changes that span the workspace. Add new
  packages to that list when they appear.
- **subject** — imperative mood, no trailing period, whole line at most 70 characters.
- **body** — required, and it is where the rationale for the change belongs, never in a
  source comment. Wrap at 72 characters.
- **jira** — required, lowercase. A ticket id, or `jira: trivial` when none applies.
- **risk** — lowercase. `nonprod` for tests/docs/CI-only, `low` for a routine change to
  shipped code, `high` for breaking or otherwise risky behavior changes.

Keep `jira:` and `risk:` on consecutive lines in the message's last paragraph. A blank line
above a trailing `Co-Authored-By:` orphans them from the trailer block, which is why the
hook rejects that shape.

gitlint runs at the commit-msg stage, installed by `make dev`. It checks the type, the
scope against its allowed list, that a body is present, and both trailers. It does **not**
check subject length — that one is convention, not enforcement.

One logical change per commit. Address review feedback inside the commit whose scope it
belongs to — `git commit --fixup=<sha>` then `git rebase -i --autosquash <sha>^` — rather
than appending a trailing `fix` commit.

## PR Format

Title follows the commit subject rules. The body needs a summary, a test plan, and the
same risk assessment as the commit.

## Cross-Cutting Constraints

### Working in this repo

- Search before inventing. Similar code almost certainly exists — do not design a second
  way to do something the repo already does.
- Do not generate, rename or refactor anything that was not asked for.
- Never create summary or documentation markdown files unless they were requested.
- Break large tasks into independently reviewable units.

### Python conventions

- **Absolute imports only.** `from gooddata_sdk.client import GoodDataSdk`, never
  `from .client import ...` — relative imports break IDE navigation.
- **All imports at the top of the file**, after the docstring and any
  `from __future__ import annotations`. ruff's `PLC0415` enforces this.
- Annotate every function and any local whose type is not obvious, especially empty
  collection initializers. Type dataclasses fully.
- Treat YAML/JSON loader output as `Any`: guard with `isinstance`, narrow once, reuse the
  narrowed value. Prefer a `TypedDict` or dataclass when the schema is known.
- Prefer one authoritative `cast(...)` over repeated inline casts, and
  `typing.assert_never` for exhaustive branches.
- Google-style docstrings on public APIs.
- Aim to be `ty`-clean on the first pass rather than writing then fixing.

### Comments

A comment explains what the code means to someone who never saw the diff. Rationale for a
change goes in the commit body or PR description.

- Do not narrate the change. `used to`, `no longer`, `previously`, `before this change`,
  `regression`, and pasted benchmark numbers all rot the moment the code moves on, and
  `git blame` already answers the question better.
- Do not put a JIRA key, ticket URL or PR number in a comment, docstring or test name. The
  one exception is a forward-looking `# TODO(ABC-1234):` for work still outstanding.
- Do write down a live constraint the next editor must not break.

### Dependencies

1. Internal packages first — `gooddata-sdk` for platform access, `gooddata-api-client` for
   raw endpoints, `tests-support` for shared test helpers.
2. Then the already-approved stack: pandas, attrs/cattrs, requests, pydantic, pyarrow,
   pytest, vcrpy — at the versions the lock file resolves.
3. Anything new or unfamiliar: search the web for its current API before proposing it. Your
   training data is likely stale, and this repo pins narrow ranges.

Internal cross-package dependencies use `~={current_version}`, which `tbump` rewrites on
release. Add a dependency to the package's `pyproject.toml`, then run `uv lock`.

### Adding a new package

Three entries in the root `pyproject.toml` — `[project].dependencies`,
`[tool.uv.sources]`, and `[tool.uv.workspace].members` (listed explicitly, not globbed, so
a stray directory cannot break every `uv` command). Then add it to `COMPONENTS` in both
`.github/workflows/dev-release.yaml` and `build-release.yaml`, to the Codecov file list in
`rw-python-tests.yaml`, and to `scopes` in `.gitlint`.

## Documentation

The public site is Hugo, under `docs/`. `make new-docs` serves it locally. Method pages are
generated from docstrings via the `{{< python "..." >}}` shortcode, so a new public method
needs its own `.md` page plus a link in the sibling `_index.md`. `CONTRIBUTING.md` has the
worked example.

## Package Index

Each package's `AGENTS.md` states what it owns and, importantly, what it does not.

- `packages/gooddata-sdk` — core SDK, `gdc` CLI, Analytics-as-Code, declarative layouts
- `packages/gooddata-pandas` — Series and DataFrame access on top of the SDK
- `packages/gooddata-dbt` — dbt metadata to GoodData semantic model
- `packages/gooddata-pipelines` — provisioning, backup/restore, LDM extension workflows
- `packages/gooddata-flight-server` — reusable Arrow Flight RPC server runtime
- `packages/gooddata-flexconnect` — custom data source framework on the Flight server
- `packages/gooddata-fdw` — PostgreSQL foreign data wrapper, built on multicorn
- `packages/gooddata-eval` — `gd-eval` CLI for evaluating the GoodData AI agent
- `packages/tests-support` — shared VCR, comparison and file helpers for the test suites

[vcrpy]: https://vcrpy.readthedocs.io/
