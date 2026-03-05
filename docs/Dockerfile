# syntax=docker/dockerfile:1
FROM python:3.14-slim AS builder

RUN apt-get update && apt-get install -y git make curl

# Install Python deps first (changes rarely) for better layer caching.
# Copy only dependency manifests and package source before installing.
COPY scripts/script-requirements.txt /scripts/script-requirements.txt
COPY gooddata-api-client /gooddata-api-client
COPY packages/gooddata-sdk /packages/gooddata-sdk
COPY packages/gooddata-pandas /packages/gooddata-pandas

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /scripts/script-requirements.txt

# Copy source (docs content changes most frequently, scripts less so)
COPY docs docs
COPY scripts/docs/ /docs

WORKDIR /docs

RUN python json_builder.py && \
    python python_ref_builder.py api_spec.toml data.json latest content/en && \
    rm -f data.json

FROM node:20.18.0-bookworm-slim

RUN apt-get update && \
    apt-get install -y git make golang-go curl && \
    npm install -g hugo-extended@0.117.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /docs /docs

WORKDIR /docs

# npm cache mount speeds up rebuilds; Go modules are stored in the image
# layer so Hugo can resolve them at runtime.
RUN --mount=type=cache,target=/root/.npm \
    npm install && \
    hugo mod get

# accessible on http://localhost:1313/latest/
ENTRYPOINT ["hugo", "server", "--bind", "0.0.0.0"]
