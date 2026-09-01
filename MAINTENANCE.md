# Repository maintenance and release

## How to release
Manually run the [Bump version & trigger release](.github/workflows/bump-version.yaml) workflow and pick the
bump type. That is the whole release.

The workflow bumps the version, creates the `rel/X.Y.Z` branch, merges it to `master`, and pushes the tag
`vX.Y.Z`. That tag push triggers two workflows in parallel:

* [Build Python Package and Create Release](.github/workflows/build-release.yaml) — builds every component,
  creates the GitHub release, publishes to PyPI, and posts to `#releases`.
* [Netlify Deploy](.github/workflows/netlify-deploy.yaml) — builds and publishes the documentation
  (takes ~15 minutes, so the packages reach PyPI well before the docs go live).

The styling of the documentation is taken from the `master` branch. For more details see
[generate.sh](scripts/generate.sh).

### Recovering a stuck release
Both downstream workflows key off the tag, so a release that stalled can be resumed by hand:

* if the tag was never pushed, check out the `Release X.Y.Z` commit on `master`, tag it `vX.Y.Z`, and push the
  tag to the gooddata/gooddata-python-sdk repository (e.g. `git push <remote> vX.Y.Z`)
* if only the documentation failed, dispatch [Netlify Deploy](.github/workflows/netlify-deploy.yaml) manually;
  it does not need the tag

The tag has to be pushed with a personal access token. GitHub does not trigger workflows from pushes made with
the default `GITHUB_TOKEN`, so a tag pushed by a workflow using it would silently start nothing.

## How to patch an already released version
Use this whenever a release must contain a specific fix and *not* everything currently on `master` — whether
that is an old line (1.60 while `master` is at 1.73) or the newest one.

Do **not** use the [Bump version & trigger release](.github/workflows/bump-version.yaml) workflow for this. Its
last step is `git checkout master && git merge`, which would drag the old code and version numbers onto
`master`. Its `patch` bump type means "release master as a patch", not "patch the released line".

Only the tagging is automated; the rest is manual by nature.

**Prerequisite:** the fix is already merged to `master`. The patch branch is never merged back, so this is what
keeps the fix from being lost in the next release.

1. **Pick the base and the new version.** List what the line already has with
   `git branch -rl '<remote>/rel/1.60.*'`. The base is the newest of them, and the new version increments the
   patch component **of that base** — so `rel/1.60.0` gives `1.60.1`, but if the line was already patched to
   `rel/1.60.2` the next one is `1.60.3`. The steps below use `1.60.1`; substitute your version throughout.

2. **Create the release branch first**, so the fix has somewhere to be reviewed into:
   ```bash
   git fetch <remote>
   # Branch from the base chosen in step 1, not blindly from X.Y.0 -- on an already-patched
   # line that would be rel/1.60.2, and starting from 1.60.0 would drop the earlier fixes.
   git checkout -b rel/1.60.1 <remote>/rel/1.60.0
   git push <remote> rel/1.60.1
   ```

3. **Cherry-pick the fix through a pull request:**
   ```bash
   git checkout -b fix/backport-1.60 rel/1.60.1
   git cherry-pick <sha-on-master>
   git push <remote> fix/backport-1.60
   ```
   Open the PR against `rel/1.60.1`. The [pre-merge pipeline](.github/workflows/pre-merge.yaml) runs because it
   triggers on `rel/**`. Merge once it is green.

4. **Bump the version on the release branch.** These commands mirror the *Install dependencies* through
   *Bump version in codebase* steps of [bump-version.yaml](.github/workflows/bump-version.yaml) — if that
   workflow gains or reorders a step, update this block with it:
   ```bash
   git checkout rel/1.60.1 && git pull
   uv sync --only-group release --locked
   uv run python ./scripts/bump_doc_dependencies.py 1.60.1
   make release-ci VERSION=1.60.1
   git add -A && git commit -m "Release 1.60.1"
   git push <remote> rel/1.60.1
   ```
   `git add -A` rather than `commit -am`, matching the workflow, so a newly created file is not dropped. On an
   older line `uv sync --locked` can fail if the lock file predates the current uv; re-lock if so.

5. **Tag it.** This is the only trigger; everything after it is automatic:
   ```bash
   git tag v1.60.1
   git push <remote> v1.60.1
   ```

The release is then built and published exactly like any other. Two things differ, and
[release-tag-checks](.github/actions/release-tag-checks/action.yaml) handles both: the GitHub release does not
take the "Latest" badge from the newest version, and the documentation is not rebuilt — the docs build checks
out the triggering tag, so publishing from one would put an outdated site live.

> **A tag runs the workflows as they exist *at that tag*, not on master.** Release lines branched before the
> release automation was added therefore run their own older copies, in which `make_latest` is hardcoded to
> `true`. Before tagging such a line, cherry-pick `.github/workflows/build-release.yaml` and
> `.github/actions/release-tag-checks/` onto `rel/X.Y.Z` — otherwise the patch takes the "Latest" badge, which
> also changes what `GET /releases/latest` returns. If you only notice afterwards, untick "Set as the latest
> release" on the GitHub release by hand. Those older copies have no tag trigger on the docs workflow, so the
> documentation is safe either way.

### What the documentation will show
The docs site keeps the four newest release branches, sorted by `major.minor`, and a section is named after the
`major.minor` only. Consequences worth knowing before someone goes looking:

* A patch never publishes its own documentation — the deploy is gated on the tag being on master. `rel/1.72.1`
  does take over the `1.72` section from `rel/1.72.0`, but only at the next deploy from master: the following
  release, or a manual dispatch of [Netlify Deploy](.github/workflows/netlify-deploy.yaml) if you need it
  sooner.
* Both branches still occupy a slot of the four, so one patch inside the window drops the site from four
  displayed versions to three.
* Patching an old line (`rel/1.60.1` while `master` is at 1.73) falls outside the window entirely and never
  appears in the docs.

### How-to dev release
To publish current master as a dev release version, use [Dev release from master](.github/workflows/dev-release.yaml) GitHub workflow.

### Errors that may appear

* Github release could not be created as the same release already exists.
  Possible Solutions:
   - Delete the release and retry.
   - It's highly probable that also Pypi release exists, so it's easier to bump version and try with higher version tag
* Pypi upload failed with file already exists.
  The file with the same name ever existed, it does not matter that it no longer exists
  (see [the linkded document](https://test.pypi.org/help/#file-name-reuse))
  Possible solutions:
  - It's desirable to have a release in consistent state (all packages of the given version updoaded in pypi),
    so in case there was partial success, please upload rest of packages manually as described in
    [packaging documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)
    Credentials were distributed though LastPass
  - Another solution is to bump version and create new release

## readthedocs integration
Repository is integrated with readthedocs pages. Currently, we have set up three separate documentation projects:
- gooddata-sdk
- gooddata-pandas
- gooddata-fdw

The setup requires special configuration in project advanced settings:
- Field requirements file - set to `<project>/docs/requirements.txt`
- Field Python configuration file - set to `<project>/docs/conf.py`

Project environment variable `CWD_TO_ROOT_RELATIVE` must be set to `.` with public access.

### Webhooks to github
User used to create project integration must have admin rights to the repository and OAuth to organization must be
permitted. If any of it is missing, readthedocs will not be able to set up webhooks in the repository. Once webhooks
are created, user admin rights to repository can and should be revoked.

### Webhooks alternative
Even if webhooks are currently in use, they could be replaced with github action https://github.com/dfm/rtds-action.
Github action together with github-vault integration would make possible to maintain readthedocs setup without help of
other teams.
