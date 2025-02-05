FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y git make curl

COPY scripts/script-requirements.txt /scripts/script-requirements.txt
COPY docs docs
COPY scripts/docs/ /docs
COPY gooddata-api-client /gooddata-api-client
COPY gooddata-sdk /gooddata-sdk
COPY gooddata-pandas /gooddata-pandas

RUN pip install --no-cache-dir -r /scripts/script-requirements.txt

WORKDIR /docs

RUN python json_builder.py && \
    python python_ref_builder.py api_spec.toml data.json latest content/en && \
    mkdir versioned_docs/latest && \
    mv -f data.json ./versioned_docs/latest/data.json && \
    mv -f content/en/latest/links.json ./versioned_docs/latest/links.json

FROM node:20.18.0-bookworm-slim

COPY --from=builder /docs /docs

RUN apt-get update && \
    apt-get install -y git make golang-go curl && \
    npm install -g hugo-extended@0.117.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /docs
RUN npm install && \
    hugo mod get

# accessible on http://localhost:1313/latest/
ENTRYPOINT ["hugo", "server", "--bind", "0.0.0.0"]
