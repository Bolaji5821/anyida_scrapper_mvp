#!/usr/bin/env python3
"""
Test script to verify Playwright implementation works
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from scraper.fetch_browser import fetch_browser

def test_playwright():
    """Test Playwright browser functionality"""
    print("Testing Playwright browser implementation...")
    
    # Test with a simple page that should work
    test_url = "https://httpbin.org/html"
    
    try:
        result = fetch_browser(test_url)
        
        if result:
            print("✅ Playwright test SUCCESS!")
            print(f"Retrieved {len(result)} characters")
            # Check if we got HTML content
            if "<html>" in result.lower() and "<body>" in result.lower():
                print("✅ HTML content detected")
            else:
                print("⚠️  HTML content not clearly detected")
            return True
        else:
            print("❌ Playwright test FAILED - No content returned")
            return False
            
    except Exception as e:
        print(f"❌ Playwright test ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_playwright()
    sys.exit(0 if success else 1)