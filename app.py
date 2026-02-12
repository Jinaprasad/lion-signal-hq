from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from database import Database
from config import *
import os

app = Flask(__name__)
CORS(app)

db = None

def get_db():
    global db
    if db is None:
        db = Database()
    return db

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/announcements')
def get_announcements():
    db = get_db()
    limit = request.args.get('limit', 50, type=int)
    # FORCED TO 0 TO ENSURE CARDS SHOW UP
    min_importance = 0 
    
    results = db.get_recent_announcements(
        limit=limit,
        min_importance=min_importance
    )
    return jsonify(results)

@app.route('/api/stats')
def get_stats():
    db = get_db()
    return jsonify(db.get_stats())

@app.teardown_appcontext
def close_db(error):
    global db
    if db is not None:
        db.close()
        db = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
