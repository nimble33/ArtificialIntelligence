import json,os
import re


#Contains the Original Values as Positive/Negative classification
trainActual = open('train/trainActual.csv','w+')
#Contains just the review. Should predict on these reviews
trainActualStars = open('train/trainActualStars.csv','w+')


def main():
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	dataFilePath= os.path.abspath('yelp_dataset_train_20000.json')
	dataContainer=readData(dataFilePath)
	for review_data in dataContainer:
		reviewText=review_data['text']
		no_punct = ""
		for char in reviewText:
			if char not in punctuations:
				no_punct = no_punct + char

		reviewRating = review_data['stars']
		if reviewRating >= 3:
			polarity = "positive"
		if reviewRating < 3:
			polarity = "negative"
		trainActual.write(polarity+","+no_punct.replace('\n',' ').encode('utf8')+"\n")
		trainActualStars.write(str(reviewRating) + "," + no_punct.replace('\n', ' ').encode('utf8') + "\n")


def readData(filePath):
	data = []
	with open(filePath) as f:
   		for line in f:
   			data.append(json.loads(line))
   		return data


def removePunctuation(wordList):
	punctuation = re.compile(r'[,./?!":;|-]')
	punct_remove = [punctuation.sub(" ", word) for word in wordList]
	return punct_remove

main()
