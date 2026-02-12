# 🦁 LION SIGNAL HQ - SETUP GUIDE FOR 5-YEAR-OLDS
## (No Tech Knowledge Required!)

---

## 📋 WHAT YOU'LL NEED (5 minutes to collect)

✅ A computer (Windows, Mac, or Linux)  
✅ An email address  
✅ 15 minutes of your time  

**That's it!** No coding knowledge needed.

---

## 🎯 THE PLAN (What We're Building)

```
You → Upload files to GitHub → GitHub runs it 24/7 → You see results on dashboard

Simple!
```

---

## 🚀 STEP-BY-STEP GUIDE

### 🔑 STEP 1: GET YOUR GEMINI API KEY (5 minutes)

**What is this?** It's like a password that lets you use Google's free AI.

**How to get it:**

1. Open your browser
2. Go to: **https://aistudio.google.com/apikey**
3. Click the blue **"Create API Key"** button
4. Click **"Create API key in new project"**
5. You'll see a long key that starts with `AIza...`
6. Click the **copy icon** (two overlapping squares)
7. Paste it in a notepad - you'll need this later!

✅ **Done! You got your free AI key!**

---

### 👤 STEP 2: CREATE GITHUB ACCOUNT (3 minutes)

**What is GitHub?** It's like Google Drive, but for code. It will run your system 24/7 for FREE.

**How to sign up:**

