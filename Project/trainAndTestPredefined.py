import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from numpy import mean
import time


# Holds the review of training data
trainReview=[]
#Holds the rating i.e. either positive or negative
trainPosNegRating=[]
#Holds the rating i.e within the range [1,5]
trainStarRating=[]

def main():
	choice=input("Select 1 or 2 \n *1-Predicts the review either positive or negative*  *2- Predicts the review with a rating within [1-5]:\n")
	if(choice==1):
		TRAIN_SET='train/trainActual.csv'
	if(choice==2):
		TRAIN_SET='train/trainActualStars.csv'
	TEST_SET='test/testPredict.csv'
	TEST_SET_ACTUAL_POS_NEG = 'test/testActual.csv'
	TEST_SET_ACTUAL_STARS='test/testActualStars.csv'
	review,rating=divideTraining(TRAIN_SET,choice)
	timeNb=time.time()
	classifierNaiveBayes=nbTrain(choice, review, rating)
	if(choice==1):
		nbTest(choice,classifierNaiveBayes,TEST_SET,TEST_SET_ACTUAL_POS_NEG)
		print('Time taken Naive Bayes Pos Neg:', time.time()-timeNb)
	if(choice==2):
		nbTest(choice, classifierNaiveBayes, TEST_SET, TEST_SET_ACTUAL_STARS)
		print('Time taken Naive Bayes Stars:',   time.time()-timeNb)
	timeSVM=time.time()
	classifierSVM=svmTrain(choice, review, rating)
	if (choice == 1):
		svmTest(choice, classifierSVM, TEST_SET, TEST_SET_ACTUAL_POS_NEG)
		print('Time taken SVM Pos Neg:',  time.time()-timeSVM )
	if (choice == 2):
		svmTest(choice, classifierSVM, TEST_SET, TEST_SET_ACTUAL_STARS)
		print('Time taken SVM Stars:',time.time()- timeSVM )


def divideTraining(trainSet,choice):

	with open(trainSet, 'rU') as f:
		lines = csv.reader(f)
		for line in lines:
			if len(line) == 2:
				trainReview.append(line[1])
				if(choice==1):
					trainPosNegRating.append(line[0])
				if(choice==2):
					trainStarRating.append(line[0])
	if(choice==1):
		return trainReview,trainPosNegRating
	if(choice==2):
		return trainReview,trainStarRating

def nbTrain(choice,review,rating):
	print 'Naive Bayes training'
	classifierNB = MultinomialNB()
	textClassifierNB = Pipeline([('vect', CountVectorizer(stop_words='english')),
								 ('tfidf', TfidfTransformer()),
								 ('clf', classifierNB), ])
	textClassifierNB = textClassifierNB.fit(review, rating)
	return textClassifierNB

testReviewsToPredict=[]
actualTestResults=[]

#predictedTestResults=[]

def nbTest(choice,classifier,testSet,testSetActual):
	print 'Naive Bayes Testing'
	with open(testSet, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				testReviewsToPredict.append(line[0])
	#ActualPosNeg/Stars takes from the argument
	with open(testSetActual, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				actualTestResults.append(line[0])

	predictedTestResults = classifier.predict(testReviewsToPredict)
	print predictedTestResults
	print actualTestResults
	if(choice==1):
		print "accuracy Naive Bayes - Positive Negative:",mean(predictedTestResults == actualTestResults)*100
	if(choice==2):
		print "accuracy Naive Bayes - Stars:", mean(predictedTestResults == actualTestResults) * 100



def svmTrain(choice,review,rating):
	print 'SVM Training'
	classifierSVM = svm.LinearSVC()
	textClassifierSVM = Pipeline([('vect', CountVectorizer(stop_words='english')),
								 ('tfidf', TfidfTransformer()),
								 ('clf', classifierSVM), ])
	textClassifierSVM = textClassifierSVM.fit(review, rating)
	return textClassifierSVM

def svmTest(choice,classifier,testSet,testSetActual):
	print 'SVM Testing'
	with open(testSet, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				testReviewsToPredict.append(line[0])
	#ActualPosNeg/Stars takes from the argument
	with open(testSetActual, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				actualTestResults.append(line[0])

	predictedTestResults = classifier.predict(testReviewsToPredict)
	print predictedTestResults
	print actualTestResults
	if(choice==1):
		print "accuracy SVM - Positive Negative:",mean(predictedTestResults == actualTestResults)*100
	if(choice==2):
		print "accuracy SVM - Stars:", mean(predictedTestResults == actualTestResults) * 100

main()
