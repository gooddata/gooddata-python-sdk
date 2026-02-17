# (C) 2021 GoodData Corporation

# Common command components (run from workspace root, scoped to this package)
ROOT_DIR = ../..
RUFF = ./.venv/bin/ruff
# ty needs uv run (unlike ruff) because it resolves imports from installed packages
TY = uv run ty
PKG_PATH = packages/$(CURR_DIR_BASE_NAME)

TOX_FLAGS =
ifeq (1,$(RECREATE_ENVS))
  TOX_FLAGS += -r
endif

LOCAL_TEST_ENVS =
ifdef TEST_ENVS
	LOCAL_TEST_ENVS := -e $(TEST_ENVS)
endif

LOCAL_ADD_ARGS =
ifdef ADD_ARGS
	LOCAL_ADD_ARGS := -- $(ADD_ARGS)
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
	uv run tox -v $(TOX_FLAGS) $(LOCAL_TEST_ENVS) $(LOCAL_ADD_ARGS)

.PHONY: test-ci
test-ci:
	TEST_CI_PROJECT=$(CURR_DIR_BASE_NAME) $(MAKE) -C ../.. -f ci_tests.mk test-ci


# this is effective for gooddata-sdk only now - it should be part of test fixtures
# remove this target once implemented in pytest global fixture
.PHONY: remove-store-data
remove-store-data:
	echo "Removing directory $(CURDIR)/tests/catalog/store"
	rm -rf $(CURDIR)/tests/catalog/store

.PHONY: remove-cassettes
remove-cassettes: remove-store-data
	find $(CURDIR)/tests -type f -name "*.yaml" -path "*/fixtures/*" -print -delete
