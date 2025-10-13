# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:30:12 2021

@author: ksbig
"""

import collections

words_collection = []
potential_stock_symbols = []
known_not_stocks = ['PROMOTED','UPVOTE','SUPPORT','YOLO','CLASS','ACTION','AGAINST','ROBINHOOD','GAIN','LOSS','PORN','WSB','WSB.','I','HEAR','NO','BELL','STRIPPER','TRIPPER']
symbols = []  

def cleanTitle(words_collection):
	for title in words_collection:                  #Search title for possible stock symbols 
		for word in title:
			if word.isupper():
				if  word_count(word) < 5:
					if word.startswith('$') and word[1].isalpha():
						if word not in known_not_stocks:
							potential_stock_symbols.append(word)
							removeBS(potential_stock_symbols)


def CountFrequency(my_list):
  counter=collections.Counter(my_list)
  return counter.most_common()
         
def word_count(word):
  count = 0
  for char in word:
    count = count + 1
    return count

def removeBS(list):
	j=0
	while j < len(list):
		for i in list:
			list[j] = i.strip('$') 
			j+=1
	removePeriod(list)
		 
def removePeriod(list):
	j=0
	while j < len(list):
		for i in list:
			list[j] = i.strip('.')
			j+=1
	return list