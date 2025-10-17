from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import prawcore
from counters import potential_stock_symbols

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols', methods=['GET'])
def symbols():
    try:
        subreddit = request.args.get('subreddit', 'wallstreetbets')
        limit = int(request.args.get('limit', 100))
        data = potential_stock_symbols(subreddit, limit)
        return render_template('results.html', **data)
    except EnvironmentError as ee:
        return render_template('error.html', error=str(ee))
    except prawcore.exceptions.ResponseException as e:
        status = getattr(e.response, 'status_code', 500)
        return render_template('error.html', error=f'Reddit API error ({status})')
    except Exception as ex:
        app.logger.exception('Symbols route error')
        return render_template('error.html', error='Internal server error')

if __name__ == '__main__':
    app.run(debug=True)