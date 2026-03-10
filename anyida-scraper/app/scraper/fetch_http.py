from curl_cffi import requests
from app.utils.logger import logger
from app.utils.retry import retry_request
from app.utils.headers import get_random_headers

@retry_request(max_attempts=3)
def fetch_http(url):
    """
    Fetches URL using curl_cffi with browser impersonation.
    """
    logger.info(f"Fetching {url} via HTTP...")
    try:
        # Use impersonate="chrome110" as seen in the existing scraper
        # Using headers from utils
        headers = get_random_headers()
        
        response = requests.get(
            url,
            headers=headers,
            impersonate="chrome110",
            timeout=30
        )
        
        if response.status_code == 200:
            return response.text
        elif response.status_code == 403:
            logger.warning(f"HTTP 403 Forbidden for {url} (Cloudflare?)")
            return None
        else:
            logger.error(f"HTTP {response.status_code} for {url}")
            return None
            
    except Exception as e:
        logger.error(f"HTTP fetch error for {url}: {e}")
        raise e # Let retry handle it
