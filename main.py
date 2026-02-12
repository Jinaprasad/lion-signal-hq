import os
import sys
from datetime import datetime
from scraper import AnnouncementScraper
from database import Database
from config import *

def main():
    print("🦁 LION SIGNAL: FETCHING REAL DATA")
    db = Database()
    scraper = AnnouncementScraper()
    
    # 1. Get real data from BSE/NSE
    real_announcements = scraper.scrape_all()
    
    if not real_announcements:
        print("⚠️ No live news found at this second. Keeping pipeline warm.")
        return

    # 2. Fill AI fields with placeholders (Bypassing Gemini for stability)
    for ann in real_announcements:
        ann['ai_company'] = ann['company'].upper()
        ann['ai_headline'] = ann['subject'].upper()
        ann['ai_importance'] = 5  # Neutral score
        ann['ai_summary'] = "RAW FEED: AI Analysis is currently being re-linked."
        ann['ai_category'] = "GENERAL"
        ann['ai_key_numbers'] = "None"

    # 3. Save to Database
    print(f"💾 Saving {len(real_announcements)} real stocks to database...")
    saved_count = db.add_announcements_batch(real_announcements)
    
    db.close()
    print(f"✅ SUCCESS: {saved_count} new stocks live.")

if __name__ == "__main__":
    main()
