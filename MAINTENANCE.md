# Repository maintenance and release

## How to release
* manually run [Bump version & trigger release](.github/workflows/bump-version.yaml) workflow
* after the previous workflow finishes, dispatch the GitHub workflow [Netlify Deploy](.github/workflows/netlify-deploy.yaml) on the `master` branch (takes ~15 minutes)
  * The styling of the documentation is taken from the `master` branch. For more details see [generate.sh](scripts/generate.sh).
* after the previous workflow finishes, push tag
  * the version should be the same as the one in [Bump version & trigger release](.github/workflows/bump-version.yaml) workflow log
  * checkout latest master branch and tag it `vX.Y.Z`
  * push the tag to the gooddata/gooddata-python-sdk repository (e.g. `git push <remote> vX.Y.Z`)


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
