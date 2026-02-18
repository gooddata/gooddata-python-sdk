# (C) 2021 GoodData Corporation
ARG PY_TAG
FROM ghcr.io/astral-sh/uv:0.10 AS uv
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

# Install tox and tox-uv as system packages so they're available globally
# We use uv pip install to install packages from the tox dependency group in pyproject.toml
# by reading from the lock file which ensures consistent versions
# Clean up dependency files after installation to reduce image size
RUN set -x \
  && uv pip install --system --group tox \
  && rm -f pyproject.toml uv.lock \
  && true

COPY .docker/entrypoint.sh /entrypoint.sh

LABEL image_name="GoodData Python SDK test image with python, tox and make"
# LABEL maintainer="TigerTeam <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk/"
LABEL parent_image="python:${PY_TAG}"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["make", "test"]
