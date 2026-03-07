FROM python:3.12-bullseye AS builder

ARG DEV=false

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev python3-dev libffi-dev zlib1g-dev \
    libjpeg62-turbo-dev libpng-dev libfreetype6-dev libtiff5-dev liblcms2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY appliances/requirements/ /tmp/requirements/

RUN pip install --upgrade pip setuptools wheel && \
    if [ "$DEV" = "true" ]; then \
        pip install --no-cache-dir --prefer-binary -r /tmp/requirements/local.txt; \
    else \
        pip install --no-cache-dir --prefer-binary -r /tmp/requirements/prod.txt; \
    fi


FROM python:3.12-slim-bullseye AS final

ARG DEV=false

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 libjpeg62-turbo libpng16-16 libtiff5 libfreetype6 curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 taskforge && \
    useradd --uid 1000 --gid 1000 --no-create-home --shell /bin/bash taskforge

COPY --from=builder --chown=taskforge:taskforge /opt/venv /opt/venv

COPY --chown=taskforge:taskforge . /app

USER taskforge

EXPOSE 8000
