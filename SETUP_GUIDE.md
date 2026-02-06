# 🚨 Website Monitor - Complete Setup Guide

Monitor UPSC, MPPEB, and other exam websites for updates automatically and get Telegram notifications every 3 hours!

---

## 📋 PART 1: Create Your Telegram Bot (5 minutes)

### Step 1: Create the Bot
1. Open Telegram app on your phone or computer
2. Search for `@BotFather` (official Telegram bot)
3. Click **Start** or send `/start`
4. Send this command: `/newbot`
5. Follow the prompts:
   - Enter a **name** for your bot (e.g., "Website Monitor")
   - Enter a **username** (must end with 'bot', e.g., "my_website_monitor_bot")
6. **SAVE THE TOKEN** you receive - it looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-ABC123
   ```

### Step 2: Get Your Chat ID
1. Search for your bot's username in Telegram
2. Click **Start** to activate it
3. Send any message to your bot (e.g., "hello")
4. Open this URL in your browser (replace `<YOUR_TOKEN>` with your actual bot token):
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
5. Look for `"chat":{"id":123456789}` in the response
6. **SAVE YOUR CHAT ID** (the number, e.g., 123456789)

---

## 🚀 PART 2: Deploy to GitHub (10 minutes)

### Step 1: Create GitHub Account
- Go to https://github.com and sign up (if you don't have an account)
- Verify your email

### Step 2: Create a New Repository
1. Click the **+** icon (top right) → **New repository**
2. Repository name: `website-monitor`
3. Description: "Automated website monitoring with Telegram notifications"
4. Choose **Public** or **Private** (both work)
5. ✅ Check "Add a README file"
6. Click **Create repository**

### Step 3: Upload Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. In your repository, click **Add file** → **Upload files**
2. Upload these 4 files (download them first from my response):
   - `website_monitor.py`
   - `requirements.txt`
   - `website_hashes.json`
   - `.github/workflows/monitor.yml` (create folder structure first)

3. For the workflow file specifically:
   - Click **Add file** → **Create new file**
   - In filename, type: `.github/workflows/monitor.yml`
   - Paste the workflow content
   - Click **Commit new file**

**Option B: Using Git Command Line**

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/website-monitor.git
cd website-monitor

# Copy the files I provided into this folder

# Create the workflow directory
mkdir -p .github/workflows
# Move monitor.yml to .github/workflows/

# Commit and push
git add .
git commit -m "Initial commit - Website monitor setup"
git push
```

### Step 4: Add Your Telegram Credentials (IMPORTANT!)

1. In your GitHub repository, go to **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add **first secret**:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: (paste your bot token from Part 1)
   - Click **Add secret**
5. Add **second secret**:
   - Name: `TELEGRAM_CHAT_ID`
   - Value: (paste your chat ID from Part 1)
   - Click **Add secret**

---

## ✅ PART 3: Activate and Test

### Enable GitHub Actions
1. Go to **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. You should see "Website Monitor" workflow listed

### Manual Test (First Run)
1. Click on **Website Monitor** workflow
2. Click **Run workflow** → **Run workflow** (green button)
3. Wait 30-60 seconds
4. Click on the running job to see logs
5. **Check your Telegram** - you should receive a test notification!

### Verify Automatic Schedule
- The monitor will now run **automatically every 3 hours**
- Check times: 12:00 AM, 3:00 AM, 6:00 AM, 9:00 AM, 12:00 PM, 3:00 PM, 6:00 PM, 9:00 PM (UTC timezone)
- To convert to IST (Indian Standard Time), add 5:30 hours

---

## 🎯 PART 4: Customize Websites (Optional)

### Add/Remove Websites

Edit `website_monitor.py` file:

```python
WEBSITES = [
    {
        'name': 'UPSC - What\'s New',
        'url': 'https://www.upsc.gov.in/',
        'selector': '.whats_new, .whatsnew, #whatsNew',
        'type': 'content'
    },
    # Add your own websites here:
    {
        'name': 'Your Website Name',
        'url': 'https://example.com',
        'selector': '.updates, .news',  # CSS selector for the section
        'type': 'content'
    },
]
```

### Find CSS Selectors
1. Open the website in Chrome/Firefox
2. Right-click on the "updates" section → **Inspect**
3. Look for class names (e.g., `class="latest-news"`)
4. Use `.latest-news` as selector (dot before class name)
5. Or use ID: `#updateSection` (# before ID)

### Change Check Frequency

Edit `.github/workflows/monitor.yml`:

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours
  # - cron: '0 */1 * * *'  # Every 1 hour
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 9,18 * * *'  # Twice daily (9 AM, 6 PM UTC)
```

---

## 📱 What You'll Receive

When a website posts new updates, you'll get a Telegram message showing the **actual content** with:

```
🚨 NEW UPDATES DETECTED!
━━━━━━━━━━━━━━━━━━━━

📌 UPSC - What's New
🌐 https://www.upsc.gov.in/

1. Combined Defence Services Examination (I), 2026 - Final Result
   📅 05/02/2026

2. Recruitment to the post of Assistant Commandant in CAPF - Notice
   📅 04/02/2026

3. Civil Services (Preliminary) Examination, 2026 - Admit Card

━━━━━━━━━━━━━━━━━━━━

📌 MPPEB - Latest Updates
🌐 https://peb.mp.gov.in/

1. Constable Recruitment 2026 - Online Application Started
   📅 06/02/2026

━━━━━━━━━━━━━━━━━━━━

⏰ Checked at: 06-02-2026 02:30 PM IST
```

**You get:**
- ✅ **Exact titles** of new notifications/updates
- ✅ **Direct clickable links** to each notification
- ✅ **Dates** (when available on the website)
- ✅ Only **NEW** items (not repeating old ones)
- ✅ Multiple websites in one message

---

## 🔧 Troubleshooting

### Not receiving notifications?
1. Check GitHub Actions logs for errors
2. Verify bot token and chat ID in Secrets
3. Make sure you started your bot in Telegram
4. Check if GitHub Actions are enabled

### False positives (too many notifications)?
- The script monitors specific sections only
- Some websites update timestamps/ads frequently
- Refine the CSS selectors to target exact sections

### Want to monitor more than 10 sites?
- Just add more entries to the `WEBSITES` list
- No limit!

---

## 📊 Monitoring Status

Check monitoring status anytime:
1. Go to GitHub repository → **Actions** tab
2. See history of all runs (success/failure)
3. Click any run to see detailed logs

---

## 💡 Pro Tips

1. **Test the bot first**: Send `/start` to your bot and send a message before deployment
2. **Use specific selectors**: Target only the "updates" or "notifications" section
3. **Check logs regularly**: First few runs help you refine selectors
4. **Bookmark your repo**: Easy access to check status
5. **Multiple notifications**: You can add this bot to a Telegram group and get notifications there too!

---

## 🆘 Need Help?

Common issues and fixes:

| Problem | Solution |
|---------|----------|
| "Invalid token" | Double-check TELEGRAM_BOT_TOKEN in Secrets |
| "Chat not found" | Make sure you started the bot and sent a message first |
| No changes detected | Wait for actual website updates, or test with a frequently changing site |
| Workflow not running | Check if Actions are enabled in repository settings |

---

## 🎉 You're All Set!

Your automated monitor is now running 24/7 in the cloud, completely free! You'll get notifications on your phone/computer whenever monitored websites update.

**What's monitored right now:**
- ✅ UPSC official website
- ✅ UPSC notifications
- ✅ MPPEB website
- ✅ SSC website
- ✅ Railway Recruitment Board

Feel free to add more government exam websites following the same pattern!
