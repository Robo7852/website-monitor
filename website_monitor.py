import requests
import hashlib
import json
import os
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Website configurations - customize the CSS selectors for each site
WEBSITES = [
    {
        'name': 'UPSC New Examinations',
        'url': 'https://upsc.gov.in/examinations/active-exams/',
        'selector': '.view view-exams view-id-exams view-display-id-page_1 view-dom-id-25e80baffe11ec329e64d7dcb13e7e00 li, .view-content li, .views-row views-row-1 views-row-odd views-row-first li, .views-row views-row-2 views-row-even li, .views-row views-row-3 views-row-odd li',
        'type': 'list',  # Extract list items
        'link_selector': 'a',  # How to find links within items
        'max_items': 5  # Show top 5 latest items
    },
    {
        'name': 'Sarkari Result Notification',
        'url': 'https://www.sarkariresult.com/',
        'selector': '#v-sarkariresult li, #post li, .table-center li, #box2 li, #box1 li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
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
        'selector': '.gen-list    no-border no-bg  padding-0 border-radius-none default-list li, #public-notices-content li, .wpb_wrapper li, .gen-list  medium-font  no-bg  padding-20 border-radius-medium default-list accent-border-color li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'ALL INDIA BAR EXAMINATION',
        'url': 'https://www.allindiabarexamination.com/',
        'selector': '.container li, .Notice text-left li',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'NTA UPDATES',
        'url': 'https://nta.ac.in/NoticeBoardArchive',
        'selector': 'table tr',
        'type': 'list',
        'link_selector': 'a',
        'max_items': 5
    },
    {
        'name': 'Finshot updates',
        'url': 'https://finshots.in/archive/',
        'selector': '.post-feed li, .post-card-content li, .post-card-content-link li',
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
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
            
            # Extract link and title
            link_elem = elem.find('a') if link_selector == 'a' else elem.select_one(link_selector)
            
            if link_elem:
                item['title'] = link_elem.get_text(strip=True)
                href = link_elem.get('href', '')
                # Make absolute URL
                item['link'] = urljoin(url, href) if href else ''
            else:
                # No link found, just get text
                item['title'] = elem.get_text(strip=True)
                item['link'] = ''
            
            # Try to extract date (common patterns)
            date_text = ''
            # Look for date patterns in the element or nearby
            date_elem = elem.find('span', class_=lambda x: x and ('date' in x.lower() if x else False))
            if not date_elem:
                date_elem = elem.find('small')
            if date_elem:
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
