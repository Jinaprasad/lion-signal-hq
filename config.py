"""
🦁 LION SIGNAL HQ - Configuration File
=====================================
FIXED FOR LIVE DEPLOY - FEB 12
"""

# ========================================
# HOW LONG TO KEEP DATA
# ========================================
RETENTION_DAYS = 365

# ========================================
# HOW OFTEN TO CHECK FOR NEW ANNOUNCEMENTS
# ========================================
UPDATE_FREQUENCY_MINUTES = 30 

# ========================================
# THE "HUNT" WINDOW (NEW FIX)
# ========================================
# Force the scraper to look back 24 hours (1440 minutes)
LOOKBACK_WINDOW_MINUTES = 1440 

# ========================================
# BSE WEBSITE URLS
# ========================================
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"

# ========================================
# NSE API URLS (FIXED: FROM WEB PAGE TO DATA API)
# ========================================
NSE_EQUITY_URL = "https://www.nseindia.com/api/corporate-announcements?index=equities"
NSE_SME_URL = "https://www.nseindia.com/api/corporate-announcements?index=sme"

# ========================================
# GEMINI AI SETTINGS
# ========================================
BATCH_SIZE = 10  # Reduced to 10 for better precision
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_MAX_RETRIES = 3
GEMINI_TIMEOUT = 90  # Increased timeout for PDF reading

# ========================================
# DATABASE SETTINGS
# ========================================
DATABASE_NAME = "lion_signal.db"
MAX_ANNOUNCEMENTS_PER_PAGE = 50

# ========================================
# ANALYSIS PROMPT FOR GEMINI
# ========================================
ANALYSIS_PROMPT = """
You are a forensic financial analyst. Analyze these corporate announcements.

For EACH announcement, extract:
1. Company Name (clean, uppercase)
2. Headline (what is it about? be specific, uppercase)
3. Category (one of: RESULTS, ORDER, DIVIDEND, ACQUISITION, REGULATORY, GOVERNANCE, OTHER)
4. Importance Score (1-10, where 10 = critical multi-bagger signal)
5. Forensic Summary (2-3 lines max, include KEY NUMBERS like revenue, profit, order value)
6. Key Numbers (extract any: Revenue, Profit, EBITDA, Order Value, Dividend %, etc.)

Output format for each:
---
COMPANY: [Name]
HEADLINE: [Specific headline]
CATEGORY: [Category]
IMPORTANCE: [1-10]
SUMMARY: [Summary]
KEY_NUMBERS: [Numbers]
---
"""

# ========================================
# DISPLAY SETTINGS
# ========================================
MIN_IMPORTANCE_TO_DISPLAY = 1
SHOW_BSE = True
SHOW_NSE = True
SHOW_NSE_SME = True
