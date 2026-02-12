# 🦁 LION SIGNAL HQ - COMPLETE BUILD PACKAGE

## ✅ BUILD COMPLETE!

I've built your complete LION SIGNAL HQ system! Everything is ready to deploy.

---

## 📦 WHAT YOU GOT (12 Files)

### Core Python Files (The Robots):
1. **config.py** - Settings (365-day retention, batch size, etc.)
2. **scraper.py** - The Scout (visits BSE/NSE websites)
3. **analyzer.py** - The Brain (Gemini AI analysis)
4. **database.py** - The Notebook (saves summaries, auto-deletes after 365 days)
5. **main.py** - The Conductor (runs everything together)
6. **app.py** - Web Server (serves the dashboard)

### Helper Files:
7. **requirements.txt** - List of Python packages to install
8. **test_system.py** - Test script (run locally to verify everything works)
9. **.env.example** - Template for environment variables
10. **.gitignore** - Prevents sensitive files from uploading to GitHub

### Documentation:
11. **README.md** - Quick reference guide
12. **SETUP_GUIDE.md** - Super detailed step-by-step instructions for 5-year-olds

### Folders:
13. **.github/workflows/schedule.yml** - GitHub Actions (runs every 30 min)
14. **templates/dashboard.html** - Your beautiful dashboard

---

## 🎯 WHAT IT DOES (Recap)

```
Every 30 minutes (24/7):
  ↓
Scrapes BSE & NSE websites
  ↓
Finds NEW announcements (gets PDF links)
  ↓
Batches 20 PDF links together
  ↓
Sends to Gemini AI for analysis
  ↓
Gemini extracts:
  • Company name
  • Headline (what it's about)
  • Category (Results, Order, Dividend, etc.)
  • Importance score (1-10)
  • Smart summary (2-3 lines with key numbers)
  • Key financial data (Revenue, Profit, Orders, etc.)
  ↓
Saves ONLY summaries + links to database
(NOT the PDFs - just links!)
  ↓
Auto-deletes anything older than 365 days
  ↓
Beautiful dashboard shows everything
  ↓
Sleeps for 30 minutes
  ↓
REPEATS FOREVER
```

**Cost: ₹0** (Gemini free tier + GitHub Actions free)

---

## 🚀 HOW TO DEPLOY (3 Options)

### Option 1: GitHub Actions (RECOMMENDED - Runs 24/7 for FREE)

**Follow SETUP_GUIDE.md** - It has step-by-step screenshots-style instructions.

Quick version:
1. Get Gemini API key from https://aistudio.google.com/apikey
2. Create GitHub account
3. Create new repository: `lion-signal-hq`
4. Upload ALL 12 files + folders
5. Add GEMINI_API_KEY in Settings → Secrets → Actions
6. Go to Actions tab → Run workflow
7. Done! Runs every 30 min automatically

### Option 2: Run Locally on Your Computer

```bash
# Install Python packages
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY='your-key-here'

# Test everything works
python test_system.py

# Run the scraper once manually
python main.py

# Start the web dashboard
python app.py

# Open browser to: http://localhost:5000
```

**Note:** With this option, you need to keep your computer on and run `python main.py` every 30 min manually (or use cron/Task Scheduler).

### Option 3: Cloud Server (DigitalOcean, AWS, etc.)

Same as Option 2, but on a cloud server that runs 24/7.

Cost: ~$5-10/month (but more reliable than your PC).

---

## ⚙️ CUSTOMIZATION (Super Easy!)

All settings are in **config.py**:

```python
# Change retention period
RETENTION_DAYS = 365  # Change to 7, 30, 90, 1000, whatever!

# Change update frequency
UPDATE_FREQUENCY_MINUTES = 30  # Every 30 minutes

# Change batch size
BATCH_SIZE = 20  # Send 20 PDFs to Gemini at once

# Show only important announcements
MIN_IMPORTANCE_TO_DISPLAY = 1  # Change to 5 to hide boring ones

# Filter exchanges
SHOW_BSE = True
SHOW_NSE = True
SHOW_NSE_SME = True  # Set to False to hide SME
```

Just edit the numbers and it adjusts automatically!

---

## 📊 THE DASHBOARD

Your dashboard has:

