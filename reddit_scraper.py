# -*- coding: utf-8 -*-
import os
import re
import collections
import praw
from typing import Dict, Any, List
import prawcore
import flask

# Reuse known exclusions from counters if available
try:
       from counters import KNOWN_NOT_STOCKS
except Exception:
       KNOWN_NOT_STOCKS = ['PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST',
                                          'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO',
                                          'BELL', 'STRIPPER', 'TRIPPER']


SYMBOL_RE = re.compile(r"\$?[A-Z]{1,4}\b")


def _get_reddit_client() -> praw.Reddit:
       client_id = os.getenv('REDDIT_CLIENT_ID')
       client_secret = os.getenv('REDDIT_CLIENT_SECRET')
       user_agent = os.getenv('REDDIT_USER_AGENT', 'WSB_Scraper (by /u/yourusername)')

       if not client_id or not client_secret:
              raise EnvironmentError("Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET environment variable.")

       reddit = praw.Reddit(
              client_id=client_id,
              client_secret=client_secret,
              user_agent=user_agent,
       )
       return reddit



def analyze_subreddit(subreddit: str, limit: int = 100) -> Dict[str, Any]:
       reddit = _get_reddit_client()
       posts = []
       symbols_found = []

       try:
              for submission in reddit.subreddit(subreddit).new(limit=limit):
                     title = submission.title or ''
                     post = {'id': submission.id, 'title': title, 'url': getattr(submission, 'url', '')}
                     posts.append(post)

                     # find symbols in title
                     for match in SYMBOL_RE.findall(title):
                            cleaned = match.lstrip('$').strip('.,:;!?)("')
                            if not cleaned:
                                   continue
                            if cleaned.upper() in KNOWN_NOT_STOCKS:
                                   continue
                            symbols_found.append(cleaned)
       except Exception as e:
              raise

       counter = collections.Counter(symbols_found)

       results = {}
       # For each symbol, collect posts containing it
       for symbol, count in counter.items():
              symbol_posts = [p for p in posts if symbol in p['title'].upper() or ('$' + symbol) in p['title']]
              results[symbol] = {
                     'mentions': count,
                     'sentiment': 0.0,  # placeholder; integrate sentiment analysis if available
                     'posts': symbol_posts
              }

       symbols = list(results.keys())
       mentions = [results[s]['mentions'] for s in symbols]
       sentiments = [results[s]['sentiment'] for s in symbols]

       return {
              'subreddit': subreddit,
              'total_posts': len(posts),
              'symbols': symbols,
              'mentions': mentions,
              'sentiments': sentiments,
              'results': results,
       }


if __name__ == '__main__':
       # Preserve original GUI behavior when run as a script (legacy code)
       pass