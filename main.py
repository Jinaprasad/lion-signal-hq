"""
🦁 LION SIGNAL HQ - Main Script
================================
This is the CONDUCTOR that makes everything work together!

It runs every 30 minutes and:
1. Scrapes BSE/NSE for new announcements (Scout)
2. Sends them to Gemini for analysis (Brain)  
3. Saves to database (Notebook)
4. Cleans up old data (Janitor)
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
        print("\n📝 How to fix:")
        print("   1. Go to https://aistudio.google.com/apikey")
        print("   2. Create a free API key")
        print("   3. Set it as environment variable:")
        print("      - Linux/Mac: export GEMINI_API_KEY='your-key-here'")
        print("      - Windows: set GEMINI_API_KEY=your-key-here")
        print("      - GitHub Actions: Add it in repository secrets")
        sys.exit(1)
    
    print("✅ Gemini API key found\n")
    
    # ========================================
    # STEP 2: Open Database
    # ========================================
    
    db = Database()
    
    # Show current stats
    stats = db.get_stats()
    print(f"📊 Current database: {stats['total']} announcements")
    print(f"   - Today: {stats['today']} new")
    print(f"   - By exchange: {stats['by_exchange']}\n")
    
    # ========================================
    # STEP 3: Clean Up Old Data (Janitor)
    # ========================================
    
    print("🗑️ Running cleanup...")
    deleted = db.delete_expired()
    print()
    
    # ========================================
    # STEP 4: Scrape New Announcements (Scout)
    # ========================================
    
    scraper = AnnouncementScraper()
    new_announcements = scraper.scrape_all()
    
    if not new_announcements:
        print("⚠️ No new announcements found. Exiting.")
        db.close()
        return
    
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
    print("="*60)
    print(f"📥 Scraped: {len(new_announcements)} announcements")
    print(f"🧠 Analyzed: {len(analyzed)} announcements")
    print(f"💾 Saved: {saved_count} new (rest were duplicates)")
    print(f"🗑️ Deleted: {deleted} expired announcements")
    print(f"📊 Total in database: {db.get_stats()['total']} announcements")
    print("="*60 + "\n")
    
    # ========================================
    # STEP 8: Show Preview of Important Ones
    # ========================================
    
    print("🔥 TOP IMPORTANT ANNOUNCEMENTS:\n")
    
    important = db.get_recent_announcements(limit=5, min_importance=7)
    
    if important:
        for i, ann in enumerate(important, 1):
            print(f"{i}. {ann['ai_company']} (Importance: {ann['ai_importance']}/10)")
            print(f"   {ann['ai_headline']}")
            print(f"   💡 {ann['ai_summary'][:150]}...")
            print()
    else:
        print("   (No high-importance announcements found)\n")
    
    # ========================================
    # STEP 9: Close Database
    # ========================================
    
    db.close()
    
    print("🦁 LION SIGNAL HQ - Run complete!")
    print(f"⏰ Finished at: {datetime.now().strftime('%H:%M:%S')}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
