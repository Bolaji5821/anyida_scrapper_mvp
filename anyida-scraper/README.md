# Anyida Scraper MVP

A distributed web scraping system built with Python, Celery, and Playwright for scraping Jiji.ng marketplace data with Cloudflare bypass capabilities.

## 🚀 Features

- **Dual Scraping Strategy**: HTTP requests with curl_cffi + Playwright browser fallback
- **Cloudflare Bypass**: Advanced anti-detection measures for bypassing Cloudflare protection
- **Distributed Architecture**: Celery task queue with Redis broker for scalable scraping
- **Dockerized**: Complete containerized deployment with multi-service architecture
- **Data Persistence**: SQLite database for storing scraped items
- **Robust Error Handling**: Exponential backoff retry logic and comprehensive logging

## 📁 Project Structure

```
anyida-scraper/
├── app/
│   ├── pipeline/
│   │   ├── database.py      # SQLite database operations
│   │   └── save_item.py      # Item saving logic
│   ├── scraper/
│   │   ├── fetch_http.py     # HTTP scraping with curl_cffi
│   │   ├── fetch_browser.py  # Browser scraping with Playwright
│   │   └── parser.py         # HTML parsing with BeautifulSoup
│   ├── utils/
│   │   ├── logger.py         # Logging configuration
│   │   ├── retry.py          # Retry decorators
│   │   └── headers.py       # HTTP headers management
│   ├── celery_app.py         # Celery application configuration
│   ├── tasks.py              # Celery task definitions
│   ├── scheduler.py          # Task scheduling logic
│   └── worker.py             # Worker entry point
├── data/
│   └── anyida.db            # SQLite database file
├── logs/
│   └── scraper.log          # Application logs
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── test_scraper.py          # End-to-end testing script
└── test_playwright.py       # Playwright functionality test
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Redis server (optional, included in Docker setup)

### Local Development

1. **Clone and setup environment:**
   ```bash
   cd anyida-scraper
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Setup environment variables:**
   ```bash
   # Create .env file
   echo "REDIS_URL=redis://localhost:6379/0" > .env
   ```

### Docker Deployment

1. **Build and start containers:**
   ```bash
   docker-compose up --build -d
   ```

2. **Check container status:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

## 🚀 Usage

### Running the Scraper

#### Method 1: Docker Compose (Recommended)
```bash
# Start all services
cd anyida-scraper
docker-compose up --build -d

# Run scheduler to start scraping
docker-compose run scheduler python app/scheduler.py
```

#### Method 2: Manual Setup
```bash
# Start Redis (if not using Docker)
redis-server

# Start Celery worker
celery -A app.celery_app worker --loglevel=info --pool=solo

# Run scheduler in another terminal
python app/scheduler.py
```

### Testing

#### Test Playwright Browser
```bash
python test_playwright.py
```

#### Test Full Scraper Pipeline
```bash
python test_scraper.py
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Target URLs

Edit `app/scheduler.py` to modify target categories:
```python
CATEGORIES = [
    "https://jiji.ng/mobile-phones",
    "https://jiji.ng/cars", 
    "https://jiji.ng/houses-apartments-for-rent",
    # Add more categories
]
```

## 🐳 Docker Architecture

The Docker setup includes:

1. **Redis Service**: Message broker for Celery tasks
2. **Worker Service**: Celery worker for processing scraping tasks
3. **Scheduler Service**: Task scheduler (run manually when needed)

### Container Services

- **Redis**: `redis:alpine`
- **Worker**: Custom Python image with Playwright
- **Scheduler**: Same image as worker, runs scheduling logic

## 🔧 Technical Details

### Scraping Strategy

1. **Primary**: HTTP requests using `curl_cffi` with browser impersonation
2. **Fallback**: Playwright browser automation with anti-detection measures
3. **Retry Logic**: Exponential backoff with 2 retry attempts

### Anti-Detection Features

- **HTTP Headers**: Realistic browser headers and user agents
- **Playwright Stealth**: JavaScript property overwrites and WebDriver detection bypass
- **Randomization**: Viewport sizes, timing delays, and user agent rotation
- **Cloudflare Handling**: Automatic challenge detection and waiting

### Data Storage

- **SQLite Database**: Local file-based storage in `data/anyida.db`
- **Table Schema**: Items stored with title, price, location, and link
- **CSV Export**: Test script exports to `jiji_mobile_phones.csv`

## 📊 Monitoring

### Logs

- Application logs: `logs/scraper.log`
- Docker logs: `docker-compose logs -f`
- Celery logs: Visible in worker output

### Database

Check scraped data:
```bash
sqlite3 data/anyida.db "SELECT COUNT(*) FROM items;"
sqlite3 data/anyida.db "SELECT * FROM items LIMIT 5;"
```

## 🚨 Troubleshooting

### Common Issues

1. **Cloudflare Blocks**:
   - The scraper includes anti-detection measures
   - If blocked, wait and retry later
   - Consider rotating proxies in production

2. **Playwright Installation**:
   ```bash
   # Reinstall Playwright browsers
   playwright install --with-deps chromium
   ```

3. **Docker Build Issues**:
   ```bash
   # Clean build
   docker-compose down
   docker system prune -a
   docker-compose up --build
   ```

4. **Redis Connection**:
   - Ensure Redis is running on port 6379
   - Check `REDIS_URL` environment variable

### Debug Mode

Enable verbose logging:
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or modify .env file
LOG_LEVEL=DEBUG
```

## 📈 Performance

- **Concurrency**: Celery supports multiple workers for parallel scraping
- **Memory**: Playwright browsers run headless to conserve resources
- **Persistence**: SQLite provides lightweight local storage
- **Scalability**: Redis broker allows horizontal scaling of workers

## 🔮 Future Enhancements

- [ ] Proxy rotation support
- [ ] Rate limiting configuration
- [ ] Advanced pagination handling
- [ ] Real-time monitoring dashboard
- [ ] Email/notification system
- [ ] API endpoints for data access

## 📝 License

This project is for educational and demonstration purposes. Ensure compliance with Jiji.ng's terms of service and robots.txt when deploying.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Ensure all dependencies are properly installed
4. Verify Docker containers are running correctly