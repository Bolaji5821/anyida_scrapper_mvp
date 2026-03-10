FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for curl-cffi and Playwright
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    gnupg \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers and dependencies
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command
CMD ["python", "app/worker.py"]
