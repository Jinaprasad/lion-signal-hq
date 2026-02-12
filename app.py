from flask import Flask, render_template, jsonify
from database import Database
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/announcements')
def get_announcements():
    db = Database()
    # Pull everything, ignore all filters
    results = db.get_recent_announcements(limit=100, min_importance=0)
    db.close()
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
