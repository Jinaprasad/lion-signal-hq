# 🦁 LION SIGNAL HQ

**Find multi-bagger stocks BEFORE everyone else!**

This system automatically scrapes BSE & NSE announcements every 30 minutes, analyzes them with AI, and shows you what matters on a beautiful dashboard.

---

## 🎯 What It Does

```
Every 30 minutes (24/7):
1. 🔍 Scrapes BSE & NSE for new announcements
2. 🧠 Sends 20 PDF links to Gemini AI  
3. 💾 Saves smart summaries (NOT the PDFs!)
4. 🗑️ Auto-deletes data after 365 days
5. 📊 Shows everything on beautiful dashboard
```

**Cost: ₹0** (Gemini free tier + GitHub free)

---

## 🚀 SUPER SIMPLE SETUP (15 Minutes)

### Step 1: Get Gemini API Key (5 min)

1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. ✅ Done!

### Step 2: Create GitHub Account (2 min)

1. Go to: https://github.com
2. Click "Sign Up"  
3. Enter email, create password
4. ✅ Done!

### Step 3: Upload Files to GitHub (5 min)

1. Click the green **"+ New"** button (top right)
2. Name it: `lion-signal-hq`
3. Click **"Create repository"**
4. Click **"uploading an existing file"** link
5. Drag ALL these files into the box:
   ```
   config.py
   scraper.py
   analyzer.py
   database.py
   main.py
   app.py
   requirements.txt
   .github/workflows/schedule.yml
   templates/dashboard.html
   ```
6. Click **"Commit changes"**
7. ✅ Done!

### Step 4: Add Your API Key (3 min)

1. In your repository, click **"Settings"** tab
2. Click **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**
4. Name: `GEMINI_API_KEY`
5. Value: (paste your Gemini API key from Step 1)
6. Click **"Add secret"**
7. ✅ Done!

### Step 5: Start It! (1 min)

1. Click **"Actions"** tab
2. Click **"Lion Signal Scraper"** 
3. Click **"Run workflow"** button
4. Click green **"Run workflow"**
5. Wait 2 minutes
6. ✅ It's running!

---

## 🌐 See Your Dashboard

### Option A: Run Locally (On Your Computer)

```bash
# Install Python packages
pip install -r requirements.txt

# Run the web server
python app.py

# Open browser to: http://localhost:5000
```

### Option B: Deploy to Free Hosting

**Netlify (Easiest):**
1. Go to netlify.com
2. Click "Add new site" → "Import from GitHub"
3. Select your `lion-signal-hq` repo
4. Deploy!

**Your dashboard will be live at:** `lion-signal-hq.netlify.app`

---

## 📊 What You'll See

Your dashboard shows:

```
🦁 LION SIGNAL HQ                    🌙 Dark Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Search: [___________]  Filter: [All ▼]

🟢 CONCORD BIOTECH                         BSE
   Q3 INVESTOR PRESENTATION
   Revenue growth robust, 6 APIs filed...
   📄 READ PDF  12-Feb-2026 00:45

🟢 HDFC BANK                               NSE
   RBI APPROVAL - ICICI ACQUISITION
   ICICI Prudential granted 9.95% holding...
   📄 READ PDF  12-Feb-2026 00:30
```

✅ Light/Dark mode toggle  
✅ Search by company  
✅ Filter by exchange (BSE/NSE)  
✅ Only shows LINKS (click to open PDF)  
✅ Auto-updates every 30 min  

---

## ⚙️ Settings You Can Change

Edit `config.py`:

```python
RETENTION_DAYS = 365  # Change to 7, 30, 90, 365, 1000, etc.
BATCH_SIZE = 20       # PDFs per Gemini request
UPDATE_FREQUENCY_MINUTES = 30  # How often to scrape
```

---

## 🛠️ How It Works (Behind The Scenes)

```
GitHub Actions (Free Robot)
    ↓
Every 30 minutes:
    ↓
1. scraper.py → Visits BSE/NSE websites
    ↓
2. Finds new announcement PDF links
    ↓
3. analyzer.py → Sends 20 links to Gemini
    ↓
4. Gemini reads PDFs and extracts:
   - Company name
   - Headline
   - Important numbers (revenue, profit, orders)
   - 2-3 line summary
    ↓
5. database.py → Saves summaries
   (NOT the PDFs - just links!)
    ↓
6. Janitor → Deletes anything older than 365 days
    ↓
7. app.py → Shows on dashboard
    ↓
Sleeps for 30 minutes → Repeats
```

---

## 📁 File Structure

```
lion-signal-hq/
├── config.py              # Settings (EDIT THIS!)
├── scraper.py             # The scout (visits websites)
├── analyzer.py            # The brain (Gemini AI)
├── database.py            # The notebook (SQLite)
├── main.py                # The conductor (runs everything)
├── app.py                 # Web server (Flask)
├── requirements.txt       # Python packages needed
├── lion_signal.db         # Database (auto-created)
├── .github/
│   └── workflows/
│       └── schedule.yml   # GitHub Actions (runs every 30 min)
└── templates/
    └── dashboard.html     # The beautiful dashboard
```

---

## ❓ Troubleshooting

### "No announcements showing up"

1. Check GitHub Actions ran successfully:
   - Go to "Actions" tab
   - See if latest run is ✅ green
   
2. Check API key is set:
   - Settings → Secrets → GEMINI_API_KEY should exist

3. Check database file exists:
   - Look for `lion_signal.db` in your repository

### "Gemini API error"

- You might have hit the free tier limit (1000 requests/day)
- Wait 24 hours, or upgrade to paid tier ($0.30/M tokens)

### "Website not loading"

- Make sure you ran `python app.py`
- Open browser to `http://localhost:5000` (not 127.0.0.1)
- Check firewall isn't blocking port 5000

---

## 💰 Costs

| Item | Cost |
|------|------|
| Gemini API (Free Tier) | ₹0 |
| GitHub Actions | ₹0 |
| GitHub Storage | ₹0 |
| Hosting (Netlify/Vercel) | ₹0 |
| **TOTAL** | **₹0** |

**If you exceed free tiers:**
- Gemini: ~₹500-1000/month for heavy usage
- Hosting: ₹300-500/month for premium

---

## 🎉 You're Done!

The system is now running 24/7:
- ✅ Scraping BSE & NSE every 30 minutes
- ✅ Analyzing with AI
- ✅ Storing smart summaries
- ✅ Auto-deleting after 365 days
- ✅ Beautiful dashboard

**Find those multi-baggers!** 🦁🚀

---

## 📞 Need Help?

- Read the code comments (they're in 5-year-old language!)
- Check GitHub Actions logs for errors
- All files are heavily commented

**Happy hunting!** 🦁
