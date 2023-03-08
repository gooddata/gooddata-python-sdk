# Repository maintenance and release

## How to release documentation for new versions

* Edit redirects in `./docs/layouts/index.redir`
* Add the new version to the version picker in `./docs/config/production/params.toml`
* Create a new branch named `rel/X.Y.Z`
  * This branch now hosts the content for documentation of the X.Y.Z version. Any changes to the content in the branch will be public.
* Dispatch the Github workflow `netlify-deploy` on the `master` branch
  * The styling of the documentation is taken from the `master` branch. For more details see `./scripts/generate.sh` and `netlify-deploy` workflow.

## How to release new version

* Run `make release VERSION=X.Y.Z`
* Create a pull request with the latest commit with bumped versions
* Ask for merge of a pull request.
* Once it is merged:
  * Checkout latest master and tag it `vX.Y.Z`
* Push the tag to the gooddata/gooddata-python-sdk repository (e.g. `git push <remote> vX.Y.Z`)

### Releasing Alpha versions
To publish current master as an alpha version, use `Release master as alpha` github workflow where you need to specify
desired alpha version. **No validity checks are performed**.

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
