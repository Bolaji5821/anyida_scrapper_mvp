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

- Docker and Docker Compose

## Quick Start (Docker)

1.  **Build and Start Services**:
    ```bash
    docker-compose up --build -d
    ```
    This starts Redis and the Celery Worker in the background.

2.  **Run the Scheduler**:
    Trigger the scraping job by running the scheduler container:
    ```bash
    docker-compose run scheduler
    ```

3.  **Check Logs**:
    Watch the worker logs to see the scraping progress:
    ```bash
    docker-compose logs -f worker
    ```

4.  **Verify Data**:
    You can inspect the SQLite database or check the logs for "Saved X new items".
    To verify data inside the container:
    ```bash
    docker-compose exec worker python -c "import sqlite3; conn = sqlite3.connect('data/anyida.db'); print(conn.execute('SELECT COUNT(*) FROM listings').fetchone()[0]);"
    ```

## Local Development (Without Docker)

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
