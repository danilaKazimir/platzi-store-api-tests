# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:0.9.30 AS uv
FROM python:3.13.0-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

CMD [".venv/bin/pytest", "-q"]
