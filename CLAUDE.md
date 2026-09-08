@AGENTS.md

## Claude-Specific

### Skills

Named workflows live in `.claude/skills/`:

- `/cassette-update` — bring up the local stack and re-record VCR cassettes
- `/api-client-regen` — regenerate `gooddata-api-client` and adapt the SDK to it
- `/commit` — stage-aware commit with the `jira:` and `risk:` trailers

### Running long commands

The output handling in AGENTS.md ("Validation Workflow" → Rules) applies to every
long-running command here, not just `make test` — `docker compose up` and `make api-client`
both produce hundreds of lines. Capture to a log, watch a tail, read the log on failure.

While iterating, scope the run down rather than widening the output:
`TEST_ENVS=py314 ADD_ARGS="-k <name>" make -C packages/<name> test`.

### Multi-repo

The API specs this repo generates from are produced by `gdc-nas`, and cassettes are
regenerated when its API changes:

```bash
claude --add-dir ../gdc-nas
```
