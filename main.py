"""
🦁 LION SIGNAL HQ - Main Script
================================
This is the CONDUCTOR that makes everything work together!
FIXED: 22:15 DEADLINE VERSION
"""

import os
import sys
from datetime import datetime
from scraper import AnnouncementScraper
from analyzer import GeminiAnalyzer, analyze_in_batches
from database import Database
from config import *

def main():
    """
    Main function that runs the whole show!
    """
    
    print("\n" + "="*60)
    print("🦁 LION SIGNAL HQ - STARTING RUN")
    print("="*60)
    print(f"⏰ Time: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}")
    print(f"📅 Retention: {RETENTION_DAYS} days")
    print("="*60 + "\n")
    
    # ========================================
    # STEP 1: Get Gemini API Key
    # ========================================
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not set!")
        sys.exit(1)
    
    print("✅ Gemini API key found\n")
    
    # ========================================
    # STEP 2: Open Database
    # ========================================
    
    db = Database()
    
    # Show current stats
    stats = db.get_stats()
    print(f"📊 Current database: {stats['total']} announcements")
    
    # ========================================
    # STEP 3: Clean Up Old Data (Janitor)
    # ========================================
    
    print("🗑️ Running cleanup...")
    deleted = db.delete_expired()
    
    # ========================================
    # STEP 4: Scrape New Announcements (Scout)
    # ========================================
    
    scraper = AnnouncementScraper()
    new_announcements = scraper.scrape_all()
    
    # FORCED DEBUG: Ensure something shows on Render even if Scraper is empty
    if not new_announcements:
        print("⚠️ No real news found. Injecting TEST SUCCESS CORP for pipeline check...")
        new_announcements = [{
            'exchange': 'DEBUG',
            'company': 'TEST SUCCESS CORP',
            'symbol': 'SUCCESS',
            'subject': 'SYSTEM PIPELINE ACTIVE',
            'pdf_link': 'https://www.bseindia.com',
            'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }]
    
    # ========================================
    # STEP 5: Analyze with Gemini (Brain)
    # ========================================
    
    analyzed = analyze_in_batches(new_announcements, api_key)
    
    # ========================================
    # STEP 6: Save to Database (Notebook)
    # ========================================
    
    print("\n💾 Saving to database...")
    saved_count = db.add_announcements_batch(analyzed)
    
    # ========================================
    # STEP 7: Summary Report
    # ========================================
    
    print("\n" + "="*60)
    print("✅ RUN COMPLETE!")
    print(f"📥 Scraped: {len(new_announcements)} announcements")
    print(f"🧠 Analyzed: {len(analyzed)} announcements")
    print(f"💾 Saved: {saved_count} new")
    print("="*60 + "\n")
    
    # ========================================
    # STEP 9: Close Database (CRITICAL FOR GITHUB PUSH)
    # ========================================
    
    db.close()
    print("🦁 LION SIGNAL HQ - Run complete!")

if __name__ == "__main__":
    try:
        main()
