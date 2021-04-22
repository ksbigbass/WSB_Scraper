import counters

import praw
import pandas as pd
#import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
from collections import OrderedDict

import pylab
import numpy as np





#from keys import reddit_client_ID, reddit_secrete_token, reddit_userName, reddit_password
reddit = praw.Reddit(client_id ='FwwowWJjJ3qa2A',  
                     client_secret ='kOGPQcJYvl5Ncu5VPZ7T2yOnbezOFw',  
                     user_agent ='WSB',  
                     username ='ksbigbass',  
                     password ='')  

subreddit = reddit.subreddit('wallstreetbets')

top_subreddit = subreddit.top(limit=1000)


words_collection = []
potential_stock_symbols = []
known_not_stocks = ['PROMOTED','UPVOTE','SUPPORT','YOLO','CLASS','ACTION','AGAINST','ROBINHOOD','GAIN','LOSS','PORN','WSB','WSB.','I','HEAR','NO','BELL','STRIPPER','TRIPPER']
 

for submission in top_subreddit:
       title= submission.title
       title_words = title.split()
       words_collection.append(title_words)


for title in words_collection:                  #Search title for possible stock symbols 
  for word in title:
    if word.isupper():
      if counters.word_count(word) < 5:
        if word.startswith('$') and word[1].isalpha():
          if word not in known_not_stocks:
            potential_stock_symbols.append(word)
            counters.removeBS(potential_stock_symbols)
            



count = (counters.CountFrequency(potential_stock_symbols))
print(count)


x = []
y = []

for key,value in count:
   key = x.append(key)
   value = y.append(value)

plt.plot(x,y)
plt.show()




#pylab.plot(*zip(*sorted(count, key=lambda x:x[1])))

#df = pd.DataFrame(count,columns=['score','symbol'])
#df = pd.DataFrame(list(zip(potential_stock_symbols,title_scores)),columns=['symbol','score'])

#df.to_csv('stocks.csv')
#df = pd.read_csv('stocks.csv')
##fig = px.line(count, y = "symbol", x ="score", title="WSB")
##fig.show()
