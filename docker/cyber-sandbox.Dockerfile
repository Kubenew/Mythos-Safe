# Docker sandbox for Mythos-Safe defensive cyber verification
# Minimal, isolated environment for running code analysis

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 sandbox
USER sandbox
WORKDIR /app

COPY --chown=sandbox requirements-sandbox.txt .
RUN pip install --user --no-cache-dir -r requirements-sandbox.txt

COPY --chown=sandbox test_cases/ /app/test_cases/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-c", "print('Mythos-Safe Cyber Sandbox ready')"]