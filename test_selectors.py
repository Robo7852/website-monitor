#!/usr/bin/env python3
"""
CSS Selector Tester
Use this to test if your CSS selectors are working correctly
"""

import requests
from bs4 import BeautifulSoup

def test_selector(url, selector):
    """Test if a CSS selector finds items on a webpage"""
    print(f"\n{'='*60}")
    print(f"Testing URL: {url}")
    print(f"Selector: {selector}")
    print(f"{'='*60}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("Fetching webpage...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        print("✅ Page fetched successfully\n")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try the selector
        elements = soup.select(selector)
        
        if elements:
            print(f"✅ SUCCESS! Found {len(elements)} items\n")
            print("First 5 items found:")
            print("-" * 60)
            
            for idx, elem in enumerate(elements[:5], 1):
                # Try to get link
                link_elem = elem.find('a')
                if link_elem:
                    title = link_elem.get_text(strip=True)
                    href = link_elem.get('href', 'No link')
                else:
                    title = elem.get_text(strip=True)
                    href = 'No link found'
                
                print(f"{idx}. {title[:80]}")
                print(f"   Link: {href[:80]}")
                print()
        else:
            print("❌ FAILED! No items found with this selector\n")
            print("Let's try to find what's available on the page:")
            print("-" * 60)
            
            # Show some common elements that might contain notifications
            print("\n1. Looking for <ul> lists:")
            uls = soup.find_all('ul', limit=3)
            for ul in uls:
                classes = ul.get('class', [])
                print(f"   - Found <ul> with class: {classes}")
            
            print("\n2. Looking for <marquee> tags:")
            marquees = soup.find_all('marquee', limit=3)
            if marquees:
                print(f"   - Found {len(marquees)} marquee elements")
            else:
                print("   - No marquee found")
            
            print("\n3. Looking for common class names:")
            for class_name in ['whats-new', 'latest', 'news', 'updates', 'notification']:
                found = soup.find_all(class_=lambda x: x and class_name in str(x).lower(), limit=1)
                if found:
                    print(f"   - Found elements with '{class_name}' in class name")
            
            print("\n💡 Suggested selectors to try:")
            print("   - 'ul li a' (generic list items)")
            print("   - 'marquee' (scrolling text)")
            print("   - '.content ul li' (content area lists)")
            print("   - 'table tr' (table rows)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("CSS SELECTOR TESTER")
    print("=" * 60)
    
    # Test your websites here
    # Add as many as you want to test
    
    tests = [
        {
            'url': 'https://www.upsc.gov.in/',
            'selector': '.whats_new ul li, .content-part ul li'
        },
        {
            'url': 'https://ssc.nic.in/',
            'selector': 'marquee, .marquee'
        },
        # Add more websites to test here:
        # {
        #     'url': 'https://your-website.com',
        #     'selector': '.your-selector'
        # },
    ]
    
    for test in tests:
        test_selector(test['url'], test['selector'])
        print("\n" + "=" * 60 + "\n")
    
    print("\n✅ Testing complete!")
    print("\nTo test a new website, edit this file and add to the 'tests' list.")
