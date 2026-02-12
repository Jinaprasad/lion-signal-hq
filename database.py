"""
🦁 LION SIGNAL HQ - Database Manager
=====================================
This is the NOTEBOOK that remembers everything.

It saves all the summaries and automatically deletes old ones after 365 days.
"""

import sqlite3
from datetime import datetime, timedelta
import json
from config import *

class Database:
    """
    The Smart Notebook that saves and retrieves announcements
    """
    
    def __init__(self, db_path=DATABASE_NAME):
        """
        Open the notebook (database)
        
        Args:
            db_path: Where to save the database file
        """
        print(f"📓 Opening database: {db_path}")
        
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # Returns rows as dictionaries
        
        # Create tables if they don't exist
        self._create_tables()
        
        print("✅ Database ready!")
    
    def _create_tables(self):
        """Create the database tables"""
        
        cursor = self.connection.cursor()
        
        # Main announcements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange TEXT NOT NULL,
                company TEXT NOT NULL,
                symbol TEXT,
                subject TEXT,
                pdf_link TEXT UNIQUE NOT NULL,
                timestamp TEXT,
                scraped_at TEXT NOT NULL,
                
                -- AI Analysis fields
                ai_company TEXT,
                ai_headline TEXT,
                ai_category TEXT,
                ai_importance INTEGER DEFAULT 5,
                ai_summary TEXT,
                ai_key_numbers TEXT,
                
                -- Auto-delete tracking
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                
                -- Metadata
                is_deleted INTEGER DEFAULT 0
            )
        """)
        
        # Index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expires 
            ON announcements(expires_at)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created 
            ON announcements(created_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_company 
            ON announcements(company)
        """)
        
        self.connection.commit()
        
        print("  ✅ Database tables ready")
    
    def add_announcement(self, announcement):
        """
        Save one announcement to the database
        
        Args:
            announcement: Dictionary with announcement data
        
        Returns:
            True if saved, False if duplicate
        """
        
        cursor = self.connection.cursor()
        
        # Calculate expiry date (365 days from now)
        now = datetime.now()
        expires = now + timedelta(days=RETENTION_DAYS)
        
        try:
            cursor.execute("""
                INSERT INTO announcements (
                    exchange, company, symbol, subject, pdf_link, timestamp,
                    scraped_at, ai_company, ai_headline, ai_category,
                    ai_importance, ai_summary, ai_key_numbers,
                    created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                announcement.get('exchange', 'Unknown'),
                announcement.get('company', 'Unknown'),
                announcement.get('symbol', ''),
                announcement.get('subject', ''),
                announcement['pdf_link'],  # Required!
                announcement.get('timestamp', ''),
                announcement.get('scraped_at', now.isoformat()),
                announcement.get('ai_company', announcement.get('company', 'Unknown')),
                announcement.get('ai_headline', announcement.get('subject', '')),
                announcement.get('ai_category', 'OTHER'),
                announcement.get('ai_importance', 5),
                announcement.get('ai_summary', ''),
                announcement.get('ai_key_numbers', ''),
                now.isoformat(),
                expires.isoformat()
            ))
            
            self.connection.commit()
            return True
            
        except sqlite3.IntegrityError:
            # Duplicate PDF link - skip it
            return False
    
    def add_announcements_batch(self, announcements):
        """
        Save multiple announcements
        
        Args:
            announcements: List of announcement dictionaries
        
        Returns:
            Number of announcements saved (excluding duplicates)
        """
        
        saved_count = 0
        duplicate_count = 0
        
        for ann in announcements:
            if self.add_announcement(ann):
                saved_count += 1
            else:
                duplicate_count += 1
        
        print(f"💾 Saved {saved_count} new announcements ({duplicate_count} duplicates skipped)")
        
        return saved_count
    
    def get_recent_announcements(self, limit=100, min_importance=None):
        """
        Get recent announcements for display
        
        Args:
            limit: How many to return
            min_importance: Only show announcements with importance >= this
        
        Returns:
            List of announcements (newest first)
        """
        
        cursor = self.connection.cursor()
        
        query = """
            SELECT * FROM announcements 
            WHERE is_deleted = 0
        """
        
        params = []
        
        if min_importance:
            query += " AND ai_importance >= ?"
            params.append(min_importance)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        return [dict(row) for row in rows]
    
    def search_announcements(self, search_term, exchange=None, category=None):
        """
        Search announcements
        
        Args:
            search_term: Search in company name, headline, summary
            exchange: Filter by exchange (BSE, NSE, NSE-SME)
            category: Filter by category
        
        Returns:
            List of matching announcements
        """
        
        cursor = self.connection.cursor()
        
        query = """
            SELECT * FROM announcements 
            WHERE is_deleted = 0
            AND (
                company LIKE ? OR 
                ai_company LIKE ? OR
                ai_headline LIKE ? OR
                ai_summary LIKE ?
            )
        """
        
        search_pattern = f"%{search_term}%"
        params = [search_pattern, search_pattern, search_pattern, search_pattern]
        
        if exchange:
            query += " AND exchange = ?"
            params.append(exchange)
        
        if category:
            query += " AND ai_category = ?"
            params.append(category)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def delete_expired(self):
        """
        Delete announcements older than RETENTION_DAYS
        
        This runs automatically - it's the JANITOR!
        
        Returns:
            Number of announcements deleted
        """
        
        cursor = self.connection.cursor()
        
        now = datetime.now().isoformat()
        
        # Mark as deleted (soft delete)
        cursor.execute("""
            UPDATE announcements 
            SET is_deleted = 1 
            WHERE expires_at < ? AND is_deleted = 0
        """, (now,))
        
        deleted_count = cursor.rowcount
        
        # Actually delete them from database (hard delete)
        cursor.execute("""
            DELETE FROM announcements 
            WHERE is_deleted = 1
        """)
        
        self.connection.commit()
        
        if deleted_count > 0:
            print(f"🗑️ JANITOR: Deleted {deleted_count} expired announcements (older than {RETENTION_DAYS} days)")
        else:
            print("🗑️ JANITOR: No expired announcements to delete")
        
        return deleted_count
    
    def get_stats(self):
        """
        Get database statistics
        
        Returns:
            Dictionary with stats
        """
        
        cursor = self.connection.cursor()
        
        # Total active announcements
        cursor.execute("SELECT COUNT(*) FROM announcements WHERE is_deleted = 0")
        total = cursor.fetchone()[0]
        
        # By exchange
        cursor.execute("""
            SELECT exchange, COUNT(*) 
            FROM announcements 
            WHERE is_deleted = 0 
            GROUP BY exchange
        """)
        by_exchange = dict(cursor.fetchall())
        
        # Today's count
        today = datetime.now().date().isoformat()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM announcements 
            WHERE is_deleted = 0 
            AND DATE(created_at) = ?
        """, (today,))
        today_count = cursor.fetchone()[0]
        
        # Oldest and newest
        cursor.execute("""
            SELECT MIN(created_at), MAX(created_at) 
            FROM announcements 
            WHERE is_deleted = 0
        """)
        oldest, newest = cursor.fetchone()
        
        return {
            'total': total,
            'by_exchange': by_exchange,
            'today': today_count,
            'oldest': oldest,
            'newest': newest,
            'retention_days': RETENTION_DAYS
        }
    
    def close(self):
        """Close the database connection"""
        self.connection.close()
        print("📓 Database closed")


# Test if run directly
if __name__ == "__main__":
    print("Testing database...")
    
    # Create database
    db = Database()
    
    # Test adding announcement
    test_ann = {
        'exchange': 'BSE',
        'company': 'Test Company',
        'pdf_link': 'https://example.com/test123.pdf',
        'ai_headline': 'TEST ANNOUNCEMENT',
        'ai_summary': 'This is a test',
        'ai_importance': 8
    }
    
    db.add_announcement(test_ann)
    
    # Get stats
    stats = db.get_stats()
    print("\nDatabase Stats:")
    print(json.dumps(stats, indent=2))
    
    # Get recent
    recent = db.get_recent_announcements(limit=5)
    print(f"\nFound {len(recent)} recent announcements")
    
    # Close
    db.close()
