import sqlite3
import json
from datetime import datetime

def emergency_run():
    print("🦁 LION SIGNAL: ABSOLUTE RECOVERY MODE")
    
    # 1. Force Open Database
    conn = sqlite3.connect('lion_signal.db')
    cursor = conn.cursor()
    
    # 2. Ensure Table Exists (Safety Check)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exchange TEXT,
            company TEXT,
            symbol TEXT,
            subject TEXT,
            pdf_link TEXT,
            timestamp TEXT,
            scraped_at TEXT,
            ai_company TEXT,
            ai_headline TEXT,
            ai_category TEXT,
            ai_importance INTEGER,
            ai_summary TEXT,
            ai_key_numbers TEXT
        )
    ''')

    # 3. Inject the Test Data
    test_data = [
        ('DEBUG', 'TEST SUCCESS CORP', 'SUCCESS', 'PIPELINE ACTIVE', 
         'https://www.bseindia.com', datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
         datetime.now().isoformat(), 'TEST SUCCESS CORP', 'SYSTEM IS LIVE', 
         'GENERAL', 10, 'The pipeline from GitHub to Render is now confirmed working.', 'None')
    ]

    cursor.executemany('''
        INSERT INTO announcements (
            exchange, company, symbol, subject, pdf_link, timestamp, 
            scraped_at, ai_company, ai_headline, ai_category, 
            ai_importance, ai_summary, ai_key_numbers
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', test_data)

    conn.commit()
    conn.close()
    print("✅ DATABASE JUMPSTARTED. Ready for Push.")

if __name__ == "__main__":
    emergency_run()
