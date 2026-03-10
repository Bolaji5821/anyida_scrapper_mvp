from fake_useragent import UserAgent
import random

ua = UserAgent()

def get_random_headers():
    """
    Generates random headers to mimic a real browser.
    """
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

def get_browser_fingerprint():
    """
    Returns a dictionary of browser fingerprint settings for Playwright/Selenium.
    """
    return {
        "timezone_id": "Africa/Lagos",  # Match Jiji.ng target audience
        "locale": "en-US",
        "geolocation": {"latitude": 6.5244, "longitude": 3.3792}, # Lagos
        "color_scheme": "dark",
    }
