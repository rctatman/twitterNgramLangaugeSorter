# -*- coding: utf-8 -*-
"""
N-gram Twitter language identification model
"""
# imports
import string

   
# function that takes a string and number of characters and returns the 
# freuency count of each ngram, excluding puncutaion
def ngramDictionaryMaker(file, n):
    ngramDict = {}
    # remove puncutation 
    stripped =  file.translate(None, string.punctuation)
    # step through line and for each n-gram, see if it's int our dict
    for i in range(0,len(stripped)):
        x = stripped[i:(i+n)]
            # if yes, iterate
        if x in ngramDict:
            ngramDict[x] += 1
                # if no, create and iterate
        else:
            ngramDict[x] = 1
    return ngramDict

# function that takes two dicitonaries and a key, and, if the key appaears
# in both, determiens how probable the key was given the first dtionary. If 
# the key appears more than once inthe second dictionary, the disjoint probablilty
# is returned  
def compareFreqDicts(dict1, dict2, key):
    # if key appears in both dictionaries, calculate probality in training dict
    if (key in dict1 and  key in dict2):
        # calculate and return probablity of key in training data
        prob = dict1.get(key)
        sum1 = sum(dict1.values())
        for i in range(0,dict2.get(key)):
            prob += (prob/sum1)
        return prob
    # if key doesn't appear in training data, return 0
    else: 
        return 0

# read in English training data
with open ('training.en.txt', 'r') as myfile:
    training=myfile.read()
# read in Twitter data
with open ('tweets.txt', 'r') as myfile:
    twitter=myfile.read()

# create dictionary (with counts) of ngrams in our training data
engData = ngramDictionaryMaker(training, 3)

# create a dictionary for out tweet "englishness" scores
tweetEnglishness = {}
n = 3
# for each tweet, create an ngram dictionary and compare to our training data
for line in twitter.splitlines():
    tweetDict = {}
    # remove puncutation
    line =  line.translate(None, string.punctuation)    
    # extract and count ngrams    
    tweetDict = ngramDictionaryMaker(line, 3)
    # step through each ngram in our tweet dictionary and compute its probaility
    if sum(tweetDict.values()) > 0: 
        tweetProb = 0.0
        for key in tweetDict:
            prob = compareFreqDicts(engData, tweetDict, key)
            tweetProb = tweetProb + prob
        averageTweetProb = tweetProb/sum(tweetDict.values())
        tweetEnglishness[str(line)] = averageTweetProb

# ok, now let's see how it worked
mostEnglishy = sorted(tweetEnglishness, key=tweetEnglishness.get, reverse=True)[:10]
leastEnglishy = sorted(tweetEnglishness, key=tweetEnglishness.get, reverse=False)[:10]

#pretty good, but for some reason the words within the key got sorted alphabetically?

