from seleniumbase import SB
from app.utils.logger import logger
import time
import random

def fetch_browser(url):
    """
    Fetches URL using SeleniumBase (headless) to bypass Cloudflare.
    """
    logger.info(f"Fetching {url} via Browser...")
    
    try:
        # Use context manager to ensure browser closes
        # uc=True is crucial for Cloudflare
        with SB(uc=True, headless=True, page_load_strategy="eager") as sb:
            
            # Set window size
            sb.set_window_size(random.randint(1024, 1920), random.randint(768, 1080))
            
            # Open with reconnect
            sb.uc_open_with_reconnect(url, reconnect_time=4)
            
            # Check for Cloudflare
            if sb.is_element_visible('iframe[src*="cloudflare"]'):
                logger.info("Cloudflare iframe detected. Attempting to click...")
                sb.uc_gui_click_captcha()
                time.sleep(5)
            
            # Wait for title to not be "Just a moment..."
            try:
                sb.wait_for_element_not_visible('title:contains("Just a moment")', timeout=20)
            except Exception:
                logger.warning("Timed out waiting for Cloudflare challenge to clear.")
            
            # Wait for content
            # Using the selector from the existing scraper
            try:
                sb.wait_for_element("div.b-list-advert__gallery__item", timeout=15)
            except Exception:
                logger.warning("Timed out waiting for listings.")
                
            # Scroll to trigger lazy loading if any
            sb.scroll_to_bottom()
            time.sleep(1)
            sb.scroll_to_top()
            
            content = sb.get_page_source()
            return content
            
    except Exception as e:
        logger.error(f"Browser fetch error for {url}: {e}")
        return None
