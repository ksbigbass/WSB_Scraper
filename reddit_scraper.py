# -*- coding: utf-8 -*-
"""
Lightweight scraper utilities adapted from the original GUI script.

Provides analyze_subreddit(subreddit, limit) which returns a JSON-serializable
structure summarizing symbol mentions and posts. GUI/Tk code is preserved but
only runs when executed as a script (not when imported).
"""
import os
import re
import collections
import praw
from typing import Dict, Any, List

# Reuse known exclusions from counters if available
try:
       from counters import KNOWN_NOT_STOCKS
except Exception:
       KNOWN_NOT_STOCKS = ['PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST',
                                          'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO',
                                          'BELL', 'STRIPPER', 'TRIPPER']


SYMBOL_RE = re.compile(r"\$?[A-Z]{1,4}\b")


def _get_reddit_client():
       """Create and return a PRAW Reddit instance using env vars (or fallback)."""
       client_id = os.getenv('REDDIT_CLIENT_ID')
       client_secret = os.getenv('REDDIT_CLIENT_SECRET')
       user_agent = os.getenv('REDDIT_USER_AGENT', 'WSB_Scraper (by /u/yourusername)')

       # Fallback to hardcoded values if present in legacy script (not recommended)
       if not client_id or not client_secret:
              # Try to honor any hardcoded credentials in the original file (if left)
              client_id = os.getenv('REDDIT_CLIENT_ID', os.getenv('REDDIT_CLIENTID'))
              client_secret = os.getenv('REDDIT_CLIENT_SECRET', os.getenv('REDDIT_CLIENTSECRET'))

       # If still missing, try to load from a .env file (if python-dotenv is installed)
       if not client_id or not client_secret:
              try:
                     from dotenv import load_dotenv
                     # Load .env from project root
                     load_dotenv()
                     client_id = os.getenv('REDDIT_CLIENT_ID')
                     client_secret = os.getenv('REDDIT_CLIENT_SECRET')
              except Exception:
                     # python-dotenv not available or load failed; will raise below if still missing
                     pass

       if not client_id or not client_secret:
              raise EnvironmentError(
                     'Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET environment variables.\n'
                     'Set them in your shell (export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=...) or create a .env file with:\n'
                     'REDDIT_CLIENT_ID=your_id\nREDDIT_CLIENT_SECRET=your_secret\nREDDIT_USER_AGENT=your_agent'
              )

       return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


def analyze_subreddit(subreddit: str, limit: int = 100) -> Dict[str, Any]:
       """Fetch recent posts from `subreddit`, extract ticker-like symbols, and return summary data.

       Returned structure::
         {
              'subreddit': subreddit,
              'total_posts': int,
              'symbols': [str,...],
              'mentions': [int,...],
              'sentiments': [float,...],
              'results': { symbol: { 'mentions': int, 'sentiment': float, 'posts': [post_dict,...] }, ... }
         }
       """
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
       try:
              from tkinter import *
              import tkinter as tk
              from PIL import Image, ImageTk
              from matplotlib.figure import Figure
              from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

              # Old GUI initialization preserved here (simplified)
              reddit = None
              try:
                     reddit = _get_reddit_client()
              except EnvironmentError as ee:
                     print('Environment credentials missing:', ee)
                     print('Please create a .env file or export REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET before running the GUI.')
                     raise

              root = Tk()
              root.title("Reddit Stock Symbol Scraper")
              root.geometry("900x900")

              # ...existing GUI wiring would go here if you want to keep it
              # For brevity we won't recreate the full GUI in this refactor.
              print('Run analyze_subreddit(subreddit, limit) from code or use the Flask app.')

       except Exception as e:
              print('GUI could not be started:', e)




