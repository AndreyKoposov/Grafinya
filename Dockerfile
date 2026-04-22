# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.14.4
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# RUN apt-get update && \
#     apt-get install -y \
#         gcc \
#         libpq-dev \
#         && rm -rf /var/lib/apt/lists/*

COPY src/ ./src/

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER appuser

EXPOSE 8000

CMD ["gunicorn", "src.app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "240", "--bind", "0.0.0.0:8000"]
