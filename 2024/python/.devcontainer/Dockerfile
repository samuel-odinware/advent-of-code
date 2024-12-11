ARG UV_VERSION=0.5.7
ARG DEBIAN_VERSION=bookworm


FROM ghcr.io/astral-sh/uv:${UV_VERSION}-${DEBIAN_VERSION} AS uv


FROM mcr.microsoft.com/vscode/devcontainers/base:${DEBIAN_VERSION}
LABEL maintainer="Samuel Moore <samuel@odinware.com>"

COPY --from=uv --chown=vscode: /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/
