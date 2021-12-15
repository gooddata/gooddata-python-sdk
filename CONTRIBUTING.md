# How to contribute

* Checkout repository
* Run `make dev`
* Create your awesome changes
* Test everything is ok by running `make test-ci` (light-weight `make test` is also available)
* Create a pull request

# How to release new version

* Run `make release VERSION=X.Y.Z`
* Create pull request with latest commit with bumped versions
* Ask for merge of pull request. Once it is merged:
* Checkout latest master tag it vX.Y.Z
* Push the tag to master branch (`git push --tags`)
