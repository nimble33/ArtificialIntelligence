from __future__ import division
import csv
import time
from sklearn import metrics
from sklearn.metrics import accuracy_score
import re
from nltk.corpus import stopwords

'''
Entry Point
'''
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
		timeNb=time.time()
		predictedResultList=naiveBayesClassifyAndTest(choice,targetLabelCount,wordLabelCount,TEST_SET)
		print predictedResultList
		actualResultListPosNeg=getActualListPosNeg(TEST_SET_ACTUAL_POS_NEG,choice)
		actualResultListStars = getActualListStars(TEST_SET_ACTUAL_STARS,choice)
		if(choice==1):
			resultAnalysis(predictedResultList,actualResultListPosNeg,choice)
			print "Time in seconds -  Naive Bayes User Defined - Positive Negative: ",time.time()-timeNb
		if(choice==2):
			resultAnalysis(predictedResultList,actualResultListStars,choice)
			print "Time in seconds -  Naive Bayes User Defined - Stars: ", time.time()-timeNb

'''
Divides the Entry set to two dictionaries
1.Dictionary with classes and counts
2.Dictionary with word,class and its frequency
'''
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


#Holds the final probability values of the classes
finalProbability={}
#Holds the test Results of every review in the testSet
testResults=[]

'''
		Naive Bayes Probability:
		References:
		1.http://sebastianraschka.com/Articles/2014_naive_bayes_1.html
		2.https://en.wikipedia.org/wiki/Naive_Bayes_classifier
		P(class|review)= p(class)* p(review|class)
		probability= (prior * likelihood)/evidence ~(read directly propotional) (prior * likelihood)
			We ignore the denominator because of the following [wikipedia reference]:
			In practice, there is interest only in the numerator of that fraction,
			because the denominator does not depend on  and the values of the
			features are given,  so that the denominator is effectively constant.
			Example p(positive|review) = (positive prior * likelihood of review being positive)/evidence
					p(negative|review) = (negative prior * likelihood of review being negative)/evidence
			We'll be comparing the above positive and negative posterior probabilities and hence the
			denominator of right hand sides of the above probabilities is unnecessary

		To classify the review as either positive or negative according to the above example we need
		i. Calculation of Prior
		ii. Likelihood

		P(class|review)= p(class)* p(review|class) class belongs to one of [positive,negative,1,2,3,4,5]


		Step 1. Calculation of Prior: p(class)


			The calculation of prior is pretty straight forward
			p(class)=no. of reviews classified to that class/total number of reviews
			where class in the current scenario can be [positive/negative] or in the range
			of [1,5]

		Step 2. Calculation of Likelihood: p(review|class)

			To calculate likelihood i.e. p(review|class)
			Note: We know that a review is a set of words
			p(review|class) = p(word1|class)*p(word2|class)*...............p(wordn|class)

			Now to calculate p(wordi|class) can be read as the probability of word belonging to a class

			if word already existing in the training set:
			p(word|class) = wordfrequency in the training set/class frequency
			if word not present in the training set:
			p(word|class) = some probability which is minute

		Step 3. Calculating the final probabilty

			final probability[class] = Step 2 * Step 3

		Step 4: Classification of Review - Prediction

			Get Maximum of probabilities of all the classes,  and assign the review with the class
			having the maximum probability

		'''

