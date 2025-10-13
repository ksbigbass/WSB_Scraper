from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

from reddit_scraper import analyze_subreddit

app = Flask(__name__)


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
    # Allow overriding port via FLASK_RUN_PORT environment variable for testing
    import os
    port = int(os.getenv('FLASK_RUN_PORT', os.getenv('PORT', '5000')))
    app.run(debug=True, port=port)