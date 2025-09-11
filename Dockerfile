FROM python:3.13-slim as builder
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

FROM python:3.13-slim as final 

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=builder /app/.venv ./.venv

COPY ./src ./app

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]