"""
🦁 LION SIGNAL HQ - Web Server
===============================
This serves the beautiful dashboard you saw earlier!

It's a simple Flask server that:
- Shows announcements from database
- Provides search & filter
- Serves the HTML/CSS/JS frontend
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from database import Database
from config import *
import os

app = Flask(__name__)
CORS(app)  # Allow requests from anywhere

# Global database connection
db = None

def get_db():
    """Get database connection"""
    global db
    if db is None:
        db = Database()
    return db

@app.route('/')
def index():
    """Main page - the dashboard"""
    return render_template('dashboard.html')

@app.route('/api/announcements')
def get_announcements():
    """
    API endpoint to get announcements
    
    Query params:
    - limit: How many to return (default 50)
    - search: Search term
    - exchange: Filter by exchange (BSE, NSE, NSE-SME)
    - category: Filter by category
    - min_importance: Minimum importance score
    """
    
    db = get_db()
    
    limit = request.args.get('limit', 50, type=int)
    search = request.args.get('search', '')
    exchange = request.args.get('exchange', '')
    category = request.args.get('category', '')
    min_importance = request.args.get('min_importance', MIN_IMPORTANCE_TO_DISPLAY, type=int)
    
    if search:
        # Search mode
        results = db.search_announcements(
            search_term=search,
            exchange=exchange if exchange else None,
            category=category if category else None
        )
    else:
        # Normal mode - get recent
        results = db.get_recent_announcements(
            limit=limit,
            min_importance=min_importance
        )
    
    # Filter by exchange if specified
    if exchange and not search:
        results = [r for r in results if r['exchange'] == exchange]
    
    # Filter by category if specified
    if category and not search:
        results = [r for r in results if r['ai_category'] == category]
    
    return jsonify(results)

@app.route('/api/stats')
def get_stats():
    """API endpoint to get database statistics"""
    db = get_db()
    stats = db.get_stats()
    return jsonify(stats)

@app.route('/api/search')
def search():
    """Search endpoint"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    db = get_db()
    results = db.search_announcements(search_term=query)
    
    return jsonify(results)

@app.teardown_appcontext
def close_db(error):
    """Close database when app shuts down"""
    global db
    if db is not None:
        db.close()
        db = None

if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("\n" + "="*60)
    print("🦁 LION SIGNAL HQ - Web Server")
    print("="*60)
    print("🌐 Starting server...")
    print("📱 Open in browser: http://localhost:5000")
    print("🔴 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Run the server
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,
        debug=False  # Set to True for development
    )
