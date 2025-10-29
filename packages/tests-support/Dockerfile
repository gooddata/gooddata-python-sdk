# (C) 2022 GoodData Corporation
ARG PY_TAG="python3.14-bookworm"
FROM ghcr.io/astral-sh/uv:${PY_TAG}

ENV USER_NAME=tests
ENV USER_GROUP=tests

RUN set -x \
 && groupadd ${USER_GROUP} \
 && useradd -m -g ${USER_GROUP} ${USER_NAME} \
 && true

WORKDIR /app
COPY ./packages/tests-support/pyproject.toml /app/pyproject.toml
COPY ./packages/tests-support/src /app/src

RUN set -x \
  && uv pip install --system . \
  && true

USER ${USER_NAME}

COPY ./packages/tests-support/fixtures /app/fixtures
COPY ./packages/tests-support/*.py /app

LABEL image_name="GoodData Python SDK python test support image"
# LABEL maintainer="TigerTeam <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk/"
LABEL parent_image="ghcr.io/astral-sh/uv:${PY_TAG}"

CMD ["python3"]
