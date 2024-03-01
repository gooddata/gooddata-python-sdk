FROM node:20.11.1-bookworm-slim

RUN npm install -g hugo-extended@0.117.0

COPY docs docs

RUN apt-get update && \
    apt-get install -y git make golang-go curl

WORKDIR docs
RUN npm install

# accessible on http://localhost:1313/docs/
ENTRYPOINT ["hugo", "server", "--bind", "0.0.0.0"]
