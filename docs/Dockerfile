FROM node:20.11.1-bookworm-slim

RUN apt-get update && \
    apt-get install -y git make golang-go curl && \
    npm install -g hugo-extended@0.117.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY docs docs

WORKDIR docs
RUN npm install

# accessible on http://localhost:1313/latest/
ENTRYPOINT ["hugo", "server", "--bind", "0.0.0.0"]
