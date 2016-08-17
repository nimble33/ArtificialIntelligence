import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
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
	review,rating,trainingSize=divideTraining(TRAIN_SET,choice)
	timeNb=time.time()
	classifierNaiveBayes=nbTrain(choice, review, rating)
	if(choice==1):
		nbTest(choice,classifierNaiveBayes,TEST_SET,TEST_SET_ACTUAL_POS_NEG,trainingSize)
		print('Time taken Naive Bayes Pos Neg:', time.time()-timeNb)
	if(choice==2):
		nbTest(choice, classifierNaiveBayes, TEST_SET, TEST_SET_ACTUAL_STARS,trainingSize)
		print('Time taken Naive Bayes Stars:',   time.time()-timeNb)
	timeSVM=time.time()
	classifierSVM=svmTrain(choice, review, rating)
	if (choice == 1):
		svmTest(choice, classifierSVM, TEST_SET, TEST_SET_ACTUAL_POS_NEG,trainingSize)
		print('Time taken SVM Pos Neg:',  time.time()-timeSVM )
	if (choice == 2):
		svmTest(choice, classifierSVM, TEST_SET, TEST_SET_ACTUAL_STARS,trainingSize)
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
		trainingSize=len(trainReview)
	if(choice==1):
		return trainReview,trainPosNegRating,trainingSize
	if(choice==2):
		return trainReview,trainStarRating,trainingSize

def nbTrain(choice,review,rating):
	print '*******************************************************************'
	print 'Naive Bayes training'
	classifierNB = MultinomialNB()
	textClassifierNB = Pipeline([('vect', CountVectorizer(stop_words='english')),
								 ('tfidf', TfidfTransformer()),
								 ('clf', classifierNB), ])
	textClassifierNB = textClassifierNB.fit(review, rating)
	return textClassifierNB

testReviewsToPredict1=[]
testReviewsToPredict2=[]

actualTestResults1=[]
actualTestResults2=[]


#predictedTestResults=[]

def nbTest(choice,classifier,testSet,testSetActual,trainingSize):
	print 'Naive Bayes Testing'
	with open(testSet, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				testReviewsToPredict1.append(line[0])
	#ActualPosNeg/Stars takes from the argument
	with open(testSetActual, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				actualTestResults1.append(line[0])

	predictedTestResults = classifier.predict(testReviewsToPredict1)

	if (choice == 1):
		print "Classification report  Naive Bayes  Predefined - Positive Negative: "
		print "Training Size- No.of reviews:",trainingSize
		print "Testing Size- No.of reviews:",len(predictedTestResults)
		print metrics.classification_report(actualTestResults1, predictedTestResults)
		print
		print "Confusion matrix Naive Bayes Predefined - Positive Negative: "
		print metrics.confusion_matrix(actualTestResults1, predictedTestResults)
		print "accuracy Naive Bayes Predefined- Positive Negative: : ", accuracy_score(actualTestResults1, predictedTestResults)

	if (choice == 2):
		# print predictedTestResults
		# print actualTestResults1
		print "Classification report  Naive Bayes Predefined - Stars: "
		print "Training Size- No.of reviews:", trainingSize
		print "Testing Size- No.of reviews:", len(predictedTestResults)
		print
		print metrics.classification_report(actualTestResults1, predictedTestResults)
		print
		print "Confusion matrix Naive Bayes Predefined - Stars: "
		print metrics.confusion_matrix(actualTestResults1, predictedTestResults)
		print "accuracy Naive Bayes Predefined - Stars : ", accuracy_score(actualTestResults1, predictedTestResults)



def svmTrain(choice,review,rating):
	print '*******************************************************************'
	print 'SVM Training'
	classifierSVM = svm.LinearSVC()
	textClassifierSVM = Pipeline([('vect', CountVectorizer(stop_words='english')),
								 ('tfidf', TfidfTransformer()),
								 ('clf', classifierSVM), ])
	textClassifierSVM = textClassifierSVM.fit(review, rating)
	return textClassifierSVM

def svmTest(choice,classifier,testSet,testSetActual,trainingSize):

	print 'SVM Testing'
	with open(testSet, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				testReviewsToPredict2.append(line[0])
	#ActualPosNeg/Stars takes from the argument
	with open(testSetActual, 'rU') as f:
		lines = csv.reader(f)
		i = 0
		for line in lines:
			if (line):
				actualTestResults2.append(line[0])

	predictedTestResults = classifier.predict(testReviewsToPredict2)
	#print predictedTestResults
	#print actualTestResults
	if(choice==1):

		print "Classification report  SVM  Predefined - Positive Negative: "
		print "Training Size- No.of reviews:", trainingSize
		print "Testing Size- No.of reviews:", len(predictedTestResults)
		print
		print metrics.classification_report(actualTestResults2, predictedTestResults)
		print
		print "Confusion matrix SVM Predefined - Positive Negative: "
		print metrics.confusion_matrix(actualTestResults2, predictedTestResults)
		print "accuracy SVM Predefined- Positive Negative: : ",accuracy_score(actualTestResults2, predictedTestResults)


	if(choice==2):
		print "Classification report  SVM Predefined - Stars: "
		print "Training Size- No.of reviews:", trainingSize
		print "Testing Size- No.of reviews:", len(predictedTestResults)
		print
		print metrics.classification_report(actualTestResults2, predictedTestResults)
		print
		print "Confusion matrix SVM Predefined - Stars: "
		print metrics.confusion_matrix(actualTestResults2, predictedTestResults)
		print "accuracy SVM Predefined - Stars : ", accuracy_score(actualTestResults2, predictedTestResults)

main()
