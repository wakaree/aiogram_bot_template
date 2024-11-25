FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"
WORKDIR /app

COPY pyproject.toml /app/
ADD . /app/
RUN pip install --no-cache-dir poetry &&  \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root && \
    chmod +x scripts/*
