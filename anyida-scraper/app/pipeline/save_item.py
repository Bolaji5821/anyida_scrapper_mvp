from app.pipeline.database import get_db_connection
from app.utils.logger import logger
import sqlite3

def save_item(item):
    """
    Saves a parsed item to the database.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Upsert logic (Insert or Ignore based on unique link)
            # Since SQLite doesn't have ON CONFLICT UPDATE in older versions (though likely supported now),
            # we can just use INSERT OR IGNORE for MVP.
            
            cursor.execute('''
                INSERT OR IGNORE INTO listings (title, price, location, link, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item.get('title'),
                item.get('price'),
                item.get('location'),
                item.get('link'),
                item.get('source', 'unknown')
            ))
            
            if cursor.rowcount > 0:
                logger.info(f"Saved new item: {item.get('title')[:30]}...")
                conn.commit()
                return True
            else:
                logger.debug(f"Item already exists: {item.get('link')}")
                return False
                
    except Exception as e:
        logger.error(f"Error saving item: {e}")
        return False
