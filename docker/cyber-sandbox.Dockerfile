# Docker sandbox for Mythos-Safe defensive cyber verification
# Minimal, isolated environment for running static analysis only

FROM python:3.11-slim

# Install minimal tools for static analysis only
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 sandboxuser
USER sandboxuser
WORKDIR /sandbox

# Install safe analysis tools
COPY --chown=sandboxuser requirements-sandbox.txt .
RUN pip install --user --no-cache-dir -r requirements-sandbox.txt

# Copy safe test cases (vulnerable code for training, no real exploits)
COPY --chown=sandboxuser test_cases/ ./test_cases/

ENV PYTHONUNBUFFERED=1
ENV PATH="/home/sandboxuser/.local/bin:${PATH}"

CMD ["echo", "Mythos-Safe Defensive Cyber Sandbox initialized."]