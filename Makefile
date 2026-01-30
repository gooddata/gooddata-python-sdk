# (C) 2021 GoodData Corporation
# list all full paths to files and directories in CWD containing "gooddata", filter out ones ending by "client"
NO_CLIENT_GD_PROJECTS_ABS = $(filter-out %client, $(wildcard $(CURDIR)/packages/*gooddata*))
# for each path, take only the base name of the path
NO_CLIENT_GD_PROJECTS_DIRS = $(foreach dir, $(NO_CLIENT_GD_PROJECTS_ABS), $(notdir $(dir)))
# TODO: replace API_VERSION in the future by call to API
API_VERSION="v1"
# Generate from localhost
BASE_URL="http://localhost:3000"
# Generate from PROD
# BASE_URL="https://demo-cicd.cloud.gooddata.com"
URL="${BASE_URL}/api/${API_VERSION}/schemas"

include ci_tests.mk

# Common command components
RUFF = .venv/bin/ruff

all:
	echo "Nothing here yet."

.PHONY: dev
dev:
	uv sync --all-groups
	.venv/bin/pre-commit install

.PHONY: lint
lint:
	$(RUFF) check .

.PHONY: lint-fix
lint-fix:
	$(RUFF) check . --fix

.PHONY: format
format:
	$(RUFF) format --check .

.PHONY: format-fix
format-fix:
	$(RUFF) format .

.PHONY: format-diff
format-diff:
	$(RUFF) format --diff .


define download_client
    curl "${URL}/$(1)" | jq --sort-keys > schemas/gooddata-$(1)-client.json
endef

define generate_client
	./scripts/generate_client.sh gooddata-$(1)-client -f "/local/schemas/gooddata-$(1)-client.json"
endef

.PHONY: api-client
api-client: download
	rm -f schemas/gooddata-api-client.json
	cat schemas/gooddata-*.json | jq -S -s 'reduce .[] as $$item ({}; . * $$item) + { tags : ( reduce .[].tags as $$item (null; . + $$item) | unique_by(.name) ) }' | sed '/\u0000/d' > "schemas/gooddata-api-client.json"
	$(call generate_client,api)

.PHONY: download
download:
	$(call download_client,afm)
	$(call download_client,metadata)
	$(call download_client,scan)
	$(call download_client,"export")
	$(call download_client,automation)

.PHONY: type-check
type-check:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C packages/$${project} type-check || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: types
types: type-check

.PHONY: test
test:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C packages/$${project} test || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: release
release:
	if [ -z "$(VERSION)" ]; then echo "Usage: 'make release VERSION=X.Y.Z'"; false; else \
	uv run tbump $(VERSION) --no-tag --no-push ; fi

.PHONY: release-ci
release-ci:
	if [ -z "$(VERSION)" ]; then echo "Usage: 'make release-ci VERSION=X.Y.Z'"; false; else \
	uv run tbump $(VERSION) --only-patch --non-interactive && uv lock ; fi

.PHONY: check-copyright
check-copyright:
	uv run ./scripts/check_copyright.py FOLDER

.PHONY: docs
docs:
	RESULT=0; \
	for project in gooddata-fdw gooddata-pandas; do $(MAKE) -C packages/$${project} $@ || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: remove-cassettes
remove-cassettes:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C packages/$${project} $@ || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: new-docs
new-docs:
	cd docs; \
	npm install; \
	hugo server
