# -*- coding: utf-8 -*-
"""
Updated on October 13, 2025

@author: Original by ksbig; updated by Grok 4 (xAI) for modern PRAW integration and efficiency

Description: Scrapes Reddit post titles from a subreddit (e.g., wallstreetbets), extracts potential stock symbols 
(uppercase words starting with $, length 1-4, not in exclusions), cleans them, and counts frequencies.
Requires PRAW credentials set as environment variables for security.
"""

import os
import argparse
import collections
import praw
import re

# Known non-stock words to exclude
KNOWN_NOT_STOCKS = ['PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST', 'ROBINHOOD', 
                    'GAIN', 'LOSS', 'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO', 'BELL', 'STRIPPER', 'TRIPPER']

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Reddit Stock Symbol Scraper")
    parser.add_argument('--subreddit', default='wallstreetbets', help='Subreddit to scrape (default: wallstreetbets)')
    parser.add_argument('--limit', type=int, default=100, help='Number of posts to fetch (default: 100)')
    args = parser.parse_args()

    # Load PRAW credentials from environment variables (secure practice)
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'WSB_Scraper (by /u/yourusername)')

    if not client_id or not client_secret:
        print("Error: Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET environment variable.")
        print("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET before running this script.")
        return

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    # Fetch recent post titles
    words_collection = []
    try:
        subreddit = reddit.subreddit(args.subreddit)
        for submission in subreddit.new(limit=args.limit):
            title_words = submission.title.split()  # Split title into words
            words_collection.append(title_words)
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return

    # Process titles for potential stock symbols using regex
    # Match either $TICKER or plain uppercase words of length 1-4 (e.g. AAPL, GME)
    SYMBOL_RE = re.compile(r"\$?[A-Z]{1,4}\b")
    potential_stock_symbols = []
    for title_words in words_collection:
        # title_words is a list from split(); join to preserve punctuation boundaries
        title = " ".join(title_words)
        for match in SYMBOL_RE.findall(title):
            # Remove leading $ and any surrounding punctuation
            cleaned = match.lstrip('$').strip('.,:;!?)("')
            if not cleaned:
                continue
            # Exclude known non-stock words (case-insensitive)
            if cleaned.upper() in KNOWN_NOT_STOCKS:
                continue
            potential_stock_symbols.append(cleaned)

    # Count and display frequencies
    if potential_stock_symbols:
        freq = collections.Counter(potential_stock_symbols).most_common()
        print("Most common potential stock symbols:")
        for symbol, count in freq:
            print(f"{symbol}: {count}")
    else:
        print("No potential stock symbols found in the fetched titles.")

if __name__ == "__main__":
    main()