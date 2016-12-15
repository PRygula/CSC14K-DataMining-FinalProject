# CSC 145K - Final Project
# Analyzing Sarcasm in Twitter
# Chris Demarco, Patrick Rygula, and Siobhan Stergis
# This program contains both the PBLGA and IWS algorithm as well as any helper functions needed.
# The majority of the code is found in this file, with other files containing data.

import twitter
import json
#import MySQLdb
import polyglot
import string

from polyglot.downloader import downloader
from polyglot.text import Text
from authTwitter import authTW
from collections import Counter

# The following declarations open files for which we store various data throughout the program
#tweetCorpus_database = {}
sentiment_file = open('/home/user/project/raw_data/sentiment_file.txt','w+')
situation_file = open('/home/user/project/raw_data/situation_file.txt','w+')
#sentiment_score_value = {}
positive_sentiment_file = open('/home/user/project/raw_data/positive_sentiment_file.txt','w+')
negative_sentiment_file = open('/home/user/project/raw_data/negative_sentiment_file.txt','w+')
positive_situation_file = open('/home/user/project/raw_data/positive_situation_file.txt','w+')
negative_situation_file = open('/home/user/project/raw_data/negative_situation_file.txt','w+')
parse_file = open('/home/user/project/raw_data/parse_file.txt', 'w+')
sarcasm_rating_file = open('/home/user/project/raw_data/sarcasm_rating_file.txt', 'w+')
IWS_table_file = open('/home/user/project/raw_data/tableFileIWS.txt','w+')

#all common stopwords
CONST_STOPWORDS=['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']

# global variable declarations
CONST_allTweets = [""]  # All of the text from the tweet itself stored into an array
CONST_allWords = [""] # Separate words from each tweets stored into the array with each word being its own string
CONST_resultWords = [""] # The array for saving the words after removing the stop words from CONST_allWords 
CONST_ZERO = 0
first_word = ""
second_word = ""
clean_tweets = ""
clean_ids = 0
clean_sentiment_score = 0
IWS_array = []

# The following function removes the stopwords from each tweet using CONST_STOPWORDS as a reference
def removeStopWords(tweet):

	global CONST_allTweets # using the global tag allows us to use the constant declared above as a global value in each function with the global tag
	global CONST_resultWords # using the global tag allows us to use the constant declared above as a global value in each function with the global tag
	#print CONST_allTweets
	# Nested for loop that takes every tweet in all of the tweets and then splits up all of the words in each tweet
	#split_words = [word for word in tweet.split()]
	#CONST_allWords = ''.join(word for word in split_words)

	# Use the removePunc function to get rid of all punctuation ASCII characters
	CONST_allWords = removePunc(tweet)
	#print CONST_allWords

	# Nested for loop that takes every word in all of the words in all of the tweets and only keeps the words that are not stop words

	CONST_resultWords  = ''.join([word for word in CONST_allWords if word.lower() not in CONST_STOPWORDS])

	return CONST_resultWords

# Removes ASCII Puncutation values
def removePunc(inText):
	tempArray = [] # Empty array
	exclude = set(string.punctuation) # List of all puncutation marks to be excluded in strings
	#for word in inText:
		#s = ''.join(character for character in word if character not in exclude) # Exclude all of the punctuation and then add all of the other words to s
		#tempArray.append(s) # Append s to the array
	#return tempArray # Return the array
	test = ''.join(c for c in inText if c.lower() not in exclude)
	return test

# PBLGA sentiment scoring function that is not in use
def sentment_score(input_phrase):
	# count words in input_phrase and save to total_words_in_phrase
	total_words_in_phrase = len(input_phrase.split())

	split_words = input_phrase.split()
	
	# count the amount of positive and negative words in a tweet and return its ratio (score)
	for word in split_words:
		if word in positive_sentiment_file:
			positive_words_in_phrase += 1

	for word in split_words:
		if word in negative_sentiment_file:
			negative_words_in_phrase += 1

	positive_ratio = positive_words_in_phrase/total_words_in_phrase
	negative_ratio = negative_words_in_phrase/total_words_in_phrase

	sentiment_score_value = positive_ratio - negative_ratio

	return sentiment_score_value

