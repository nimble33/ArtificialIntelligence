from __future__ import division
import csv
import time
#Regular Expression Engine
import re
#2,400 stopwords for 11 languages -We use the stop words in english
from nltk.corpus import stopwords

def main():
	choice=input("Select 1 or 2 \n *1-Predicts the review either positive or negative*  *2- Predicts the review with a rating within [1-5]:\n")
	if(choice==1):
		TRAIN_SET='train/trainActual.csv'
	elif(choice==2):
		TRAIN_SET='train/trainActualStars.csv'
	else:
		print "Please enter 1 or 2"
	TEST_SET='test/testPredict.csv'
	TEST_SET_ACTUAL_POS_NEG = 'test/testActual.csv'
	TEST_SET_ACTUAL_STARS='test/testActualStars.csv'
	if(choice==1 or choice==2):
		targetLabelCount,wordLabelCount=divideTraining(TRAIN_SET,choice)
		print targetLabelCount
		#print wordLabelCount
		timeNb=time.time()
		naiveBayesClassifyAndTest(choice,targetLabelCount,wordLabelCount,TEST_SET)
		#classifierNaiveBayes=nbTrain(choice, review, rating)
		# if(choice==1):
		# 	nbTest(choice,classifierNaiveBayes,TEST_SET,TEST_SET_ACTUAL_POS_NEG)
		# 	print('Time taken Naive Bayes Pos Neg:', time.time()-timeNb)
		# if(choice==2):
		# 	nbTest(choice, classifierNaiveBayes, TEST_SET, TEST_SET_ACTUAL_STARS)
		# 	print('Time taken Naive Bayes Stars:',   time.time()-timeNb)


def divideTraining(trainSet,choice):
	print 'Naive Bayes training'
	with open(trainSet, 'rU') as f:
		lines = csv.reader(f)
		for line in lines:
			if len(line) == 2:
				#Positive/Negative or [1-5]
				classLabel = line[0]
				classCountDictionary=classCount(classLabel)
				#Split by white spaces
				wordSplit = re.split('\s+', line[1].lower())
				wordNoStopWords = removeStopWords(wordSplit)
				for word in wordNoStopWords:
					wordClassLabelCountDictionary=wordClassCount(word,classLabel)
					#print wordClassLabelCountDictionary
	return classCountDictionary,wordClassLabelCountDictionary

probabilityClasses={}
def naiveBayesClassifyAndTest(choice,targetLabelCount,wordLabelCount,testSetPath):
	print 'Naive Bayes test'
	#Total Size
	totalReviewsInDataSet=sum(targetLabelCount.values())
	print totalReviewsInDataSet
	#Labels either [positive,negative] or [1,2,3,4,5]
	classLabels = targetLabelCount.keys()
	print classLabels
	#Explore test set
	with open(testSetPath, 'rU') as f:
		lines = csv.reader(f)
		# For each Review
		for line in lines:
			if len(line)==1:
				wordSplit = re.split('\s+', line[0].lower())
				wordNoStopWords = removeStopWords(wordSplit)
				#Arrange as list
				words=list(wordNoStopWords)
				#Mapping each word to a classlabel
				for classLabel in classLabels:
					for word in words:
						#Assign probability to each word for each class label
						wordProbability=getWordProbability(word,classLabel,targetLabelCount,wordLabelCount)
						#p(word1/classLabel)*p(word2/classLabel)...n classLabel belongs to class[p,n] or [1-5]
						#Calculate the product of prob's in wor







testReviewsToPredict=[]
actualTestResults=[]

#predictedTestResults=[]

def nbTest(choice,classifier,testSet,testSetActual):
	print 'Naive Bayes Testing'
	#
	# if(choice==1):
	# 	print "accuracy Naive Bayes - Positive Negative:",mean(predictedTestResults == actualTestResults)*100
	# if(choice==2):
	# 	print "accuracy Naive Bayes - Stars:", mean(predictedTestResults == actualTestResults) * 100

#*******************************************************
				#HELPER FUNCTIONS
#*******************************************************

def removeStopWords(wordList):
	#Stopwords: Words that have no value in the context of sentiment analysis
	stopWordList = stopwords.words('english')
	stopWordList=[item.encode('utf-8') for item in stopWordList]
	stopWordList.remove('not')
	stopWordList.remove('nor')
	stopWordList.remove('no')
	stopWordList.remove('against')
	newList=[]
	for word in wordList:
		if word not in stopWordList:
			newList.append(word)
	return newList


classesCountDictionary={}
# 'boiled': {'positive': 24, 'negative': 7}
wordClassCountDictionary={}

#Increase count for every label
#Stores class:count Eg ->{'positive': 15787, 'negative': 4213}
def classCount(classLabel):
	#classesCountDictionary[classLabel]=classesCountDictionary.get(classLabel,0)+1
	if classLabel not in classesCountDictionary:
		classesCountDictionary[classLabel]=0
	classesCountDictionary[classLabel]+=1
	return classesCountDictionary

# 'boiled': {'positive': 24, 'negative': 7}
def wordClassCount(word,classLabel):
	if not word in wordClassCountDictionary:
		wordClassCountDictionary[word] = {}
	if classLabel not in wordClassCountDictionary[word]:
		wordClassCountDictionary[word][classLabel]=0
	wordClassCountDictionary[word][classLabel]+=1
	return wordClassCountDictionary


DEFAULT_PROB=0.000000001 #Random Probability Should be smallest probability when the word is not in trainset
def getWordProbability(word,classLabel,targetLabelCount,wordLabelCount):
	print "Word Probability"
	classCount=getClassCount(classLabel,targetLabelCount)
	try:
		wordFrequency=getWordFrequency(word,classLabel,wordLabelCount)
	except:
		return None
	if wordFrequency==None:
		return DEFAULT_PROB
	probability=wordFrequency/classCount
	return probability


#Returns class count of given class label Example <- getClassCount('positive;) - 15787
def getClassCount(classLabel,targetLabelCount):
	return targetLabelCount.get(classLabel)

def getWordFrequency(word,classLabel,wordLabelCount):
	try:
		wordExists=wordLabelCount[word]
	except:
		pass
	try:
		return wordExists[classLabel]
	except:
		return None
main()
