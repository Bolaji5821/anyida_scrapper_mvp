from app.celery_app import celery_app
from app.scraper.fetch_http import fetch_http
from app.scraper.fetch_browser import fetch_browser
from app.scraper.parser import parse_html
from app.pipeline.save_item import save_item
from app.utils.logger import logger
import time

@celery_app.task(bind=True, max_retries=2)
def scrape_category_page(self, url):
    """
    Task to scrape a category page.
    """
    logger.info(f"Task received: Scrape {url}")
    
    html = None
    
    # 1. Try HTTP
    try:
        html = fetch_http(url)
    except Exception as e:
        logger.warning(f"HTTP fetch failed for {url}: {e}")
    
    # 2. Fallback to Browser
    if not html:
        logger.info(f"Falling back to browser for {url}")
        try:
            html = fetch_browser(url)
        except Exception as e:
            logger.error(f"Browser fetch failed for {url}: {e}")
            # Retry the task
            raise self.retry(exc=e, countdown=60)
            
    if not html:
        logger.error(f"Failed to fetch {url} via both methods.")
        return {"status": "failed", "url": url}
        
    # 3. Parse
    items = parse_html(html)
    logger.info(f"Parsed {len(items)} items from {url}")
    
    # 4. Save
    saved_count = 0
    for item in items:
        item['source'] = url
        if save_item(item):
            saved_count += 1
            
    logger.info(f"Saved {saved_count} new items from {url}")
    
    return {"status": "success", "url": url, "items_found": len(items), "items_saved": saved_count}
