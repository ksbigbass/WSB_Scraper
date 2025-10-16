from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import praw
import re
import collections
from datetime import datetime

from reddit_scraper import analyze_subreddit

load_dotenv()  # Load environment variables from .env file if present

required_env_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
    print("Please create a .env file or export the required variables before running the app.")


app = Flask(__name__)

reddit= praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        subreddit = request.form.get('subreddit')
        if not subreddit:
            return jsonify({'status': 'error', 'message': 'Missing subreddit parameter'}), 400

        try:
            limit = int(request.form.get('limit', 100))
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid limit value'}), 400

        # Call the refactored scraper
        try:
            results = analyze_subreddit(subreddit, limit)
        except EnvironmentError as ee:
            return jsonify({'status': 'error', 'message': str(ee)}), 500
        except Exception as e:
            app.logger.exception('Scraper error')
            return jsonify({'status': 'error', 'message': 'Scraping failed'}), 500

        return jsonify({'status': 'success', 'data': results})

    except Exception as e:
        app.logger.exception('Error during analysis')
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
        
            # Allow overriding port via FLASK_RUN_PORT environment variable for testing
  