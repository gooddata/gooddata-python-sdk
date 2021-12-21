# (C) 2021 GoodData Corporation
# list all full paths to files and directories in CWD containing "gooddata", filter out ones ending by "client"
NO_CLIENT_GD_PROJECTS_ABS = $(filter-out %client, $(wildcard $(CURDIR)/*gooddata*))
# for each path, take only the base name of the path
NO_CLIENT_GD_PROJECTS_DIRS = $(foreach dir, $(NO_CLIENT_GD_PROJECTS_ABS), $(notdir $(dir)))

include ci_tests.mk

all:
	echo "Nothing here yet."

.PHONY: dev
dev:
	python3.9 -m venv .venv --upgrade-deps
	.venv/bin/pip3 install -r dev-requirements.txt
	.venv/bin/pre-commit install

.PHONY: lint
lint:
	flake8 .

.PHONY: format
format:
	black --check .
	isort --check .

.PHONY: format-diff
format-diff:
	black --diff .
	isort --diff .

.PHONY: format-fix
format-fix:
	black .
	isort .

.PHONY: clients
clients: afm-client metadata-client scan-client

.PHONY: afm-client
afm-client:
	scripts/generate_afm_client.sh

.PHONY: metadata-client
metadata-client:
	scripts/generate_metadata_client.sh

.PHONY: scan-client
scan-client:
	scripts/generate_scan_client.sh

.PHONY: mypy
mypy:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C $${project} $@ || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: test
test:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C $${project} test || RESULT=$$?; done; \
	exit $$RESULT

.PHONY: release
release:
	if [ -z "$(VERSION)" ]; then echo "Usage: 'make release VERSION=X.Y.Z'"; false; else \
	tbump $(VERSION) --no-tag --no-push ; fi

.PHONY: check-copyright
check-copyright:
	./scripts/check_copyright.py FOLDER

.PHONY: docs
docs:
	RESULT=0; \
	for project in $(NO_CLIENT_GD_PROJECTS_DIRS); do $(MAKE) -C $${project} $@ || RESULT=$$?; done; \
	exit $$RESULT
