# (C) 2021 GoodData Corporation
ARG PY_TAG
FROM python:${PY_TAG}

ARG PY_TAG
ARG ENV_TAG
# tox defines all python targets, makefile recognizes TEST_ENVS and forces
# tox to execute only tests for installed python
ENV TEST_ENVS=${ENV_TAG}

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

# install tox
ENV PYTHON_TOX_VERSION=4.14.1
ENV PYTHON_TOX_UV_VERSION=1.7.0
RUN set -x \
  && pip3 install tox==${PYTHON_TOX_VERSION} tox-uv==${PYTHON_TOX_UV_VERSION}\
  && true

COPY .docker/entrypoint.sh /entrypoint.sh
WORKDIR /data

LABEL image_name="GoodData Python SDK test image with python, tox and make"
# LABEL maintainer="TigerTeam <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk/"
LABEL parent_image="python:${PY_TAG}"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["make", "test"]