1. Go to: **https://github.com**
2. Click green **"Sign up"** button (top right)
3. Enter your email
4. Create a password (write it down!)
5. Create a username (anything you like)
6. Solve the puzzle (prove you're human)
7. Click **"Create account"**
8. Check your email and verify

✅ **Done! You have a GitHub account!**

---

### 📁 STEP 3: CREATE YOUR PROJECT (2 minutes)

**Now we'll create a home for your LION SIGNAL HQ:**

1. You should be on GitHub homepage now
2. Look for the **green "New"** button (top left, near your profile picture)
3. Click it
4. You'll see "Create a new repository" page
5. In the "Repository name" box, type: **lion-signal-hq**
6. Leave everything else as-is (don't touch anything!)
7. Scroll down and click the green **"Create repository"** button

✅ **Done! Your project home is ready!**

---

### 📤 STEP 4: UPLOAD THE FILES (5 minutes)

**Now we put all the code files into your GitHub project:**

1. You should see your empty repository now
2. Look for text that says "uploading an existing file" (it's a link)
3. Click on **"uploading an existing file"**
4. Now **drag and drop ALL these files** into the box:
   ```
   config.py
   scraper.py
   analyzer.py
   database.py
   main.py
   app.py
   requirements.txt
   test_system.py
   README.md
   .env.example
   .gitignore
   ```
5. Also upload the **folders** (drag the whole folder):
   ```
   .github/
   templates/
   ```
6. Wait for all files to upload (you'll see them listed)
7. Scroll to bottom and click green **"Commit changes"** button

✅ **Done! All code is uploaded!**

---

### 🔐 STEP 5: ADD YOUR SECRET API KEY (3 minutes)

**This is important! We're giving GitHub your Gemini API key (but keeping it secret):**

1. In your repository, click the **"Settings"** tab (top right area)
2. On the left sidebar, look for **"Secrets and variables"**
3. Click on it, then click **"Actions"**
4. You'll see a page with "Repository secrets"
5. Click the green **"New repository secret"** button
6. In the "Name" field, type exactly: **GEMINI_API_KEY**
7. In the "Secret" field, paste your API key from Step 1 (the one starting with `AIza...`)
8. Click green **"Add secret"** button
9. You should see "GEMINI_API_KEY" in the list now

✅ **Done! Your API key is safely stored!**

---

### ▶️ STEP 6: START THE SYSTEM! (2 minutes)

**Let's wake up the LION!**

1. Click the **"Actions"** tab (top of the page)
2. You might see a message "Workflows aren't being run on this repository"
   - If you see this, click the green **"I understand my workflows, go ahead and enable them"** button
3. On the left sidebar, click **"Lion Signal Scraper"**
4. On the right side, click the gray **"Run workflow"** dropdown
5. Click the green **"Run workflow"** button
6. Wait 5 seconds, then refresh the page
7. You should see a yellow dot 🟡 (it's running!)
8. Wait 2-3 minutes
9. Refresh again - it should turn green ✅

✅ **Done! Your system is ALIVE!**

---

### 🎉 STEP 7: SEE THE RESULTS! (ongoing)

**Two ways to see your announcements:**

#### Option A: Download Database and Run Locally

1. Go to **"Actions"** tab
2. Click on the latest successful run (green ✅)
3. Scroll to bottom - you'll see "Artifacts"
4. Download **lion-signal-database**
5. Extract the .db file
6. On your computer, run:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
7. Open browser to: **http://localhost:5000**
8. 🎊 See your beautiful dashboard!

#### Option B: Deploy to Free Website (Advanced)

We can do this next if you want a live website!

---

## 🎯 WHAT HAPPENS NOW?

Your system is running 24/7 on GitHub for FREE:

```
Every 30 minutes:
  ↓
GitHub wakes up
  ↓
Visits BSE & NSE websites
  ↓
Finds new announcements (PDF links)
  ↓
Sends 20 links to Gemini AI
  ↓
Gemini reads PDFs and extracts:
  • Company name
  • Important headline
  • Key numbers (revenue, profit, orders)
  • 2-3 line smart summary
  ↓
Saves to database (only summaries, NOT PDFs!)
  ↓
Goes back to sleep for 30 minutes
  ↓
Repeats FOREVER (24/7)
```

After 365 days, old announcements auto-delete (keeps database clean).

---

## 📊 CHECKING IF IT'S WORKING

1. Go to **"Actions"** tab on GitHub
2. You should see runs every 30 minutes
3. Green ✅ = Working perfectly!
4. Red ❌ = Something wrong (click to see error)

**Common issues:**
- Red X = API key wrong or missing
- No runs = GitHub Actions not enabled
- Yellow dot for long time = BSE/NSE website slow (normal)

---

## 🛠️ MAKING CHANGES

Want to change settings? Easy!

1. Click on **config.py** in your repository
2. Click the ✏️ pencil icon (edit)
3. Change the numbers:
   ```python
   RETENTION_DAYS = 365  # Change to 7, 30, 90, 1000, etc.
   BATCH_SIZE = 20       # Keep at 20 (works best)
   ```
4. Scroll down, click **"Commit changes"**
5. Done! It will use new settings on next run.

---

## 💰 COSTS

Everything is **FREE**:

- ✅ Gemini AI: Free (1000 requests/day = plenty!)
- ✅ GitHub Actions: Free (2000 minutes/month = plenty!)
- ✅ GitHub Storage: Free (1 GB = plenty!)

**If you exceed limits** (very rare):
- Gemini: Might need to pay ~₹500/month
- But with 20 PDF batches, you'll stay in free tier!

---

## 🆘 NEED HELP?

**If something doesn't work:**

1. Check GitHub Actions logs:
   - Actions tab → Click failed run → See error message
   
2. Common fixes:
   - API key wrong? Re-add it in Settings → Secrets
   - No data? Wait 30 minutes for first run
   - Red errors? Read the error message (it usually tells you what's wrong!)

3. Read the code comments - they explain everything!

---

## 🎓 WHAT YOU LEARNED

Congrats! You just:

✅ Set up a cloud automation system  
✅ Integrated with AI (Gemini)  
✅ Built a web scraper  
✅ Created an automated database  
✅ Deployed to production (GitHub Actions)  

**You're not a tech person? YOU ARE NOW!** 🎉

---

## 🦁 HAPPY HUNTING!

Your LION is now hunting for multi-baggers 24/7 while you sleep!

**Next time you check:**
- Hundreds of analyzed announcements ready
- Smart summaries with key numbers
- Just scroll and find the gems!

**Good luck finding those 10x stocks!** 🚀

---

*Made with ❤️ for non-tech multi-bagger hunters*
