#natural language toolkit
#regular expressions
import re
import collections
from nltk.corpus import stopwords
import time
import csv

trainingCount=0
positiveCount=0
negativeCount=0
frequencyDictionary={}
positiveDictionary={}
negativeDictionary={}

def removeStopWords(wordList):
	stopWord = stopwords.words('english')
	stopWord.remove('not')
	stopWord.remove('nor')
	stopWord.remove('no')
	stopWord.append('')
	return [w for w in wordList if w not in stopWord]
start=time.time()
with open('train/trainActual.csv', 'rU') as f:

	lines = csv.reader(f)
	i=0
	for line in lines:
		if len(line)==2:
			trainingCount+=1
			wordSplit = re.split('\s+', line[1].lower())
			#remove all stop words
			wordNoStopWords=removeStopWords(wordSplit)
			#print 'Word No Stopwords',wordNoStopWords
			#count the number of times a word has occurred in the list
			wordCount = collections.Counter(wordNoStopWords)
			#print wordCount
			#POSITIVE REVIEWS
		 	if(line[0]=="positive"):
		 		positiveCount+=1
				for word in wordCount:
				#Already in  dictionary
					if word in frequencyDictionary:
						current=frequencyDictionary[word]
						current[0]+=wordCount[word]
						current[1]+=1
						frequencyDictionary[word]=current
					#Add the word into dictionary
					else:
						frequencyDictionary[word]=[wordCount[word],1]
					if word in positiveDictionary:
						current = positiveDictionary[word]
						current[0] += wordCount[word]
						current[1] += 1
						positiveDictionary[word] = current
					# Add the word into dictionary
					else:
						positiveDictionary[word] = [wordCount[word], 1]

			#NEGATIVE REVIEWS
			if(line[0]=="negative"):
				negativeCount+=1
			for word in wordCount:
				# Already in  dictionary
				if word in frequencyDictionary:
					current = frequencyDictionary[word]
					current[0] += wordCount[word]
					current[1] += 1
					frequencyDictionary[word] = current
				#Add the word into dictionary
				else:
					frequencyDictionary[word] = [wordCount[word], 1]
				if word in negativeDictionary:
					current = negativeDictionary[word]
					current[0] += wordCount[word]
					current[1] += 1
					negativeDictionary[word] = current
				#Add the word into dictionary
				else:
					negativeDictionary[word] = [wordCount[word], 1]