# The following helper functions are used to determine whether or not a given phrase is in a tweet.
# They are very rudementary and generic and do not include every possible combination.
# These helper functions are used in the PBLGA function

# Checks if there is a noun phrase
def hasNounPhrase(tweet):
	# remove stop words
	tweet_split = removeStopWords(tweet)

	# use polyglot library to separate the words into part of speech tags
	text = Text(tweet_split,hint_language_code='en')	
	text.pos_tags
	
	# check the tweet for occurences of an adjective and noun in two consecutive words and return true or false
	i=0
	while i<len(tweet_split.split()):
		if((i+1) < len(tweet_split.split())):
			if(text.words[i].pos_tag=="ADJ" and text.words[i+1].pos_tag=="NOUN"):
				return True	
			else:
				return False
		i+=1

# Checks if there is a verb phrase
def hasVerbPhrase(tweet):
	tweet_split = removeStopWords(tweet)
	text = Text(tweet_split,hint_language_code='en')
	
	text.pos_tags
	
	# uses auxilary + verb or adjective + verb to check whether a tweet has a verb phrase
	i=0
	while i<len(tweet_split.split()): 
		if((i+1) < len(tweet_split.split())): # make sure that the tweet can be processed
			if(text.words[i].pos_tag=="AUX" and text.words[i+1].pos_tag=="VERB"):
				return True	
			elif(text.words[i].pos_tag=="ADJ" and text.words[i+1].pos_tag=="VERB"):
				return True				
			else:
				return False
		i+=1

# Checks if there is a adjective phrase
def hasAdjectivePhrase(tweet):
	tweet_split = removeStopWords(tweet)
	text = Text(tweet_split,hint_language_code='en')
	
	text.pos_tags
	
	# checks three cases in see if there is an adjective phrase 
	i=0
	while i<len(tweet_split.split()):
		if((i+1) < len(tweet_split.split())):
			if(text.words[i].pos_tag=="ADJ" and text.words[i+1].pos_tag=="ADV"):
				return True	
			elif(text.words[i].pos_tag=="ADJ" and text.words[i+1].pos_tag=="ADJ"):
				return True				
			elif(text.words[i].pos_tag=="ADV" and text.words[i+1].pos_tag=="ADJ"):
				return True				
			else:
				return False

		i+=1

# Check if there is an adverb phrase in a tweet
def hasAdverbPhrase(tweet):
	tweet_split = removeStopWords(tweet)
	text = Text(tweet_split,hint_language_code='en')
	
	text.pos_tags
	
	# checks for adjective + adposition or adverb + adverb
	i=0
	while i<len(tweet_split.split()):
		if((i+1) < len(tweet_split.split())):
			if(text.words[i].pos_tag=="ADJ" and text.words[i+1].pos_tag=="ADP"):
				return True	
			elif(text.words[i].pos_tag=="ADV" and text.words[i+1].pos_tag=="ADV"):
				return True				
			else:
				return False
		i+=1

