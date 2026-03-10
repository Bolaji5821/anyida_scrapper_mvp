from app.tasks import scrape_category_page
from app.utils.logger import logger
import time

CATEGORIES = [
    "https://jiji.ng/cars",
    "https://jiji.ng/mobile-phones",
    "https://jiji.ng/houses-apartments-for-rent",
    # Add more categories
]

def schedule_scrapes():
    """
    Generates URLs and schedules tasks.
    For MVP, just iterates categories and paginates a few times.
    """
    logger.info("Starting scheduler...")
    
    for category_url in CATEGORIES:
        # Schedule first page
        logger.info(f"Scheduling {category_url}")
        scrape_category_page.delay(category_url)
        
        # Schedule next pages (e.g., page 2 to 5)
        for page in range(2, 4):
            page_url = f"{category_url}?page={page}"
            logger.info(f"Scheduling {page_url}")
            scrape_category_page.delay(page_url)
            
    logger.info("Scheduling complete.")

if __name__ == "__main__":
    schedule_scrapes()
