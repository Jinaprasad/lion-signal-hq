"""
🦁 LION SIGNAL HQ - Configuration File
=====================================
This is where you control ALL the settings!

Change numbers here, everything else adjusts automatically.
"""

# ========================================
# HOW LONG TO KEEP DATA
# ========================================
RETENTION_DAYS = 365  # ← Change this number anytime! (7, 30, 90, 365, etc.)

# ========================================
# HOW OFTEN TO CHECK FOR NEW ANNOUNCEMENTS
# ========================================
UPDATE_FREQUENCY_MINUTES = 30  # Every 30 minutes

# ========================================
# HOW MANY PDF LINKS TO SEND TO GEMINI AT ONCE
# ========================================
BATCH_SIZE = 20  # Send 20 PDF links together

# ========================================
# BSE WEBSITE URLS
# ========================================
BSE_ANNOUNCEMENTS_URL = "https://www.bseindia.com/corporates/ann.html"

# ========================================
# NSE WEBSITE URLS
# ========================================
NSE_EQUITY_URL = "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
NSE_SME_URL = "https://www.nseindia.com/emerge-companies-listing/corporate-filings-announcements"

# ========================================
# GEMINI AI SETTINGS
# ========================================
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Free tier model
GEMINI_MAX_RETRIES = 3  # Try 3 times if it fails
GEMINI_TIMEOUT = 60  # Wait 60 seconds max

# ========================================
# DATABASE SETTINGS
# ========================================
DATABASE_NAME = "lion_signal.db"  # SQLite database file
MAX_ANNOUNCEMENTS_PER_PAGE = 50  # Show 50 at a time on dashboard

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

Rules:
- If announcement is generic/boring (like "Loss of Share Certificate"), mark importance as 1
- Focus on ACTIONABLE financial data
- Convert all values to Crores (Cr) for consistency
- Be dense and factual, no fluff
- If no financial data available, still provide context

Output format for each:
---
COMPANY: [Name]
HEADLINE: [Specific headline]
CATEGORY: [Category]
IMPORTANCE: [1-10]
SUMMARY: [2-3 line forensic analysis]
KEY_NUMBERS: [Revenue: X Cr, Profit: Y Cr, etc. OR "None"]
---
"""

# ========================================
# FILTERING KEYWORDS (Optional - not used yet)
# ========================================
HIGH_PRIORITY_KEYWORDS = [
    "revenue", "profit", "ebitda", "order", "contract",
    "acquisition", "merger", "dividend", "results",
    "growth", "expansion", "loan", "funding"
]

SKIP_KEYWORDS = [
    "loss of share certificate",
    "change of address",
    "loss of certificate",
    "duplicate share"
]

# ========================================
# DISPLAY SETTINGS
# ========================================
MIN_IMPORTANCE_TO_DISPLAY = 1  # Show all (change to 5 to filter out boring ones)
SHOW_BSE = True
SHOW_NSE = True
SHOW_NSE_SME = True

# ========================================
# THAT'S IT! 
# ========================================
# Everything else is automatic!
# Just change numbers above and the system adapts.
