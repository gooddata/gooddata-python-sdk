# Documentation Generation

This directory contains Python scripts that generate the API reference pages and
pre-render method documentation for the GoodData Python SDK documentation site.

## How it works

The docs site is built with Hugo. API content is generated in three steps:

1. **`griffe_builder.py`** — performs static AST analysis of the `gooddata_sdk`
   and `gooddata_pandas` source trees using [griffe](https://mkdocstrings.github.io/griffe/),
   producing a `data.json` file with class/function/property metadata and parsed
   Google-style docstrings. No package installation required.
   Falls back to the legacy **`json_builder.py`** (runtime introspection via
   `inspect`) for older branches that don't have the griffe builder.

2. **`python_ref_builder.py`** — reads `data.json` and `api_spec.toml`, then
   generates markdown files with pre-rendered HTML for each module, class, and
   function. Jinja2 templates in `templates/` replicate the output of the former
   Hugo shortcodes. Also exports a `links.json` mapping type names to their
   generated page URLs.

3. **`method_page_renderer.py`** — reads `data.json` and `links.json`, then
   pre-renders the 136 method documentation pages (e.g., `scan_sql.md`,
   `list_workspaces.md`). For each page with an `api_ref` frontmatter key, it
   generates the signature, description, parameters table, and returns table
   from the docstring, with type names hyperlinked to the API reference pages.
   Hand-written `## Example` sections are preserved.

The generated markdown files contain Hugo front matter and pre-rendered HTML.
Hugo serves them as-is without needing shortcodes, `data.json`, or `links.json`.

## Method page format

Method pages use an `api_ref` frontmatter key to specify which class method to
render from:

```yaml
---
title: "scan_sql"
linkTitle: "scan_sql"
weight: 210
superheading: "catalog_data_source."
api_ref: "CatalogDataSourceService.scan_sql"
---
```

Everything between the frontmatter and the first `## Example` heading is
auto-generated. Only the example section is hand-written.

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
  installs master's `script-requirements.txt`, runs `griffe_builder.py` +
  `python_ref_builder.py` + `method_page_renderer.py` via
  `generate-single-version.sh`.
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

## Data flow

```
griffe_builder.py (static AST analysis, no imports needed)
  -> data.json

python_ref_builder.py (reads data.json + api_spec.toml)
  -> links.json (type name -> URL mapping)
  -> versioned_docs/{version}/api-reference/  (pre-rendered API ref pages)
  -> versioned_docs/{version}/pandas/         (pre-rendered pandas ref pages)

method_page_renderer.py (reads data.json + links.json)
  -> versioned_docs/{version}/**/*.md (pre-rendered method pages with linked types)

Hugo (pure static build, no shortcode processing needed)
  -> public/ (final site)
```

## Local development

Build and serve docs locally using Docker:

```bash
cd docs
docker build -t python-sdk-docs -f Dockerfile ..
docker run --rm -p 1313:1313 python-sdk-docs
# Open http://localhost:1313/latest/
```

Or manually:

```bash
cd docs
# Generate data.json (from repo root, no package install needed)
uv run --with griffe python3 ../scripts/docs/griffe_builder.py \
    --search-path ../packages/gooddata-sdk/src \
    --search-path ../packages/gooddata-pandas/src \
    --output data.json \
    gooddata_sdk gooddata_pandas

# Generate API reference pages + links.json
mkdir -p versioned_docs/latest
cp -r content/en/latest/* versioned_docs/latest/
uv run --with jinja2 --with toml --with attrs --with cattrs \
    python3 ../scripts/docs/python_ref_builder.py \
    api_spec.toml data.json latest versioned_docs --export-links links.json

# Pre-render method pages
python3 ../scripts/docs/method_page_renderer.py \
    data.json versioned_docs/latest --links-json links.json

# Serve
hugo server -e production
```

## Key files

| File | Purpose |
|------|---------|
| `griffe_builder.py` | Static AST analysis of SDK source into `data.json` |
| `json_builder.py` | Legacy runtime introspection fallback (older branches) |
| `python_ref_builder.py` | Generates API reference markdown + exports `links.json` |
| `method_page_renderer.py` | Pre-renders method pages from `api_ref` frontmatter |
| `migrate_method_pages.py` | One-time migration script (added `api_ref` to 136 pages) |
| `templates/*.html.j2` | Jinja2 templates for API reference pages |
| `tests/` | Unit tests for all scripts |
| `../script-requirements.txt` | Python dependencies |
| `../../docs/api_spec.toml` | Maps package names to output directories |
| `../../docs/*_template.md` | Markdown front matter templates (module/class/function) |

## Running tests

```bash
uv run --with griffe --with pytest --with jinja2 --with toml --with attrs --with cattrs \
    pytest scripts/docs/tests/ -v
```
