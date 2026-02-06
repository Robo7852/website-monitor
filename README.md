# 🔔 Automated Website Monitor

Get instant Telegram notifications when UPSC, MPPEB, SSC, and other exam websites post new updates!

## 🌟 Features

- ✅ **Shows exact notification titles and links** - See what was actually posted!
- ✅ Monitors specific sections (like "What's New", "Latest Notifications")
- ✅ Extracts dates when available
- ✅ Runs automatically every 3 hours (24/7)
- ✅ Free forever (uses GitHub Actions)
- ✅ No server or computer needed
- ✅ Instant Telegram notifications with clickable links
- ✅ Easy to customize

## 🚀 Currently Monitoring

1. **UPSC** - What's New & Notifications
2. **MPPEB** - Latest Updates
3. **SSC** - Latest News
4. **Railway Recruitment Board** - Updates
5. *Add your own websites easily!*

## 📖 Setup Instructions

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete step-by-step instructions.

**Quick Start:**
1. Create Telegram bot (5 mins)
2. Fork/upload this repo to your GitHub (5 mins)
3. Add bot credentials to GitHub Secrets (2 mins)
4. Done! Notifications start automatically

## 🔧 Customization

### Add More Websites

Edit `website_monitor.py`:

```python
WEBSITES = [
    {
        'name': 'Your Website Name',
        'url': 'https://example.com',
        'selector': '.updates',  # CSS selector
        'type': 'content'
    },
]
```

### Change Check Frequency

Edit `.github/workflows/monitor.yml` cron schedule.

## 📱 Sample Notification

```
🚨 NEW UPDATES DETECTED!
━━━━━━━━━━━━━━━━━━━━

📌 UPSC - What's New
🌐 https://www.upsc.gov.in/

1. Combined Defence Services Examination (I), 2026 - Final Result
   📅 05/02/2026

2. Recruitment to the post of Assistant Commandant in CAPF
   📅 04/02/2026

━━━━━━━━━━━━━━━━━━━━

⏰ Checked at: 06-02-2026 02:30 PM IST
```

**Each notification includes:**
- ✅ Exact title/heading of the update
- ✅ Direct clickable link to the notification
- ✅ Date (if available on the website)
- ✅ Website name and URL

## 🆓 Completely Free

- GitHub Actions: 2,000 minutes/month (free)
- This monitor uses ~5 mins/day = 150 mins/month
- Telegram: Free forever
- Total cost: **₹0**

## 📊 View Monitoring History

Go to **Actions** tab to see:
- All check runs (success/failure)
- Detailed logs
- Execution times

## ⚡ Tech Stack

- Python 3.10
- BeautifulSoup4 (web scraping)
- Requests (HTTP)
- GitHub Actions (automation)
- Telegram Bot API (notifications)

## 📄 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ for exam aspirants across India**

*Never miss an important notification again!*
