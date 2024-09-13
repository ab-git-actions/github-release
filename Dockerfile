FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    ca-certificates \
    libicu-dev \
    && rm -rf /var/lib/apt/lists/*

# Install GitVersion ARM64 binary
RUN wget https://github.com/GitTools/GitVersion/releases/download/6.0.2/gitversion-linux-arm64-6.0.2.tar.gz -O /tmp/gitversion.tar.gz \
    && tar -xzf /tmp/gitversion.tar.gz -C /usr/local/bin \
    && rm /tmp/gitversion.tar.gz \
    && chmod +x /usr/local/bin/gitversion

# Verify GitVersion installation
RUN gitversion /?

# Upgrade pip and install pipenv
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir pipenv

# Add pipenv installation directory to PATH
ENV PATH="$PATH:/root/.local/bin"


WORKDIR /app

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . /app

# Create non-root user and ensure permissions
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser /app \
    && chown appuser /usr/local/bin/gitversion


USER appuser

# Run GitVersion
RUN gitversion


CMD ["pipenv", "run", "python", "main.py"]
