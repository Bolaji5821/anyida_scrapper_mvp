from seleniumbase import SB
from bs4 import BeautifulSoup
import time
import json
import random

def analyze_jiji():
    url = "https://jiji.ng/cars"
    print(f"Fetching {url} with SeleniumBase...")
    
    # UC mode is essential for Cloudflare
    with SB(uc=True, headless=True, page_load_strategy="eager") as sb:
        try:
            # Randomize window size
            sb.set_window_size(random.randint(1024, 1920), random.randint(768, 1080))
            
            # Open with reconnect to simulate real user
            sb.uc_open_with_reconnect(url, reconnect_time=4)
            
            # Wait for Cloudflare challenge to potentially appear and handle it
            print("Checking for Cloudflare...")
            if sb.is_element_visible('iframe[src*="cloudflare"]'):
                print("Cloudflare detected. Clicking...")
                sb.uc_gui_click_captcha()
                time.sleep(5)
            
            # Wait for the title to change from "Just a moment..."
            try:
                sb.wait_for_element_not_visible('title:contains("Just a moment")', timeout=15)
            except:
                print("Title is still 'Just a moment...' - might be stuck.")
            
            # Try to scroll to trigger loading
            sb.scroll_to_bottom()
            time.sleep(2)
            sb.scroll_to_top()
            
            title = sb.get_title()
            print(f"Page Title: {title}")
            
            content = sb.get_page_source()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try to find the data state
            found_data = False
            
            # Check for __INITIAL_STATE__ (Vue/Nuxt) or __NEXT_DATA__ (Next.js)
            for script in soup.find_all('script'):
                if script.string:
                    if 'window.__INITIAL_STATE__' in script.string:
                        print("Found __INITIAL_STATE__")
                        try:
                            json_text = script.string.split('window.__INITIAL_STATE__ = ')[1].strip()
                            if json_text.endswith(';'):
                                json_text = json_text[:-1]
                            data = json.loads(json_text)
                            with open("jiji_state.json", "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2)
                            print("Saved jiji_state.json")
                            found_data = True
                        except Exception as e:
                            print(f"Error extracting state: {e}")
                    elif '__NEXT_DATA__' in script.string:
                         print("Found __NEXT_DATA__")
                         # Extraction logic for Next.js if needed
            
            if not found_data:
                print("No structured JSON state found. Dumping HTML.")
            
            with open("jiji_sb.html", "w", encoding="utf-8") as f:
                f.write(content)
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    analyze_jiji()
