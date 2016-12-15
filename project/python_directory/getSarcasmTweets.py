# Chris DeMarco
# Sep 12, 2016
# Mining Social Web - Assignment 1
# Get 100 Tweets, remove puncutation and all stop words from the tweets. Use Python collection.count to found how many times each word was used
# Use TF-IDF to determine the frequency of each word and compare to the collections.Counter amount

import twitter 
import json
import math
import string
#from twitter import *

#from authTwitter import authTW
from collections import Counter

# List of all stop words
CONST_STOPWORDS=['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
CONST_allTweets = [""]  # An Array of just the text of each tweet
CONST_allWords = [""] # An Array of all words from all tweets. Each word being a separate string without puncutation
CONST_resultWords = [""] # An Array of all words from CONST_allWords, minus the stop words
countFile = open('output.txt', 'w+') # Opens an Output file for python count and TFIDF Count

def authTW():
        CONSUMER_KEY = 'PKdYx5iAPX7RG0fnScv0014L2'
        CONSUMER_SECRET = 'xmaEwNJMdN2PepTHqbwcnIlA1PDnoy71YDtif8Gb2ahn0DUpWx'

        OAUTH_TOKEN = '596054075-cmzVgJfiCV1Xnqr0EbyGsnlgacGUEZm6idMpqQVy'
        OAUTH_TOKEN_SECRET = 'GnIMIEIBRK9XsLPUsv8KRcGN0k6NhwcTunSW71zewDZRt'

        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        twitter_api = twitter.Twitter(auth = auth)

        return twitter_api


# This is a modified version that we used in class.
# The getSeach Function will search the twitter api for the specific query we want and the number of tweets based on the query. 
# After it finds all 100 statuses, it will write them to all to a json file. After that, the function will then take just the main text of the tweets 
# and store them in the CONST_allTweets array
def getSearch(t_obj):

	q = '#sarcasm' #The word that we are searching
	count = 100 #the number of tweets we want
	
	search_results = t_obj.search.tweets( q = q, count = count)  # Q= query string
        with open('SarcasticTweetsRaw.json', 'w+') as outputFile:
                json.dump(search_results,outputFile, indent = 1)

	statuses = search_results['statuses'] #saves the json object 'statuses' to the variable statuses

	#this line will open a .json file and write statuses to it. w+ is used to write to a file and if the file does not exist
	# it will create the file too
	with open('SarcasticTweets.json', 'w+') as outputFile2:  
		json.dump(statuses,outputFile2, indent = 1)

	# this line will take text out of each status (a json file subobject) and saves it to the list status_texts
	status_texts = [status['text']
		for status in statuses]
	with open('SarcasticTweetsText.json', 'w+') as outputFile3:
        	json.dump(status_texts,outputFile3, indent = 1)

	global CONST_allTweets # global tag makes this constant a global variable and allows data to be shared with other functions
	CONST_allTweets = status_texts # set the text of each status to the global variable CONST_allTweets

	return statuses

# The removeStopWords function will take the allTweets array, 
# split the strings word by word making each word a separate string.
# Then it will remove any puncutation that if found on a word. 
# Then it will check each word, compare that word to all the stopwords. 
# If it is not a stop word it will be stored into resultwords variable. 
def removeStopWords():
	global CONST_allTweets # global tag makes this constant a global variable and allows data to be shared with other functions
	global CONST_resultWords # global tag makes this constant a global variable and allows data to be shared with other functions
	global countFile # global tag makes this constant a global variable and allows data to be shared with other functions

	# This nested for loop will split up all the tweets and then split up all the words in each tweet.
	# leaving an array of words
	CONST_allWords = [word 
						for tweet in CONST_allTweets
							for word in tweet.split()]

	# call the remove puncutation function on the all words array
	CONST_allWords = removePunc(CONST_allWords)

	# for loop that will check if each word in the allWords array is a stop word, if it is, it will not be added to resultWords
	CONST_resultWords  = [word for word in CONST_allWords if word.lower() not in CONST_STOPWORDS]

	# gives us the frequency of how mnay times each word was used
	counts = Counter(CONST_resultWords).most_common()
	
	with open('SarcasticTweetsWithoutStopWords.json', 'w+') as outputFile:
       		json.dump(CONST_resultWords,outputFile, indent = 1)

	#write it out to the file
	countFile.write("Python frequency counter using collections library: ")
	countFile.write("\n")
	for x in counts:
		countFile.write("%s" % str(x))
	countFile.write("\n")
	countFile.write("\n")
	countFile.write("\n")

# Removes Puncutation
def removePunc(inText):
	tempArray = []
	exclude = set(string.punctuation) # List of all puncutation marks to be excluded in strings
	for word in inText:
		s = ''.join(character for character in word if character not in exclude)
		tempArray.append(s)
	return tempArray

#	Frequency	for	TF.IDF
def freq(word, document):
	return document.split(None).count(word)

# Fuction that returns a counter of how many documents contained a specific work
def numDocsContaining(word,documentList):
	documentCount = 0   #Counter to seehow many documents contain the word
	for document in documentList:
		if document.find(word):
			documentCount += 1
	return documentCount

	
def tf(word, document):
	return (freq(word,document) / float(len(document)))

def idf(word, documentList):
	return math.log(len(documentList) / numDocsContaining(word,documentList))

def tfidf(word, document, documentList):
	return (tf(word,document) * idf(word,documentList))

def runTFIDF():
	global CONST_allTweets
	global countFile
	tweetList = []
	for tweet in CONST_allTweets:
		tweetList.append(tweet)
	term = {}
	words = {}
	tweetNumber = 0
	while tweetNumber < len(tweetList):
		for tweet in tweetList[tweetNumber].split(None):
			words[tweet] = tfidf(tweet,tweetList[tweetNumber],tweetList)
		term[tweetNumber] = words
		words = {}
		tweetNumber += 1

	# write it to the file
	countFile.write("Python Counter Using TF-IDF: ")
	countFile.write("\n")
	countFile.write("%s" % str(term))


def main():
	twitter_obj = authTW()
	r = getSearch(twitter_obj)
	s = removeStopWords()
	#t = runTFIDF()
	#print(json.dumps(r, indent = 1))

main()
