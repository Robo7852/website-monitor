# 📱 Example Telegram Notifications

## How Your Notifications Will Look

### Example 1: Single Website Update

```
🚨 NEW UPDATES DETECTED!
━━━━━━━━━━━━━━━━━━━━

📌 UPSC - What's New
🌐 https://www.upsc.gov.in/

1. Combined Defence Services Examination (I), 2026 - Final Result
   📅 05/02/2026

2. Recruitment to the post of Assistant Commandant in Central Armed Police Forces
   📅 04/02/2026

3. Civil Services (Preliminary) Examination, 2026 - Admit Card Released

━━━━━━━━━━━━━━━━━━━━

⏰ Checked at: 06-02-2026 02:30 PM IST
```

---

### Example 2: Multiple Websites Updated

```
🚨 NEW UPDATES DETECTED!
━━━━━━━━━━━━━━━━━━━━

📌 UPSC - Notifications
🌐 https://www.upsc.gov.in/notifications

1. Engineering Services (Main) Examination, 2026 - Schedule Released
   📅 06/02/2026

━━━━━━━━━━━━━━━━━━━━

📌 SSC - Latest News
🌐 https://ssc.nic.in/

1. Combined Graduate Level Examination - Tier II Admit Card
   📅 05/02/2026

2. Junior Engineer (Civil, Mechanical, Electrical) Examination 2026 - Notification
   📅 05/02/2026

━━━━━━━━━━━━━━━━━━━━

📌 MPPEB - Latest Updates
🌐 https://peb.mp.gov.in/

1. MP Vyapam Sub Engineer Recruitment 2026 - Application Form
   📅 06/02/2026

━━━━━━━━━━━━━━━━━━━━

⏰ Checked at: 06-02-2026 05:30 PM IST
```

---

## What Each Notification Contains

### ✅ Website Name & URL
Shows which website posted the update

### ✅ Exact Notification Title
The actual heading/title as it appears on the website (clickable link)

### ✅ Date/Time Stamp
When the notification was posted (if available on the website)

### ✅ Direct Links
Click the title to go directly to that notification

### ✅ Only NEW Items
You'll only see notifications that appeared since the last check - no repetitions!

---

## Smart Features

### 🔍 Tracks Individual Items
The script remembers each notification by its title and link, so even if a website reorders their list, you won't get duplicate alerts.

### 📊 Top 5 Latest Items
By default, monitors the 5 most recent items from each website (customizable).

### 🔗 Clickable Links
All notification titles are clickable - tap to open in browser.

### ⏰ Time Stamped
Every notification includes the exact check time in IST.

---

## Important Notes

### First Run Behavior
- On the **first run**, the script will NOT send notifications
- It will just record the current state of all websites
- From the **second run** onwards, you'll get notifications for new items

### What Counts as "New"?
- Any notification that wasn't there in the previous check
- Based on title + link combination (unique ID)

### Handling Website Changes
- If a website redesigns and changes their HTML structure, you may need to update the CSS selector
- The script will log warnings if it can't find items

---

## Customization Examples

### Show More Items Per Website

In `website_monitor.py`, change:
```python
'max_items': 5  # Change to 10, 15, etc.
```

### Filter Specific Keywords

You can add filtering logic to only notify about items containing certain words:
```python
# Example: Only notify about "Admit Card" or "Result"
keywords = ['admit card', 'result', 'answer key']
if any(keyword in item['title'].lower() for keyword in keywords):
    # Send notification
```

---

## Sample Console Output

When the script runs, you'll see logs like:

```
🔍 Starting website check at 2026-02-06 14:30:00

Checking: UPSC - What's New
  URL: https://www.upsc.gov.in/
  ✅ Found 5 items
  🆕 2 NEW items detected!
    - Combined Defence Services Examination (I), 2026 - Final R...
    - Recruitment to the post of Assistant Commandant in Centra...

Checking: MPPEB - Latest Updates
  URL: https://peb.mp.gov.in/
  ✅ Found 3 items
  ➖ No new items

Checking: SSC - Latest News
  URL: https://ssc.nic.in/
  ✅ Found 4 items
  🆕 1 NEW items detected!
    - Junior Engineer Examination 2026 - Notification...

📱 Sending Telegram notification with 2 update(s)...
✅ Notification sent successfully!

============================================================
```
