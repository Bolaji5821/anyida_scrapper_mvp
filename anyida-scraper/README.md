# Anyida Scraper MVP

A robust scraping system for Jiji.ng built with Python, Celery, and SeleniumBase.

## Architecture

- **Scheduler**: Generates URLs (categories, pagination) and pushes tasks to Redis.
- **Worker**: Consumes tasks from Redis.
  - **Strategy**: Tries fast HTTP scrape (curl_cffi) first.
  - **Fallback**: Uses SeleniumBase (headless browser) if HTTP fails (Cloudflare/403).
- **Parser**: Extracts structured data (Title, Price, Location, Link) using BeautifulSoup.
- **Pipeline**: Saves unique listings to SQLite database.

## Prerequisites

- Python 3.11+
- Redis (for task queue)
- Google Chrome (for browser automation)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis**:
   Ensure Redis is running on localhost:6379.

3. **Run Worker**:
   ```bash
   celery -A app.celery_app worker --loglevel=INFO --pool=solo
   ```
   *Note: `--pool=solo` is required on Windows.*

4. **Run Scheduler**:
   ```bash
   python app/scheduler.py
   ```

## Docker

Run the full stack with Docker Compose:

```bash
docker-compose up --build
```

## Project Structure

```
anyida-scraper/
├── app/
│   ├── scraper/        # Fetching and parsing logic
│   ├── pipeline/       # Database operations
│   ├── utils/          # Logger, Retry, Headers
│   ├── tasks.py        # Celery task definitions
│   ├── worker.py       # Worker entry point
│   ├── scheduler.py    # URL generator
│   └── celery_app.py   # Celery configuration
├── data/               # SQLite database location
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
