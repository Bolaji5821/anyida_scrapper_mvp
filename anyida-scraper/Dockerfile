FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for curl-cffi and others
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for SeleniumBase (optional if using remote browser or just curl_cffi mostly)
# But for fallback, we need a browser.
# Installing Chrome in Docker is heavy. For MVP, maybe we stick to curl_cffi primarily.
# Or use a separate selenium/standalone-chrome container and connect via Remote WebDriver.
# However, SeleniumBase manages its own drivers/browsers usually.
# Let's keep it simple for now and assume curl_cffi does most work.
# If we need browser, we might need a more complex Dockerfile with Chrome installed.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command
CMD ["python", "app/worker.py"]
