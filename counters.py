# counters.py
import os
import collections
import praw
import re
from typing import Dict, Any, List

KNOWN_NOT_STOCKS = [    'PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST',
    'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO',
    'BELL', 'STRIPPER', 'TRIPPER'
]

SYMBOL_RE = re.compile(r"\$?[A-Z]{1,4}\b")

def get_reddit_instance() -> praw.Reddit:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "WSB_Scraper (by /u/yourusername)")

    if not client_id or not client_secret:
        raise EnvironmentError("Missing REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET environment variable.")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return reddit

def potential_stock_symbols(subreddit: str, limit: int = 100) -> Dict[str, Any]:
    """
    Fetch recent posts, extract potential $TICKER / TICKER tokens,
    and return a results payload compatible with results.html.
    """
    reddit = get_reddit_instance()
    posts: List[Dict[str, str]] = []
    symbols_found: List[str] = []

    for submission in reddit.subreddit(subreddit).new(limit=limit):
        title = submission.title or ""
        posts.append({
            "id": submission.id,
            "title": title,
            "url": getattr(submission, "url", ""),
        })
        for match in SYMBOL_RE.findall(title):
            cleaned = match.lstrip("$").strip(".,:;!?)(\"'")
            if not cleaned:
                continue
            if cleaned.upper() in KNOWN_NOT_STOCKS:
                continue
            symbols_found.append(cleaned.upper())

    counter = collections.Counter(symbols_found)
    symbols = [sym for sym, _ in counter.most_common()]
    mentions = [counter[sym] for sym in symbols]
    sentiments = [0.0 for _ in symbols]  # placeholder; no sentiment here

    # Build per-symbol post list (titles that mention the symbol)
    results: Dict[str, Any] = {}
    for sym in symbols:
        sym_posts = [p for p in posts if sym in p["title"].upper() or f"${sym}" in p["title"]]
        results[sym] = {
            "mentions": counter[sym],
            "sentiment": 0.0,
            "posts": sym_posts,
        }

    return {
        "subreddit": subreddit,
        "total_posts": len(posts),
        "symbols": symbols,
        "mentions": mentions,
        "sentiments": sentiments,
        "results": results,
        "avg_sentiment": 0.0,
    }


# Keep CLI behavior for ad-hoc testing
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reddit Stock Symbol Scraper")
    parser.add_argument("--subreddit", default="wallstreetbets")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    data = potential_stock_symbols(args.subreddit, args.limit)
    print("Most common potential stock symbols:")
    for s, m in zip(data["symbols"], data["mentions"]):
        print(f"{s}: {m}")