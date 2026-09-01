# (C) 2021 GoodData Corporation
ARG PY_TAG
FROM ghcr.io/astral-sh/uv:0.12 AS uv
FROM python:${PY_TAG}

ARG PY_TAG
ARG ENV_TAG

# tox defines all python targets, makefile recognizes TEST_ENVS and forces
# tox to execute only tests for installed python
ENV TEST_ENVS=${ENV_TAG}

# copy uv binary from official image; version is guarded by required-version in pyproject.toml
COPY --from=uv /uv /usr/local/bin/uv

# install make and gosu
ENV GOSU_VERSION=1.14
RUN set -x \
  && apt-get update \
  && apt-get install -y --no-install-recommends make curl gnupg \
  && curl -sSLo /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" \
  && curl -sSLo /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc" \
  && export GNUPGHOME="$(mktemp -d)" \
  && gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
  && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
  && rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc \
  && chmod +x /usr/local/bin/gosu \
  && gosu nobody true \
  && apt-get -y remove curl gnupg \
  && apt-get -y auto-remove \
  && rm -rf /var/lib/apt/lists/* \
  && true

# Set working directory before copying files
WORKDIR /data

# copy dependency files - these will be available at build time
# At runtime, the directory will be mounted, but uv will use the lock file
# to ensure consistent dependencies
COPY pyproject.toml uv.lock ./

# Install tox and tox-uv as system packages so they're available globally.
# Via `uv export` and not `uv pip install --group`: the latter re-resolves fresh from the
# index, while export reads uv.lock, so the image gets exactly the pinned versions.
# NOTE: tox-uv's `uv` dependency installs a console script over the binary COPYed above;
# [tool.uv] constraint-dependencies keeps the locked version inside required-version.
# Clean up dependency files after installation to reduce image size
RUN set -x \
  && uv export --frozen --only-group tox -o /tmp/tox-requirements.txt \
  && uv pip install --system -r /tmp/tox-requirements.txt \
  && rm -f pyproject.toml uv.lock /tmp/tox-requirements.txt \
  && true

# Any uv command here must not REWRITE the bind-mounted host uv.lock if it thinks it is
# stale -- fail instead. Not UV_FROZEN: tox-uv reads that and downgrades its own --locked
# to --frozen, silently accepting a stale lock. Must be set AFTER the export above, which
# is rejected in combination with UV_LOCKED and has to stay --frozen because only the root
# pyproject.toml and uv.lock exist at that layer for --locked to validate against.
ENV UV_LOCKED=1

# Use the lock-pinned tox installed system-wide above rather than project_common.mk's
# default `uv run tox`, which would first sync the whole workspace into a throwaway
# in-container project env (measured: 58 packages, ~7s) just to obtain the same tox.
ENV TOX=tox

# The repo is bind-mounted at /data, so the default project environment (/data/.venv) is
# the developer's host venv; a `uv run` here would rebuild it against this image's Linux
# interpreter. Redirect it somewhere container-local (/tmp, not a home dir: the runtime
# user is created by entrypoint.sh, so no home exists when this ENV is evaluated).
ENV UV_PROJECT_ENVIRONMENT=/tmp/uv-project-venv

COPY .docker/entrypoint.sh /entrypoint.sh

LABEL image_name="GoodData Python SDK test image with python, tox and make"
# LABEL maintainer="TigerTeam <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk/"
LABEL parent_image="python:${PY_TAG}"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["make", "test"]
