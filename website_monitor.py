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

# Website configurations - customize the CSS selectors for each site
WEBSITES = [
   
    {
        'name': 'Sarkari Result - Latest Jobs',
        'url': 'https://www.sarkariresult.com/',
        'selector': 'td[align="right"] div#post ul li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 8
    },
    {
        'name': 'Sarkari Result - Admit Cards',
        'url': 'https://www.sarkariresult.com/',
        'selector': 'td[align="center"] div#post ul li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 8
    },
    {
        {
        'name': 'Sarkari Result - Results',
        'url': 'https://www.sarkariresult.com/',
        'selector': 'td[align="left"] div#post ul li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 8
    },
   
    {
        'name': 'MPESB Latest Update',
        'url': 'https://esb.mp.gov.in/e_default.html',
        'selector': '.modal-content li, .modal li, #myModal li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'SSC - Latest Updates',
        'url': 'https://ssc.gov.in/',
        'selector': '.linkHead li,  .notice-board li, .card li, .innerCardHead li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'UGC NET UPDATES',
        'url': 'https://ugcnet.nta.nic.in/',
        'selector': '.vc_tta-panel-body li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'ALL INDIA BAR EXAMINATION',
        'url': 'https://www.allindiabarexamination.com/',
        'selector': '.container',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'NTA UPDATES',
        'url': 'https://nta.ac.in/NoticeBoardArchive',
        'selector': 'table tbody tr, marquee, .marquee',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'Finshot updates',
        'url': 'https://finshots.in/archive/',
        'selector': '.site-content',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'Vajiram Current Affairs',
        'url': 'https://vajiramandravi.com/current-affairs/',
        'selector': '.lcontainer li, .lcolumn li, .item li, .posts-grid li, .left-section li, .first-post li, .right-section li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'CTET UPDATES',
        'url': 'https://ctet.nic.in/',
        'selector': '.wpb_wrapper li, .vc_tta-container li, .vc_tta-panels-container li, .vc_tta-panel-body li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    # Add more websites here following the same pattern
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
        # Enhanced headers to avoid bot detection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find notification elements
        items = []
        elements = soup.select(selector)
        
        if not elements:
            # Fallback: try to find any list in main content
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                elements = main_content.find_all('li')[:max_items]
        
        for elem in elements[:max_items]:
            item = {}
            
            # Get FULL text from the entire element (including text outside <a> tags)
            full_text = elem.get_text(separator=' ', strip=True)
            
            # Extract link
            link_elem = elem.find('a') if link_selector == 'a' else elem.select_one(link_selector)
            
            if link_elem:
                href = link_elem.get('href', '')
                # Make absolute URL
                item['link'] = urljoin(url, href) if href else ''
            else:
                # No link found - check if entire element might be clickable
                onclick = elem.get('onclick', '')
                if onclick:
                    # Try to extract URL from onclick attribute
                    url_match = re.search(r'["\']([^"\']*\.pdf[^"\']*)["\'"]', onclick)
                    if url_match:
                        item['link'] = urljoin(url, url_match.group(1))
                    else:
                        item['link'] = ''
                else:
                    item['link'] = ''
            
            # Use full text as title (this includes everything in the element)
            item['title'] = full_text
            
            # Try to extract date (common patterns)
            date_text = ''
            # Look for date patterns in the element - SSC style (dateBox class)
            date_elem = elem.find('div', class_=lambda x: x and ('date' in x.lower() if x else False))
            if not date_elem:
                date_elem = elem.find('span', class_=lambda x: x and ('date' in x.lower() if x else False))
            if not date_elem:
                date_elem = elem.find('small')
            if not date_elem:
                # Try to find date pattern in text (multiple formats)
                # Format: Feb 05 2026, 05/02/2026, 05-02-2026, etc.
                date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}', full_text)
                if not date_match:
                    date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', full_text)
                if date_match:
                    date_text = date_match.group()
            
            if date_elem and not date_text:
                date_text = date_elem.get_text(strip=True)
            
            item['date'] = date_text
            
            # Create unique ID for this item (for comparison)
            item['id'] = hashlib.md5(
                (item['title'] + item['link']).encode('utf-8')
            ).hexdigest()[:12]
            
            # Only add if title is not empty and meaningful
            if item['title'] and len(item['title']) > 5:
                items.append(item)
        
        return items
    
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def send_telegram_message(message):
    """Send notification via Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured!")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Split long messages if needed (Telegram has 4096 char limit)
        max_length = 4000
        if len(message) > max_length:
            # Send in chunks
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
    print(f"🔍 Starting website check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    old_items = load_previous_items()
    new_items = {}
    all_updates = []
    
    for site in WEBSITES:
        name = site['name']
        url = site['url']
        selector = site['selector']
        link_selector = site.get('link_selector', 'a')
        max_items = site.get('max_items', 5)
        
        print(f"\nChecking: {name}")
        print(f"  URL: {url}")
        
        # Extract current notifications
        current_items = extract_notifications(url, selector, link_selector, max_items)
        
        if current_items is None:
            print(f"  ⚠️ Failed to fetch content")
            # Keep old items if fetch failed
            if name in old_items:
                new_items[name] = old_items[name]
            continue
        
        if not current_items:
            print(f"  ⚠️ No items found (check selector)")
            new_items[name] = []
            continue
        
        print(f"  ✅ Found {len(current_items)} items")
        
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
                print(f"  🆕 {len(new_notifications)} NEW items detected!")
                all_updates.append({
                    'site_name': name,
                    'site_url': url,
                    'items': new_notifications
                })
                
                # Print new items to console
                for item in new_notifications:
                    print(f"    - {item['title'][:60]}...")
            else:
                print(f"  ➖ No new items")
        else:
            print(f"  🆕 First time monitoring - tracking {len(current_items)} items")
            # Don't send notifications on first run, just store items
    
    # Save current state
    save_items(new_items)
    
    # Send notifications if there are updates
    if all_updates:
        # Create detailed message
        message = "🚨 <b>NEW UPDATES DETECTED!</b>\n"
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
                
                message += "\n"
            
            message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Get IST time (UTC + 5:30)
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
        print("\n✅ No new updates detected on any website")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    check_websites()
