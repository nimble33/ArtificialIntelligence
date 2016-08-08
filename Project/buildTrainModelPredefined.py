#natural language toolkit
#regular expressions
import re
import collections
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from sklearn.metrics import confusion_matrix

import time
import csv


start=time.time()
trainReview=[]
trainRating=[]

testReview=[]
testActualRating=[]

with open('train/trainActual.csv', 'rU') as f:

	lines = csv.reader(f)
	i=0
	for line in lines:
		if len(line)==2:
			
			#print 'Word No Stopwords',wordNoStopWords
			#count the number of times a word has occurred in the list
			trainReview.append(line[1])
			trainRating.append(line[0])
   
with open('test/testPredict.csv', 'rU') as f:

	lines = csv.reader(f)
	i=0
	for line in lines:
		if (line):

		
			#print 'Word No Stopwords',wordNoStopWords
			#count the number of times a word has occurred in the list
			testReview.append(line[0])


classifier=MultinomialNB()
textClassifier=Pipeline([('vect', CountVectorizer(stop_words='english')),
                        ('tfidf', TfidfTransformer()),
                        ('clf', classifier),])
textClassifier=textClassifier.fit(trainReview,trainRating)
predicted = textClassifier.predict(testReview)
with open('test/testActual.csv', 'rU') as f:

	lines = csv.reader(f)
	i=0
	for line in lines:
		if (line):

		
			#print 'Word No Stopwords',wordNoStopWords
			#count the number of times a word has occurred in the list
			testActualRating.append(line[0])

f = open("myfile.txt", "w")
f.write("\n".join(map(lambda x: str(x), predicted)) + "\n")
f.close()





