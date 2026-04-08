# (C) 2021 GoodData Corporation

# Common command components (run from workspace root, scoped to this package)
ROOT_DIR = ../..
RUFF = ./.venv/bin/ruff
# ty needs uv run (unlike ruff) because it resolves imports from installed packages
TY = uv run ty
PKG_PATH = packages/$(CURR_DIR_BASE_NAME)

# Optional: specify Python version (e.g. make test TEST_PYTHON=3.12)
ifdef TEST_PYTHON
  UV_PYTHON_FLAG = --python $(TEST_PYTHON)
  REPORT_TAG = py$(subst .,,$(TEST_PYTHON))
else
  UV_PYTHON_FLAG =
  REPORT_TAG = default
endif

# linting and formatting tools have configuration in root dir to support pre-commit - use it
# ruff uses root directory to have the same per-file-ignores config parameter for all packages
CURR_DIR_BASE_NAME = $(notdir $(CURDIR))

.PHONY: all
all:
	echo "Nothing here yet."

.PHONY: lint
lint:
	(cd $(ROOT_DIR); $(RUFF) check $(PKG_PATH))

.PHONY: lint-fix
lint-fix:
	(cd $(ROOT_DIR); $(RUFF) check $(PKG_PATH) --fix)

.PHONY: format
format:
	(cd $(ROOT_DIR); $(RUFF) format --check $(PKG_PATH))

.PHONY: format-fix
format-fix:
	(cd $(ROOT_DIR); $(RUFF) format $(PKG_PATH))

.PHONY: format-diff
format-diff:
	(cd $(ROOT_DIR); $(RUFF) format --diff $(PKG_PATH))

.PHONY: type-check
type-check:
	(cd $(ROOT_DIR); $(TY) check --project $(PKG_PATH) $(PKG_PATH)/src)

.PHONY: types
types: type-check

.PHONY: test
test:
	COVERAGE_CORE=sysmon uv run $(UV_PYTHON_FLAG) \
		pytest -v --cov --cov-report=xml tests $(ADD_ARGS) \
		--json-report --json-report-file=.json-report-$(REPORT_TAG).json

.PHONY: test-staging
test-staging:
	@test -n "$(TOKEN)" || (echo "ERROR: TOKEN is required." && exit 1)
	COVERAGE_CORE=sysmon TOKEN=$(TOKEN) DS_PASSWORD=$(DS_PASSWORD) GD_TEST_ENV=staging \
		uv run $(UV_PYTHON_FLAG) \
		pytest -v --cov --cov-report=xml tests $(ADD_ARGS) \
		--json-report --json-report-file=.json-report-staging.json

# this is effective for gooddata-sdk only now - it should be part of test fixtures
# remove this target once implemented in pytest global fixture
.PHONY: remove-store-data
remove-store-data:
	echo "Removing directory $(CURDIR)/tests/catalog/store"
	rm -rf $(CURDIR)/tests/catalog/store

.PHONY: remove-cassettes
remove-cassettes: remove-store-data
	find $(CURDIR)/tests -type f -name "*.yaml" -path "*/fixtures/*" -print -delete
