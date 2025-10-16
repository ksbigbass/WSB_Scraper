import os
import argparse
import collections
import praw
import re
import sys

KNOWN_NOT_STOCKS = [
    'PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST',
    'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO',
    'BELL', 'STRIPPER', 'TRIPPER'
]

SYMBOL_RE = re.compile(r"\$?[A-Z]{1,4}\b")

def main():
    parser = argparse.ArgumentParser(description="Reddit Stock Symbol Scraper")
    parser.add_argument("--subreddit", default="wallstreetbets", help="Subreddit to scrape")
    parser.add_argument("--limit", type=int, default=100, help="Number of posts to fetch")
    args = parser.parse_args()

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret:
        sys.exit("❌ Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET. Set them before running.")

    if not user_agent or "yourusername" in user_agent.lower():
        sys.exit("❌ REDDIT_USER_AGENT is invalid. Use format: python:com.appname:1.0 (by u/ksbigbass)")

    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    # Choose flow based on available credentials
    if username and password:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
    else:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    words_collection = []
    try:
        for submission in reddit.subreddit(args.subreddit).new(limit=args.limit):
            words_collection.append(submission.title.split())
    except Exception as e:
        sys.exit(f"❌ Reddit API error: {e}")

    potential_stock_symbols = []
    for title_words in words_collection:
        title = " ".join(title_words)
        for match in SYMBOL_RE.findall(title):
            cleaned = match.lstrip("$").strip(".,:;!?)(\"'")
            if cleaned and cleaned.upper() not in KNOWN_NOT_STOCKS:
                potential_stock_symbols.append(cleaned)

    if potential_stock_symbols:
        freq = collections.Counter(potential_stock_symbols).most_common()
        print("✅ Most common potential stock symbols:")
        for symbol, count in freq:
            print(f"{symbol}: {count}")
    else:
        print("ℹ️ No potential stock symbols found.")

if __name__ == "__main__":
    main()