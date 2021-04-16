import praw
import pandas as pd
# import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
from collections import OrderedDict
import collections
import pylab
import numpy as np


def countFrequency(my_list):
    counter = collections.Counter(my_list)
    return counter.most_common()


def word_count(word):
    count = 0
    for char in word:
        count = count + 1
        return count


# from keys import reddit_client_ID, reddit_secrete_token, reddit_userName, reddit_password
reddit = praw.Reddit(client_id='FwwowWJjJ3qa2A',
                     client_secret='kOGPQcJYvl5Ncu5VPZ7T2yOnbezOFw',
                     user_agent='WSB',
                     username='ksbigbass',
                     password='')

subreddit = reddit.subreddit('stocks')

top_subreddit = subreddit.top(limit=1000)

words_collection = []
title_scores = []
potential_stock_symbols = []
known_not_stocks = ['PROMOTED', 'UPVOTE', 'SUPPORT', 'YOLO', 'CLASS', 'ACTION', 'AGAINST', 'ROBINHOOD', 'GAIN', 'LOSS',
                    'PORN', 'WSB', 'WSB.', 'I', 'HEAR', 'NO', 'BELL', ]

for submission in top_subreddit:
    title = submission.title
    title_words = title.split()
    words_collection.append(title_words)

for title in words_collection:
    for word in title:
        if word.isupper():
            if word_count(word) < 5:
                if word.startswith('$') and word[1].isalpha():
                    if word not in known_not_stocks:
                        potential_stock_symbols.append(word)

count = (countFrequency(potential_stock_symbols))
pylab.plot(*zip(*sorted(count, key=lambda x: x[1])))

od = OrderedDict(zip(count, potential_stock_symbols))
od = {'title': potential_stock_symbols, 'score': count}

for i, j in od.items():
    print(i)
    print(j)
# count = {}

df = pd.DataFrame(count, columns=['score', 'symbol'])
df = pd.DataFrame(list(zip(potential_stock_symbols, title_scores)), columns=['symbol', 'score'])

df.to_csv('stocks.csv')
df = pd.read_csv('stocks.csv')
# fig = px.line(count, y = "symbol", x ="score", title="WSB")
# fig.show()
