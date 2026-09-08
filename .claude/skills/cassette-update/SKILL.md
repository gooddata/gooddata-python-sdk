---
name: cassette-update
description: Re-record VCR cassettes against the local docker-compose stack or staging. Use when a test fails on a recorded HTTP response, after a backend API change, or when adding a test that makes a new request. Triggers on "update cassettes", "re-record cassettes", "regenerate fixtures", "cassette mismatch", "CannotOverwriteExistingCassetteException".
disable-model-invocation: true
---

## When to use

A test fails because the recorded response no longer matches what the code sends or expects
— a changed request body, a new query parameter, a new field in the response, a
`CannotOverwriteExistingCassetteException`. The fix is to re-record, never to loosen the
assertion or point the test at a live host.

Cassettes live in `packages/*/tests/**/fixtures/*.yaml`.

## Decide the source first

**Local docker-compose** is the default. Use it for anything already supported by the demo
layout.

**Staging** is needed when the change depends on a backend that is newer than the images in
`docker-compose.yaml` — typically a field the local stack does not serve yet. Ask the user
which one applies if it is not obvious from the failure.

## Local stack

1. Preconditions, both easy to forget:

   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin \
     020413372491.dkr.ecr.us-east-1.amazonaws.com
   mkdir -p build && echo "<license-key>" > build/license
   ```

   The license key comes from the GoodData team; `auth-service` reads it from that path. Ask
   the user for it rather than inventing one.

2. Start the stack and wait for bootstrap — this takes minutes, and recording before it
   finishes produces cassettes full of errors:

   ```bash
   docker compose up -d
   docker compose wait metadata-organization-bootstrap data-loader create-ds layout-uploader
   ```

   `wait` blocks until those one-shot containers exit and returns their exit code. Do not use
   `docker compose logs -f` for this — it follows indefinitely and never returns, so watching
   for `Layout upload completed successfully!` that way hangs instead of continuing. To read
   what bootstrap did, run `docker compose logs layout-uploader` (no `-f`) afterwards.

   The API is then on `http://localhost:3000`.

3. `gooddata-fdw` tests only: `docker compose --profile fdw up -d`.

4. Delete only the cassettes you intend to re-record. `make remove-cassettes` deletes every
   cassette in the repo, which turns a one-test change into a repo-wide diff:

   ```bash
   rm packages/gooddata-sdk/tests/catalog/fixtures/<specific>.yaml
   ```

   Use `make remove-cassettes` (or the per-package `make -C packages/<name> remove-cassettes`)
   only when the change really is repo-wide, such as a normalization change in
   `tests-support`.

5. Re-run the affected tests to record:

   ```bash
   TEST_ENVS=py314 ADD_ARGS="-k <test-name>" make -C packages/<name> test
   ```

6. Review the diff before staging it. A re-recorded cassette should differ only in the ways
   the change explains — a diff touching timestamps, host names or ordering everywhere means
   normalization is not doing its job, and that is a bug in `tests-support/vcrpy_utils.py`,
   not something to commit around.

7. `docker compose down -v` when finished. Without `-v` the next run starts from dirty
   volumes.

## Staging

Requires `STAGING_ADMIN_TOKEN` and `STAGING_DS_PASSWORD`, from a gitignored `.env` at the
repo root or passed on the command line.

```bash
make clean-staging        # drop the previous run's data
make load-staging         # upload the demo layout
make test-staging TEST_ENVS=py314 ADD_ARGS="-k <test-name>"
```

Recording against staging still writes real cassettes — that is the point. Never bypass VCR
to make a staging run pass; a test that only works against a live host is a test nobody else
can run.

## Committing

Cassettes are large and numerous, so keep them in a commit of their own with a
`chore(tests):` or `chore(cassettes):` subject describing what changed in the API, rather
than mixing them into the code change. `risk: nonprod`.
