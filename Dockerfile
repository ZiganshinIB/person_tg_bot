FROM python:3.10.17

ARG BASE_DIR=/opt/app


ENV \
    # python
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # poetry
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


RUN pip install pipx
RUN PIPX_BIN_DIR=/usr/local/bin pipx install poetry==2.1.1

WORKDIR ${BASE_DIR}
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-ansi

COPY ./src ./src
ENV PYTHONPATH "$PYTHONPATH:${BASE_DIR}/src/"
WORKDIR ${BASE_DIR}/srс
ENTRYPOINT ["python3"]

