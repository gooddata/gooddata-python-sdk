# (C) 2022 GoodData Corporation
ARG PY_TAG="3.9.9-slim-bullseye"
FROM python:${PY_TAG}

ENV USER_NAME=tests
ENV USER_GROUP=tests

RUN set -x \
 && groupadd ${USER_GROUP} \
 && useradd -m -g ${USER_GROUP} ${USER_NAME} \
 && true

USER ${USER_NAME}
WORKDIR /app
COPY ./tests-support/requirements.txt /app/requirements.txt

RUN set -x \
  && pip3 install --no-cache-dir --user -r requirements.txt \
  && true

COPY ./tests-support/*.py /app

LABEL image_name="GoodData Python SDK python test support image"
# LABEL maintainer="TigerTeam <tiger@gooddata.com>"
LABEL git_repository_url="https://github.com/gooddata/gooddata-python-sdk/"
LABEL parent_image="python:${PY_TAG}"

CMD ["python3"]
