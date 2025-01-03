# (C) 2021 GoodData Corporation
IN_TEST_ENVS = py313,py312,py311,py310,py39
ifdef TEST_ENVS
	IN_TEST_ENVS = $(TEST_ENVS)
endif
COMMA := ,
# space separated list of envs to test in docker if target test-ci is requested
DOCKER_TEST_ENVS = $(subst $(COMMA), ,$(IN_TEST_ENVS))
# for each requested env create target name "test-ci-{env}"
TEST_CI_ENVS = $(foreach test_env,$(DOCKER_TEST_ENVS),test-ci-$(test_env))

# prepare make control flags and send them to docker execution
LOCAL_RECREATE_ENVS =
ifeq (1,$(RECREATE_ENVS))
  LOCAL_RECREATE_ENVS = -e 'RECREATE_ENVS=$(RECREATE_ENVS)'
endif

LOCAL_ADD_ARGS =
ifdef ADD_ARGS
	LOCAL_ADD_ARGS := -e 'ADD_ARGS=$(ADD_ARGS)'
endif

LOCAL_HOST_NETWORK =
ifeq (1,$(HOST_NETWORK))
	LOCAL_HOST_NETWORK := --network=host
endif


# Docker image has default target "make test". When test-ci is called from the project, drill down
# to the project directory so that only tests for given project are executed
DOCKER_COMMAND =
ifdef TEST_CI_PROJECT
	DOCKER_COMMAND = make -C $(TEST_CI_PROJECT) test
endif


# Targets to build docker file for each python version
.PHONY: test-ci-py39-build
test-ci-py39-build: Dockerfile
	docker build --build-arg "PY_TAG=3.9.20-slim-bookworm" --build-arg "ENV_TAG=py39" -t python-sdk:py39 .

.PHONY: test-ci-py310-build
test-ci-py310-build: Dockerfile
	docker build --build-arg "PY_TAG=3.10.15-slim-bookworm" --build-arg "ENV_TAG=py310" -t python-sdk:py310 .

.PHONY: test-ci-py311-build
test-ci-py311-build: Dockerfile
	docker build --build-arg "PY_TAG=3.11.10-slim-bookworm" --build-arg "ENV_TAG=py311" -t python-sdk:py311 .

.PHONY: test-ci-py312-build
test-ci-py312-build: Dockerfile
	docker build --build-arg "PY_TAG=3.12.6-slim-bookworm" --build-arg "ENV_TAG=py312" -t python-sdk:py312 .

.PHONY: test-ci-py313-build
test-ci-py313-build: Dockerfile
	docker build --build-arg "PY_TAG=3.13.1-slim-bookworm" --build-arg "ENV_TAG=py313" -t python-sdk:py313 .

# test-ci target triggers unit tests for each requested environment
.PHONY: test-ci
test-ci: $(TEST_CI_ENVS)

# for each requested environment define target, respective build target prerequisite and variable with env itself
.PHONY: $(TEST_CI_ENVS)
$(TEST_CI_ENVS): TEST_ENV=$(patsubst test-ci-%,%,$@)
.SECONDEXPANSION:
$(TEST_CI_ENVS): $$@-build
	docker run --rm --mount type="bind,src=$(CURDIR),dst=/data" \
           --security-opt seccomp:unconfined \
           --security-opt label=disable \
           $(LOCAL_RECREATE_ENVS) $(LOCAL_ADD_ARGS) \
           $(LOCAL_HOST_NETWORK) \
           -e USER_UID=$$(id -u) \
           -e USER_GID=$$(id -g) \
           python-sdk:$(TEST_ENV) $(DOCKER_COMMAND)
