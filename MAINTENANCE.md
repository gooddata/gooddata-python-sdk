# Repository maintenance and release

## How to release

Releases are fully automated by a single workflow dispatch. **Always run the
[Release](.github/workflows/bump-version.yaml) workflow from `master`** ("Use
workflow from: master") — the workflow definition is always master's (single
source of truth); the `base_branch` input selects which line's code it acts on.

> The Release workflow dispatches `build-release.yaml` and `netlify-deploy.yaml`
> from `master`, so those workflows must already exist on `master`. The first
> orchestrated release therefore has to run after this change is merged, not from
> a feature branch.

### Standard release (major / minor)
1. Run the [Release](.github/workflows/bump-version.yaml) workflow from `master` with `bump_type = major` or `minor` and `base_branch = master` (the default).
2. The run bumps the version, commits onto `master`, creates the long-lived `rel/X.Y.0` maintenance branch (for later patching), and pushes the `vX.Y.0` tag.
3. It then dispatches — from `master` — the downstream workflows:
   * [Build Python Package and Create Release](.github/workflows/build-release.yaml) builds all components, publishes them to PyPI, creates the GitHub release (marked latest), and notifies Slack.
   * [Netlify Deploy](.github/workflows/netlify-deploy.yaml) rebuilds and deploys the documentation (styling is taken from the `master` branch; see [generate.sh](scripts/generate.sh)).

> `patch` is intentionally rejected when `base_branch = master` — patches come from a `rel/X.Y.Z` maintenance branch (see below).

### Releasing an LTS patch (patching an old version)
Each version has its own maintenance branch `rel/X.Y.Z`. A minor/major release creates the line anchor `rel/X.Y.0`; each patch creates the next `rel/X.Y.(n+1)` from the line's latest branch, so all patch branches persist.

> If the line predates this release scheme it has no `rel/X.Y.0` branch yet — create it once from that line's tag before patching: `git branch rel/X.Y.0 vX.Y.0 && git push origin rel/X.Y.0`.

1. Merge the fix to `master` via a normal PR.
2. **Cherry-pick the fix onto the line's _latest_ `rel/X.Y.*` branch** (e.g. `rel/1.5.2`, not the anchor `rel/1.5.0`) and push it. This is what the next patch builds on — cherry-picking onto an older branch would silently drop the fix.
3. Run the [Release](.github/workflows/bump-version.yaml) workflow **from `master`** with `bump_type = patch` and `base_branch = rel/X.Y.0` (the anchor; the workflow auto-selects the line's highest `rel/X.Y.*` to build from).
4. The workflow builds from that latest branch, bumps the patch (e.g. `1.5.2` → `1.5.3`), and creates a new `rel/1.5.3` branch plus the `v1.5.3` tag. It does **not** touch `master` or the source branch.
5. It dispatches `build-release.yaml` from `master`, which publishes every component to PyPI and creates the GitHub release. Because the tag is not the highest semver, the release is marked **non-latest** and documentation is **not** redeployed. (Patching the current latest line is the exception — that tag *is* the highest, so it is marked latest and docs deploy.)

Subsequent patches repeat steps 1-4; each creates the next `rel/X.Y.Z` branch from the previous one, so patches chain and accumulate.

### Re-running a release (escape hatch)
To rebuild/republish an existing tag without bumping again, dispatch the build workflow directly from `master`:

```shell
gh workflow run build-release.yaml --ref master -f tag=vX.Y.Z -f make_latest=false
```


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
