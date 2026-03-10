from bs4 import BeautifulSoup
from app.utils.logger import logger

def parse_html(html_content, base_url="https://jiji.ng"):
    """
    Parses HTML content to extract listing data.
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Selectors from the existing scraper
        cards = soup.select("div.b-list-advert__gallery__item")
        
        if not cards:
            # Try alternative layout if gallery item not found (e.g. list layout)
            cards = soup.select("div.b-list-advert-base")
            
        data = []
        
        for card in cards:
            try:
                title_el = card.select_one(".b-advert-title-inner")
                price_el = card.select_one(".qa-advert-price")
                location_el = card.select_one(".b-list-advert__region__text")
                link_el = card.select_one("a.b-list-advert-base")
                
                # Image extraction (bonus)
                image_el = card.select_one("img")
                image_url = image_el.get("src") if image_el else None

                title = title_el.text.strip() if title_el else None
                price = price_el.text.strip() if price_el else None
                location = location_el.text.strip() if location_el else None
                
                link = None
                if link_el:
                    href = link_el.get("href")
                    if href.startswith("http"):
                        link = href
                    else:
                        link = base_url.rstrip("/") + href if href.startswith("/") else base_url + "/" + href

                if title and link:
                    data.append({
                        "title": title,
                        "price": price,
                        "location": location,
                        "link": link,
                        "image_url": image_url
                    })
            except Exception as e:
                logger.warning(f"Error parsing card: {e}")
                continue
                
        return data
        
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return []