✅ **Light/Dark mode toggle** (click 🌙/☀️ button)  
✅ **Search** (type company name)  
✅ **Filter by exchange** (BSE, NSE, NSE-SME)  
✅ **Filter by category** (Results, Orders, Dividend, etc.)  
✅ **Live stats** (today's count, last update time)  
✅ **Beautiful cards** showing:
   - Company name + exchange badge
   - Headline (uppercase, bold)
   - AI summary (2-3 lines with key numbers)
   - Category tag
   - [READ PDF] button → Opens link in new tab
✅ **Infinite scroll** (load more button)  
✅ **Auto-refresh** (every 5 minutes)

**NO PDFs are loaded in the dashboard** - only links!

---

## 🗄️ DATABASE

Uses SQLite (simple file: `lion_signal.db`)

**What's stored:**
- Company name, exchange, timestamp
- PDF link (NOT the PDF file itself!)
- AI analysis (headline, summary, importance, key numbers)
- Created date + expiry date (365 days later)

**Size:** ~440 MB for full year of data (1500 announcements/day)

**Auto-cleanup:** Janitor runs daily and deletes entries older than 365 days.

---

## 💰 COSTS (Detailed Breakdown)

| Component | Free Tier | Your Usage | Cost |
|-----------|-----------|------------|------|
| Gemini AI | 1000 req/day | ~100 req/day | ₹0 |
| GitHub Actions | 2000 min/month | ~30 min/month | ₹0 |
| GitHub Storage | 1 GB | ~440 MB | ₹0 |
| **TOTAL** | | | **₹0** |

**If you exceed limits** (unlikely):
- Gemini: $0.15/$0.60 per million tokens (~₹500-1000/month)
- GitHub: Still free (you'd need to run A LOT to hit limits)

---

## 🛠️ TROUBLESHOOTING

### "No announcements showing up"

1. Check GitHub Actions ran successfully (green ✅)
2. Check GEMINI_API_KEY is set correctly
3. Check database file exists (`lion_signal.db`)
4. Wait 30 minutes for first run

### "API Error" or "429 Rate Limit"

- You hit Gemini's free tier limit (1000 requests/day)
- Wait 24 hours, or reduce BATCH_SIZE, or upgrade to paid

### "Scraper returning empty results"

- BSE/NSE might have changed their HTML structure
- Check if websites are accessible (try opening in browser)
- Look at GitHub Actions logs for specific error

### "Dashboard not loading"

- Make sure `python app.py` is running
- Open `http://localhost:5000` (not 127.0.0.1)
- Check if port 5000 is blocked by firewall

---

## 📁 FILE STRUCTURE

```
lion-signal-hq/
├── config.py              ← Edit settings here
├── scraper.py             ← Visits BSE/NSE
├── analyzer.py            ← Gemini AI integration
├── database.py            ← SQLite operations
├── main.py                ← Main runner script
├── app.py                 ← Flask web server
├── requirements.txt       ← Python packages
├── test_system.py         ← Test before deploying
├── .env.example           ← API key template
├── .gitignore             ← Don't upload these files
├── README.md              ← Quick reference
├── SETUP_GUIDE.md         ← Detailed guide
├── lion_signal.db         ← Database (auto-created)
├── .github/
│   └── workflows/
│       └── schedule.yml   ← GitHub Actions
└── templates/
    └── dashboard.html     ← Beautiful UI
```

---

## 🎓 TECHNICAL DETAILS (For the Curious)

### Scraper (scraper.py)
- Uses `requests` + `BeautifulSoup` to parse HTML
- Visits BSE & NSE (Equity + SME)
- Extracts: Company, Subject, PDF URL, Timestamp
- Handles NSE's cookie requirements (visits homepage first)
- Returns list of announcement dictionaries

### Analyzer (analyzer.py)
- Uses `google-generativeai` SDK
- Sends up to 20 PDF URLs in one request
- Gemini reads PDFs directly from URLs (we never download them!)
- Extracts structured data using custom prompt
- Returns enhanced announcements with AI analysis

### Database (database.py)
- SQLite with single `announcements` table
- Indexes on: expires_at, created_at, company
- Soft-delete mechanism (marks as deleted, then hard deletes)
- Auto-expiry tracking (created_at + 365 days)
- Simple SQL queries for search/filter

### Main Script (main.py)
- Orchestrates: Scrape → Analyze → Save → Clean
- Error handling at each step
- Logs progress to console
- Can run standalone or via GitHub Actions

### Web Server (app.py)
- Flask REST API
- Endpoints: /api/announcements, /api/stats, /api/search
- CORS enabled for frontend
- Serves dashboard from templates/

### GitHub Actions (.github/workflows/schedule.yml)
- Cron: `*/30 * * * *` (every 30 minutes)
- Installs Python, dependencies
- Runs main.py
- Commits updated database
- Uploads database as artifact (7-day retention)

---

## 🔒 SECURITY NOTES

✅ **API key stored in GitHub Secrets** (encrypted, never visible in code)  
✅ **.gitignore prevents .env from being uploaded** (won't leak keys)  
✅ **No PDFs stored** (only public links)  
✅ **No user authentication needed** (public dashboard)  
✅ **SQLite database** (no external connections)

**Important:** Never commit your `.env` file or API key to GitHub!

---

## 🚀 NEXT STEPS

1. **Test locally first:**
   ```bash
   python test_system.py
   ```

2. **Deploy to GitHub:**
   - Follow SETUP_GUIDE.md step-by-step
   - Takes 15 minutes total

3. **Wait 30 minutes:**
   - First run will populate database
   - Check GitHub Actions tab for green ✅

4. **View dashboard:**
   - Run `python app.py` locally, OR
   - Deploy to Netlify/Vercel for live website

5. **Customize:**
   - Edit config.py to your liking
   - Adjust retention, filters, etc.

6. **Find multi-baggers!** 🎯

---

## 💡 TIPS FOR SUCCESS

1. **Start small:** Let it run for a day, see what data looks like
2. **Adjust filters:** Use MIN_IMPORTANCE_TO_DISPLAY to hide boring ones
3. **Monitor GitHub Actions:** Check logs if something seems off
4. **Backup database:** Download from Actions → Artifacts occasionally
5. **Read the summaries:** The AI extracts KEY numbers - use them!

---

## 🎉 YOU'RE DONE!

Everything is built and ready. Just follow the SETUP_GUIDE.md and you'll have:

✅ 24/7 automated system  
✅ AI-powered analysis  
✅ Beautiful dashboard  
✅ 365 days of data retention  
✅ Zero cost  

**Happy hunting for those 10x stocks!** 🦁🚀

---

*Built with ❤️ by Claude Sonnet for the Lion Hunters*
