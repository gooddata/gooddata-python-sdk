---
name: api-client-regen
description: Regenerate the gooddata-api-client package from the OpenAPI specs and adapt the SDK to the result. Use after a backend API change lands, or when the client is missing an endpoint, model or field. Triggers on "regenerate api client", "regen client", "openapi spec changed", "update api-client".
disable-model-invocation: true
---

## When to use

The backend added or changed an endpoint, model or field and `gooddata-api-client/` does not
have it yet. The client is generated — never hand-edit it, because the next regeneration
discards the edit silently.

## Regenerate

Pick the spec source:

```bash
make api-client              # download specs from localhost:3000 (docker compose), then generate
make api-client STAGING=1    # download from staging instead — usual choice for a new API
make api-client-local        # regenerate from the specs already in schemas/, no download
```

`make api-client` is `download` followed by `_api-client-generate`. The download step writes
one `schemas/gooddata-<api>-client.json` per API surface (afm, metadata, scan, export,
automation, result), then the generate step merges them into
`schemas/gooddata-api-client.json` and runs the OpenAPI generator in Docker.

Both the merged spec and the generated code are committed.

## After regenerating

1. **Check what moved.** `git diff --stat gooddata-api-client/` — a regeneration that only
   touches version strings and `README.md` means the spec did not actually change and the
   commit is noise.

2. **Adapt the SDK.** A regeneration that changes model shapes usually breaks
   `gooddata-sdk`, which wraps them. Run at minimum:

   ```bash
   make -C packages/gooddata-sdk type-check
   TEST_ENVS=py314 make -C packages/gooddata-sdk test
   ```

   Watch for renamed model classes and changed required/optional fields — those are the two
   that surface as type errors rather than test failures.

3. **Expect cassette churn.** If the request shape changed, recorded cassettes no longer
   match. Use the `/cassette-update` skill; do not loosen assertions.

4. **Tag renames are breaking.** The generator turns each OpenAPI tag into an `*Api` class
   name (tag `AI` → `AIApi`). A tag renamed upstream in `gdc-nas` renames a public class here
   even if nothing in `gooddata-sdk` imports it — call it out for the changelog.

## Commit shape

Keep the regeneration and the SDK adaptation as separate commits, matching the existing
history:

```
chore(api-client): regenerate against staging
fix(gooddata-sdk): adapt to regenerated api-client
```

Generator configuration and custom templates live in `.openapi-generator/`; its README
covers generator version upgrades.
