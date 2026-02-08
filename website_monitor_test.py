import requests
import hashlib
import json
import os
import re
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# TEST CONFIGURATION - Only SSC Notice Board
WEBSITES = [
    {
        'name': 'SSC - Notice Board (TEST)',
        'url': 'https://ssc.gov.in/home/notice-board',
        'selector': 'div[class*="rightSection"], div[class*="innerCard"]',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5  # Only top 5 for testing
    },
]

# File to store previous items
ITEMS_FILE = 'website_items.json'

def load_previous_items():
    """Load previously seen items"""
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_items(items):
    """Save current items"""
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

def extract_notifications(url, selector, link_selector, max_items=5):
    """Extract notification items with titles, links, and dates"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find notification elements
        items = []
        elements = soup.select(selector)
        
        print(f"  Found {len(elements)} elements matching selector")
        
        if not elements:
            print("  Trying fallback selectors...")
            # Fallback: try to find any list in main content
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                elements = main_content.find_all('li')[:max_items]
                print(f"  Fallback found {len(elements)} list items")
        
        for idx, elem in enumerate(elements[:max_items], 1):
            item = {}
            
            # Get FULL text from the entire element
            full_text = elem.get_text(separator=' ', strip=True)
            
            print(f"  Item {idx}: {full_text[:80]}...")
            
            # Extract link
            link_elem = elem.find('a') if link_selector == 'a' else elem.select_one(link_selector)
            
            if link_elem:
                href = link_elem.get('href', '')
                item['link'] = urljoin(url, href) if href else ''
                print(f"    Link found: {item['link'][:60]}")
            else:
                # Check for onclick handlers
                onclick = elem.get('onclick', '')
                if onclick:
                    url_match = re.search(r'["\']([^"\']*\.pdf[^"\']*)["\'"]', onclick)
                    if url_match:
                        item['link'] = urljoin(url, url_match.group(1))
                        print(f"    Link from onclick: {item['link'][:60]}")
                    else:
                        item['link'] = ''
                        print(f"    No link found (no href, no onclick PDF)")
                else:
                    item['link'] = ''
                    print(f"    No link found")
            
            # Use full text as title
            item['title'] = full_text
            
            # Try to extract date
            date_text = ''
            # Look for dateBox class (SSC specific)
            date_elem = elem.find('div', class_=lambda x: x and ('date' in x.lower() if x else False))
            if not date_elem:
                date_elem = elem.find('span', class_=lambda x: x and ('date' in x.lower() if x else False))
            
            if not date_elem:
                # Try to find date pattern in text
                # Format: Feb 05 2026
                date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}', full_text)
                if not date_match:
                    # Format: 05/02/2026 or 05-02-2026
                    date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', full_text)
                if date_match:
                    date_text = date_match.group()
                    print(f"    Date extracted: {date_text}")
            
            if date_elem and not date_text:
                date_text = date_elem.get_text(strip=True)
                print(f"    Date from element: {date_text}")
            
            item['date'] = date_text
            
            # Create unique ID
            item['id'] = hashlib.md5(
                (item['title'] + item['link']).encode('utf-8')
            ).hexdigest()[:12]
            
            # Only add if title is meaningful
            if item['title'] and len(item['title']) > 5:
                items.append(item)
        
        return items
    
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def send_telegram_message(message):
    """Send notification via Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured!")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Split long messages if needed
        max_length = 4000
        if len(message) > max_length:
            parts = [message[i:i+max_length] for i in range(0, len(message), max_length)]
            for part in parts:
                data = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'text': part,
                    'parse_mode': 'HTML',
                    'disable_web_page_preview': True
                }
                requests.post(url, data=data, timeout=10)
            return True
        else:
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}")
        return False

def check_websites():
    """Main function to check all websites"""
    print(f"🔍 TEST MODE - Starting website check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    old_items = load_previous_items()
    new_items = {}
    all_updates = []
    
    for site in WEBSITES:
        name = site['name']
        url = site['url']
        selector = site['selector']
        link_selector = site.get('link_selector', 'a')
        max_items = site.get('max_items', 5)
        
        print(f"\n{'='*60}")
        print(f"Checking: {name}")
        print(f"URL: {url}")
        print(f"Selector: {selector}")
        print(f"{'='*60}")
        
        # Extract current notifications
        current_items = extract_notifications(url, selector, link_selector, max_items)
        
        if current_items is None:
            print(f"⚠️ Failed to fetch content")
            if name in old_items:
                new_items[name] = old_items[name]
            continue
        
        if not current_items:
            print(f"⚠️ No items found (check selector)")
            new_items[name] = []
            continue
        
        print(f"\n✅ Successfully extracted {len(current_items)} items")
        
        # Store current items
        new_items[name] = current_items
        
        # Check for new items
        if name in old_items:
            old_ids = {item['id'] for item in old_items[name]}
            new_notifications = [
                item for item in current_items 
                if item['id'] not in old_ids
            ]
            
            if new_notifications:
                print(f"\n🆕 {len(new_notifications)} NEW items detected!")
                all_updates.append({
                    'site_name': name,
                    'site_url': url,
                    'items': new_notifications
                })
                
                for item in new_notifications:
                    print(f"  NEW: {item['title'][:70]}...")
            else:
                print(f"\n➖ No new items (all {len(current_items)} items seen before)")
        else:
            print(f"\n🆕 First time monitoring - tracking {len(current_items)} items")
            print("   (No notification sent on first run)")
    
    # Save current state
    save_items(new_items)
    print(f"\n💾 Saved items to {ITEMS_FILE}")
    
    # Send notifications if there are updates
    if all_updates:
        message = "🚨 <b>TEST: NEW UPDATES DETECTED!</b>\n"
        message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for update in all_updates:
            message += f"📌 <b>{update['site_name']}</b>\n"
            message += f"🌐 {update['site_url']}\n\n"
            
            for idx, item in enumerate(update['items'], 1):
                # Add title
                if item['link']:
                    message += f"{idx}. <a href='{item['link']}'>{item['title']}</a>\n"
                else:
                    message += f"{idx}. {item['title']}\n"
                
                # Add date if available
                if item['date']:
                    message += f"   📅 {item['date']}\n"
                
                # Note if no link
                if not item['link']:
                    message += f"   ⚠️ <i>No direct link - visit website</i>\n"
                
                message += "\n"
            
            message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Get IST time
        utc_now = datetime.now(timezone.utc)
        ist_offset = timedelta(hours=5, minutes=30)
        ist_time = utc_now + ist_offset
        message += f"⏰ <i>Checked at: {ist_time.strftime('%d-%m-%Y %I:%M %p')} IST</i>"
        
        print(f"\n📱 Sending Telegram notification with {len(all_updates)} update(s)...")
        if send_telegram_message(message):
            print("✅ Notification sent successfully!")
        else:
            print("❌ Failed to send notification")
    else:
        print("\n✅ No new updates detected")
    
    print(f"\n{'='*60}")
    print("TEST COMPLETE")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    check_websites()