'''
Takes in training set dictionaries, test set to predict
returns finalprobability dictionary and test results
'''
def naiveBayesClassifyAndTest(choice,targetLabelCount,wordLabelCount,testSetPath):
	print 'Naive Bayes test'
	#Total Size
	totalReviewsInDataSet=sum(targetLabelCount.values())

	#print totalReviewsInDataSet
	#Labels either [positive,negative] or [1,2,3,4,5]
	classLabels = targetLabelCount.keys()
	#Explore test set

	with open(testSetPath, 'rU') as f:
		lines = csv.reader(f)
		count=0
		for line in lines:
			count+=1
			# print 'line'
			print count, line
			if len(line)==1:
				wordSplit = re.split('\s+', line[0].lower())
				wordNoStopWords = removeStopWords(wordSplit)
				#Arrange as list
				words=list(wordNoStopWords)
				# print "words in line"
				# print words
				#Mapping each word to a classlabel
				for classLabel in classLabels:
					'''
					#1. Calculation of Prior:
					p(class)=no. of reviews classified to that class/total number of reviews
					'''
					# Positive/Negative Scenario
					countReviewSpecificClassLabel=getClassCount(classLabel,targetLabelCount)
					priorProbability=getPriorProbability(countReviewSpecificClassLabel,totalReviewsInDataSet)

					'''
					2. Calculation of Likelihood
					'''
					wordProbability = []
					#Calculating Individual word probabilities p(word/class)
					for word in words:
						wordOccurence=getWordOccurence(word,classLabel,wordLabelCount)
						classCount=getClassCount(classLabel,targetLabelCount)
						wordProbability.append(wordOccurence/classCount)


					#Product of individual likelihoods
					likelihood=1.0
					for indivWordProb in wordProbability:
						likelihood*=indivWordProb


					'''
					3. Calculation of Final Probability
					'''
					finalProbability[classLabel] = likelihood * priorProbability
					#print finalProbability
					'''
					4. Classification of Review - Prediction
					'''
				if(choice==1):
					positiveScore = finalProbability.get('positive')
					negativeScore = finalProbability.get('negative')
					if (positiveScore > negativeScore):
						testResults.append('positive')
					else:
						testResults.append('negative')
				if(choice==2):
					score1 = finalProbability.get('1')
					score2 = finalProbability.get('2')
					score3 = finalProbability.get('3')
					score4 = finalProbability.get('4')
					score5 = finalProbability.get('5')
					scoreList = [score1, score2, score3, score4, score5]
					maxValue = max(scoreList)
					if (maxValue == score1):
						testResults.append('1')
					elif (maxValue == score2):
						testResults.append('2')
					elif (maxValue == score3):
						testResults.append('3')
					elif (maxValue == score4):
						testResults.append('4')
					else:
						testResults.append('5')
	return testResults

#Evaluation of results
def resultAnalysis(predicted,actual,choice):
	print 'result analysis'
	# count = 0
	# for i in range(0, len(predicted)):
	# 	# if (predicted[i] == actual[i]):
	# 	# 	count += 1
	'''
	Precision: Fraction of retrieved instances that are relevant/How useful the search results are tp/tp+fp
	Recall: Fraction of relevant instances that retrived/How complete the search results are tp/tp+fn
	Fmeasure:harmonic mean of precision and recall - how well we are doing like an average
	support: occurences of classes in the dataset

	'''
	if(choice==1):
		print "Classification report  Naive Bayes User Defined - Positive Negative: "
		print
		print metrics.classification_report(actual, predicted)
		print
		print "Confusion matrix Naive Bayes User Defined - Positive Negative: "
		print metrics.confusion_matrix(actual, predicted)
		print "accuracy Naive Bayes User Defined - Positive Negative: : ",accuracy_score(actual, predicted)


	if(choice==2):
		print "Classification report  Naive Bayes User Defined - Stars: "
		print
		print metrics.classification_report(actual, predicted)
		print
		print "Confusion matrix Naive Bayes User Defined - Stars: "
		print metrics.confusion_matrix(actual, predicted)
		print "accuracy Naive Bayes User Defined - Stars : ", accuracy_score(actual, predicted)







#**********************************************************************************
								#HELPER FUNCTIONS
#***********************************************************************************

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


#Returns the prior probability which is
def getPriorProbability(part,total):
	return part/total


#Returns class count of given class label Example <- getClassCount('positive;) - 15787
def getClassCount(classLabel,targetLabelCount):
	return targetLabelCount.get(classLabel)

def getWordOccurence(word,classLabel,wordLabelCount):
	if word in wordLabelCount.keys():
		wordInTrainSet = wordLabelCount[word]
		if classLabel in wordInTrainSet.keys():
			return wordInTrainSet[classLabel]
		else:
			return 0.000000001
	else:
		return 0.000000001

actualTestResultsPosNeg=[]


def getActualListPosNeg(actualTestSet,choice):
	with open(actualTestSet, 'rU') as f:
		lines = csv.reader(f)
		for line in lines:
			if (line):
				actualTestResultsPosNeg.append(line[0])
	return actualTestResultsPosNeg


actualTestResultsStars=[]
def getActualListStars(actualTestSet,choice):
	with open(actualTestSet, 'rU') as f:
		lines = csv.reader(f)
		for line in lines:
			if (line):
				actualTestResultsStars.append(line[0])
	return actualTestResultsStars


main()