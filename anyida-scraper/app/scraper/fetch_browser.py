from playwright.sync_api import sync_playwright
from app.utils.logger import logger
import time
import random

def fetch_browser(url):
    """
    Fetches URL using Playwright (headless) to bypass Cloudflare.
    """
    logger.info(f"Fetching {url} via Playwright Browser...")
    
    try:
        with sync_playwright() as p:
            # Launch browser with stealth options to avoid detection
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    f'--window-size={random.randint(1024, 1920)},{random.randint(768, 1080)}'
                ]
            )
            
            # Create context with stealth settings
            context = browser.new_context(
                viewport={'width': random.randint(1024, 1920), 'height': random.randint(768, 1080)},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                java_script_enabled=True,
                bypass_csp=True
            )
            
            # Add stealth evasions
            context.add_init_script("""
                // Overwrite the `languages` property to use a custom getter
                Object.defineProperty(navigator, 'languages', {
                    get: function() {
                        return ['en-US', 'en'];
                    },
                });
                
                // Overwrite the `plugins` property to use a custom getter
                Object.defineProperty(navigator, 'plugins', {
                    get: function() {
                        // Return a non-empty array
                        return [1, 2, 3, 4, 5];
                    },
                });
                
                // Pass the WebDriver test
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Pass the Chrome test
                window.chrome = {
                    runtime: {},
                };
            """)
            
            page = context.new_page()
            
            # Navigate to URL
            response = page.goto(url, wait_until='domcontentloaded', timeout=30000)
            
            # Check for Cloudflare challenge
            if response and response.status == 403:
                logger.warning("Cloudflare challenge detected. Waiting for resolution...")
                # Wait for Cloudflare challenge to clear
                try:
                    page.wait_for_selector("text=Just a moment", timeout=5000, state='hidden')
                    page.wait_for_load_state('networkidle', timeout=15000)
                except:
                    logger.warning("Cloudflare challenge may still be present")
            
            # Wait for content to load
            try:
                page.wait_for_selector("div.b-list-advert__gallery__item", timeout=15000)
            except:
                logger.warning("Timed out waiting for listings, proceeding anyway")
            
            # Scroll to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            page.evaluate("window.scrollTo(0, 0)")
            
            # Get page content
            content = page.content()
            
            # Close browser
            browser.close()
            
            return content
            
    except Exception as e:
        logger.error(f"Playwright browser fetch error for {url}: {e}")
        return None
