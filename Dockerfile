FROM python:3.10-slim-bullseye

ARG PIP_INDEX_URL=https://pypi.org/simple
ARG POETRY_VERSION=1.1.14
ARG ENVIRONMENT=develop

ENV ENVIRONMENT=${ENVIRONMENT}

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_ACCEPT=y \
    POETRY_URL="https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py" \
    POETRY_VIRTUALENVS_CREATE=false \
    # pip:
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="$PATH:/root/.poetry/bin"

COPY . /code
WORKDIR /code

SHELL ["/bin/bash", "-c"]

RUN update-ca-certificates \
  && apt-get update  \
  && apt-get install curl -y \
  && curl -sSL "${POETRY_URL}" | python /dev/stdin --version "${POETRY_VERSION}"

RUN echo "ENVIRONMENT is ${ENVIRONMENT}" \
    && echo "PIP_INDEX_URL is ${PIP_INDEX_URL}" \
    && source ${HOME}/.poetry/env \
    && poetry config virtualenvs.create false \
    && poetry install $(test ${ENVIRONMENT} = "prod" && echo "--no-dev") --no-interaction

RUN chmod +x ./entrypoint.sh
