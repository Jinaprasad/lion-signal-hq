import sqlite3
from datetime import datetime

def main():
    print("🦁 LION SIGNAL: STABILIZING...")
    conn = sqlite3.connect('lion_signal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exchange TEXT, company TEXT, symbol TEXT, subject TEXT, 
            pdf_link TEXT, timestamp TEXT, scraped_at TEXT, 
            ai_company TEXT, ai_headline TEXT, ai_category TEXT, 
            ai_importance INTEGER, ai_summary TEXT, ai_key_numbers TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ SYSTEM STABLE")

if __name__ == "__main__":
    main()
