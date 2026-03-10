from app.scraper.fetch_http import fetch_http
from app.scraper.fetch_browser import fetch_browser
from app.scraper.parser import parse_html
from app.pipeline.database import init_db
from app.pipeline.save_item import save_item
import sys
import pandas as pd

BASE_URL = "http://jiji.ng"
URL = "http://jiji.ng/mobile-phones"

def test_pipeline():
    print("Initializing DB...")
    init_db()
    
    print(f"Testing fetch for {URL}...")
    
    # 1. Try HTTP
    html = fetch_http(URL)
    if html:
        print("HTTP Fetch Success!")
    else:
        print("HTTP Fetch Failed. Trying Browser...")
        html = fetch_browser(URL)
        
    if html:
        print(f"Got HTML ({len(html)} chars)")
        items = parse_html(html, base_url=BASE_URL)
        print(f"Parsed {len(items)} items.")
        
        if items:
            print("Sample item:", items[0])
            
            # Save to DB
            print("Saving items to DB...")
            count = 0
            for item in items:
                item['source'] = URL
                if save_item(item):
                    count += 1
            print(f"Saved {count} new items to DB.")
            
            # Save to CSV
            print("Saving to CSV...")
            df = pd.DataFrame(items)
            df.to_csv("jiji_mobile_phones.csv", index=False)
            print("\nSaved to jiji_mobile_phones.csv")
            
    else:
        print("All fetch methods failed.")

if __name__ == "__main__":
    # Ensure app is in path
    sys.path.append(".")
    test_pipeline()
