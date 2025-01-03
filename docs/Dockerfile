FROM python:3.13-slim AS python-stage

COPY . data

WORKDIR data

RUN pip install --no-cache-dir -r scripts/script-requirements.txt

WORKDIR docs

RUN python3 ../scripts/docs/json_builder.py && \
    mkdir versioned_docs/latest && \
    mv -f data.json versioned_docs/latest && \
    python3 ../scripts/docs/python_ref_builder.py api_spec.toml versioned_docs/latest/data.json latest versioned_docs

FROM node:20.18.0-bookworm-slim

COPY docs docs

COPY --from=python-stage data/docs/versioned_docs/latest/api-reference docs/content/en/latest/api-reference
COPY --from=python-stage data/docs/versioned_docs/latest/pandas docs/content/en/latest/pandas


RUN apt-get update && \
    apt-get install -y git make golang-go curl && \
    npm install -g hugo-extended@0.117.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir -p docs/versioned_docs/latest

COPY --from=python-stage data/docs/versioned_docs/latest/links.json docs/versioned_docs/latest
COPY --from=python-stage data/docs/versioned_docs/latest/data.json docs/versioned_docs/latest

COPY docs/content/en/latest/ docs/versioned_docs/latest/

WORKDIR docs
RUN npm install && \
    rm -rf node_modules

# accessible on http://localhost:1313/latest/
ENTRYPOINT ["hugo", "server", "-e", "dev", "--bind", "0.0.0.0"]
