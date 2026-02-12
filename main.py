import os
import sys
from datetime import datetime
from scraper import AnnouncementScraper
from database import Database
from config import *

def main():
    print("🦁 EMERGENCY RECOVERY START")
    db = Database()
    scraper = AnnouncementScraper()
    
    # Simple hunt - bypass AI to stop the crash
    new_announcements = scraper.scrape_all()
    
    if not new_announcements:
        print("⚠️ No news found. Injecting TEST SUCCESS CORP...")
        new_announcements = [{
            'exchange': 'DEBUG',
            'company': 'TEST SUCCESS CORP',
            'symbol': 'SUCCESS',
            'subject': 'PIPELINE RESTORED',
            'pdf_link': 'https://www.bseindia.com',
            'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }]

    # Fake the 'AI' fields so the database doesn't complain
    for ann in new_announcements:
        ann['ai_company'] = ann['company']
        ann['ai_headline'] = ann['subject']
        ann['ai_importance'] = 5
        ann['ai_summary'] = "Recovery Mode: AI Analysis bypassed to restore feed."
        ann['ai_category'] = "GENERAL"

    print(f"💾 Saving {len(new_announcements)} items...")
    db.add_announcements_batch(new_announcements)
    db.close()
    print("✅ RECOVERY COMPLETE")

if __name__ == "__main__":
    main()