# The PBLGA function uses the helper functions created above to create a lexicon of phrases in positive/negative
# situation and sentiment of a sentence. There is supposed to a sentiment scoring aspect as well but that cannot
# be implemented because lack of documentation and poor pseudocode. This algorithm was minimized and done solely
# as proof that it could be done. Too much information was left out to recreate it properly so a minimal viable
# algorithm was created.
def PBLGA(tweetCorpus):

	# same as with IWS, can make this function work on one tweet and pass it an entire corpus to work one by one
	
	# this for loop takes in all tweets and puts them into a file

	# for every tweet in the inputed corpus of tweets, check if there is a noun phrase/adjective phrase or
	# both a noun phrase and verb phrase and then add the tweet to the sentiment file
	for tweet in tweetCorpus:
		if(hasNounPhrase(tweet) or hasAdjectivePhrase(tweet) or (hasNounPhrase(tweet) and hasVerbPhrase(tweet))):
			sentiment_file.write(tweet.encode('ascii','ignore'))
			sentiment_file.write('\n')	
		# if the tweet has the following combinations of phrases, add the tweet to the situation file
		elif(hasVerbPhrase(tweet) or (hasAdverbPhrase(tweet) and hasVerbPhrase(tweet)) or (hasVerbPhrase(tweet) and hasAdverbPhrase(tweet)) or (hasAdjectivePhrase(tweet) and hasVerbPhrase(tweet)) 
			or (hasVerbPhrase(tweet) and (hasNounPhrase(tweet))) or (hasVerbPhrase(tweet) and hasAdverbPhrase(tweet) and hasAdjectivePhrase(tweet)) or (hasVerbPhrase(tweet) and hasAdjectivePhrase(tweet) and hasNounPhrase(tweet)) 
			or (hasAdverbPhrase(tweet) and hasAdjectivePhrase(tweet) and hasNounPhrase(tweet))):
			situation_file.write(tweet.encode('ascii','ignore'))
			situation_file.write('\n')
				# append phrase to file instead of union(k)
	
	# the phrase is put into a positive or negative file based on if any word in the phrase is already in 
	# a positive or negative file. Must have some sort of phrases already in both files.

	# the following scoring elements were commented out because there is no heuristic that puts a score on each phrase
	# so there is no way to score the tweets and rate them after the algorithm has run. 	

	#for phrase in sentiment_file:
	#	sentiment_score_value = sentiment_score(phrase)
	#	if(sentiment_score_value > 0.0):
	#		positive_sentiment_file = positive_sentiment_file.union(phrase)
	#	elif(sentiment_score_value < 0.0):
	#		negative_sentiment_file = negative_sentiment_file.union(phrase)	
		#else:
			# neutral sentiment phrase

	#for phrase in situation_file:
	#	sentiment_score_value = sentiment_score(phrase)
	#	if(sentiment_score_value > 0.0):
	#		positive_situation_file = positive_situation_file.union(phrase)
	#	elif(sentiment_score_value < 0.0):
	#		negative_situation_file = negative_situation_file.union(phrase)
		#else:
			# neutral situation phrase
	
	

# This function is a helper function for IWS that finds the first word of a tweet.
# it removes punctuation, then finds the first word's part of speech and returns it.
def find_first_tag(tweet):
	# first word in the tweet
	global first_word
	print tweet	
	tweet_split = removePunc(tweet)
	#print tweet_split
	#tweet_join = " ".join(tweet_split)
	#print tweet_join	
	#text = Text(tweet_join,hint_language_code='en')
	text = Text(tweet_split,hint_language_code='en')
	#print text
	text.pos_tags
	#print text.pos_tags
	first_word = text.words[0].pos_tag
	#text_Pos = text.pos_tags
	#first_word = text_Pos.words[0].pos_tag
	#print first_word
	return first_word

# This function is a helper function to the IWS algorithm. It finds the word immediately after the first word.
# This function does not remove stop words or anythinng else and returns immediately the next word.
# It also checks if the tweet is longer than one word in order to properly run. It returns a dummy
# 'X' part of speech if there was nothing found. 
def find_immediate_next_tag(tweet):
	# second word in the tweet
	global second_word 

	tweet_split = removePunc(tweet)
	if(len(tweet_split.split()) >= 2):
		#sentence = " ".join(tweet_split)
		#sentence_text = Text(sentence,hint_language_code='en')
		sentence_text = Text(tweet_split,hint_language_code='en')
		sentence_text.pos_tags
		second_word = sentence_text.words[1].pos_tag
		#sentence_Pos = sentence_text.pos_tags
		#second_word = sentence_Pos.words[1].pos_tag
		return second_word	
	else:
		return 'X'

# This function is a helper function to the IWS algorithm. It removes stop words and punctation and finds
# the next most significant word after the first word. This is important in order to make proper phrases.
def find_next_tag(tweet):
	# remove stop words
	print tweet
	global CONST_STOPWORDS
	tweet_noPunc = removePunc(tweet)
	tweet_split = tweet_noPunc.split()
	start_word = tweet_noPunc[0]
	
	# if the length is not long enough, return the immediate next word and a dummy character
	if(len(tweet_split) < 3):
		first_next_word = find_immediate_next_tag(tweet)
		second_next_word = 'X'
		return first_next_word, second_next_word 	
	
	num = 1	
	if start_word in CONST_STOPWORDS:
		num = 0
	else:
		num = 1
	
	temp = removeStopWords(tweet)
	if(len(temp) < 3):
		return 'X','X'
	else:
		#sentence = " ".join(temp)
		#sentence_text = Text(sentence, hint_language_code = 'en')
		sentence_text = Text(temp,hint_language_code='en')
		sentence_text.pos_tags
		first_next_word = sentence_text.words[num].pos_tag
		second_next_word = sentence_text.words[num+1].pos_tag
		#sentence_pos = sentence_text.pos_tags 
		#next_word = sentence_pos.words[num].pos_tag
		return first_next_word, second_next_word

