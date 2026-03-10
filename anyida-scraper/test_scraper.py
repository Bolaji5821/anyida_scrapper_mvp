from app.scraper.fetch_http import fetch_http
from app.scraper.fetch_browser import fetch_browser
from app.scraper.parser import parse_html
from app.pipeline.database import init_db
from app.pipeline.save_item import save_item
import sys

def test_pipeline():
    print("Initializing DB...")
    init_db()
    
    url = "https://jiji.ng/mobile-phones"
    print(f"Testing fetch for {url}...")
    
    # 1. Try HTTP
    html = fetch_http(url)
    if html:
        print("HTTP Fetch Success!")
    else:
        print("HTTP Fetch Failed. Trying Browser...")
        html = fetch_browser(url)
        
    if html:
        print(f"Got HTML ({len(html)} chars)")
        items = parse_html(html)
        print(f"Parsed {len(items)} items.")
        
        if items:
            print("Sample item:", items[0])
            print("Saving items...")
            count = 0
            for item in items:
                item['source'] = url
                if save_item(item):
                    count += 1
            print(f"Saved {count} new items.")
    else:
        print("All fetch methods failed.")

if __name__ == "__main__":
    # Ensure app is in path
    sys.path.append(".")
    test_pipeline()
