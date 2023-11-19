# Separate build image
FROM python:3.11-slim as compile-image
RUN python -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# Final image
FROM python:3.11-slim
COPY --from=compile-image /opt/.venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"
WORKDIR /app
COPY bot /app/bot
COPY migrations /app/migrations
COPY translations /app/translations
COPY utils /app/utils
COPY alembic.ini /app/alembic.ini
CMD ["python", "-m", "bot"]