# This function implements the Interjection Start Word algorithm. It takes in tweets and checks if they start with an
# interjection word. It finds the part of speech of the helpper function words. If the tweet starts with an interjection word,
# it rates the amount of sarcasm by comparing the following words and returns 1. If the tweet does not start with 
# and interjection word, it returns 0 as a neutral tweet. Otherwise, it returns -1.
def IWS(tweet_corpus):
	global clean_tweets
	global clean_ids
	global IWS_array
	# for adverb/verb/adj/adverb/interjection
	# check a file of respective words 
	# if it is in the file return true?
	# remove all for loops and leave only if elses and tag functions. Make simple for loop to just run for tweet in tweets

	for tweet in tweet_corpus:
		first_tag = find_first_tag(tweet)
		immediate_next_tag = find_immediate_next_tag(tweet)
		first_next_tag, second_next_tag = find_next_tag(tweet)

		if(len(tweet) < 4 ):
			sarcasm_rating = 0
		elif((first_tag == "INTJ") and (immediate_next_tag == ("ADJ" or "ADV"))):
			sarcasm_rating = 1
		elif((first_tag == "INTJ") and (((first_next_tag == "ADV") and (second_next_tag == "ADJ")) or ((first_next_tag == "ADJ") and (second_next_tag == "NOUN")) or ((first_next_tag == "ADV") and (second_next_tag == "VERB")))):
			sarcasm_rating = 1
		elif(first_tag != "INTJ"):
			sarcasm_rating = 0
		else:
			sarcasm_rating = -1

		# add each rating to an array and write to the file.
		IWS_array.append(sarcasm_rating)
		print IWS_array
		sarcasm_rating_file.write(str(sarcasm_rating))
		sarcasm_rating_file.write('/n')
		#print sarcasm_rating	
	
	# create the database entries for the id, tweet, and rating
	i = 0
	while i < len(clean_ids):
		tweet = clean_tweets[i].encode('ascii','ignore')
		#print tweet
		id = clean_ids[i]
		score = IWS_array[i] 
		IWS_table_file.write(str(id) + "$" + tweet + "$" + str(score))
		IWS_table_file.write('\n')
		i+=1	
	return sarcasm_rating # sarcasm rating of 1 is sarcastic, 0 is doesn't start with interjection, -1 is not sarcastic

# clean the data from the tweets and ids and create files for them
def cleanData():
	global clean_tweets
	global clean_ids
	global clean_sentiment_score

	with open('/home/user/project/raw_data/SarcasticTweets.json', 'r') as outputFile:
		dirtyData = json.load(outputFile)
	clean_tweets = [status['text']
		for status in dirtyData]
	clean_ids = [status['id']
		for status in dirtyData]
	
	cleanTweetFile = open('/home/user/project/raw_data/cleanTweets.txt', 'w+')
	cleanIDFile = open('/home/user/project/raw_data/cleanIDs.txt', 'w+')

	#cleanTweetFile.write("\n".join(str(elem) for elem in clean_tweets))	
	cleanIDFile.write("\n".join(str(elem) for elem in clean_ids))
	
	for tweet in clean_tweets:
		clean = tweet.encode('ascii','ignore')
		cleanTweetFile.write(clean)
		cleanTweetFile.write("\n")
	
	#i = 0	
	#while i<len(tweets):
	#	tableFile.write(str(clean_tweets[i]) + "$" + str(clean_ids[i]) + "$" + str(clean_sentiment_score[i]))
	#	tableFile.write("\n")
	#	i+=1

#ID$tweet$sentimentscore
#make another function to put all of the cleaned data into database file	

def main():
	cleanData()
	PBLGA(clean_tweets)
	testing_tweets = ["The brown fox jumped over the red wagon.", "well that was stupid"]
	#IWS(clean_tweets)
	#PBLGA(testing_tweets)
main()
