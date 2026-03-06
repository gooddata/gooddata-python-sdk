# Documentation Generation

This directory contains Python scripts that generate the API reference pages for
the GoodData Python SDK documentation site.

## How it works

The docs site is built with Hugo. API reference pages are generated in two steps:

1. **`json_builder.py`** — introspects the installed `gooddata_sdk` and
   `gooddata_pandas` packages using `inspect`, producing a `data.json` file with
   class/function/property metadata and parsed docstrings.
2. **`python_ref_builder.py`** — reads `data.json` and `api_spec.toml`, then
   generates markdown files with pre-rendered HTML for each module, class, and
   function. Jinja2 templates in `templates/` replicate the output of the former
   Hugo shortcodes, but at build time instead of at Hugo render time.

The generated markdown files contain Hugo front matter (title, linkTitle, weight)
and a `CONTENT` block with the full HTML. Hugo serves them as-is without needing
shortcodes, `data.json`, or `links.json`.

## Workflows

There are three documentation deployment workflows, in order of
preference:

### 1. V2 parallel workflow (`netlify-deploy-v2.yaml`) — recommended

Triggered manually via `workflow_dispatch`.

```
discover-versions ──> generate-version (matrix, parallel) ──> build-and-deploy
```

- `discover-versions.sh` finds the latest N release branches.
- Each version runs in its own runner: checks out the version's SDK packages,
  installs master's `script-requirements.txt`, runs `json_builder.py` +
  `python_ref_builder.py` via `generate-single-version.sh`.
- Per-version results are cached by `(scripts hash + templates hash + branch SHA)`.
- `assemble-versions.sh` merges all version artifacts, promotes the highest
  numbered version to `/latest`, then Hugo builds the final site.
- Deploys as a Netlify **draft** (no `--prod`).

### 2. Legacy single-job workflow (`netlify-deploy.yaml`) — production

Triggered manually via `workflow_dispatch`.

- Uses `hugo-build-versioned-action` which downloads `generate.sh` from master.
- `generate.sh` runs all versions sequentially in one job.
- Deploys to Netlify with `--prod`.

### 3. PR preview (`netlify-deploy-preview.yaml`)

Triggered automatically on PRs that change `docs/**`.

- Only builds the current branch's docs content (no multi-version).
- Uses the simpler `hugo-build-action` (no API reference generation).
- Deploys to a Netlify preview URL (`preview-{PR}--{site}.netlify.app`).

## Local development

Build and serve docs locally using Docker:

```bash
cd docs
docker build -t python-sdk-docs -f Dockerfile ..
docker run --rm -p 1313:1313 python-sdk-docs
# Open http://localhost:1313/latest/
```

## Key files

| File | Purpose |
|------|---------|
| `json_builder.py` | Introspects SDK packages into `data.json` |
| `python_ref_builder.py` | Generates markdown + HTML from `data.json` |
| `templates/*.html.j2` | Jinja2 templates (replicate old Hugo shortcodes) |
| `tests/test_python_ref_builder.py` | Unit tests (`make test-docs-scripts`) |
| `../script-requirements.txt` | Python dependencies for both scripts |
| `../../docs/api_spec.toml` | Maps package names to output directories |
| `../../docs/*_template.md` | Markdown front matter templates (module/class/function) |

## Running tests

```bash
make test-docs-scripts
```
