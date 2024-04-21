FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"
WORKDIR /app

# Install poetry
RUN set +x \
 && apt update \
 && apt upgrade -y \
 && apt install -y --no-install-recommends curl gcc build-essential \
 && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -\
 && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry \
 && apt-get purge --auto-remove -y curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Prepare entrypoint
ADD . /app/
RUN chmod +x scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]
