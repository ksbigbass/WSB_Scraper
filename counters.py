import collections


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
