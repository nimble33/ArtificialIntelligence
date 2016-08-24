import json,os

#Contains the Original Values as Positive/Negative classification
testActual = open('test/testActual.csv','w+')
#Contains the Original Values as [1,5] classification
testActualStars = open('test/testActualStars.csv','w+')
#Contains just the review. Should predict on these reviews
testPredict=open('test/testPredict.csv','w+')

def main():
	# Preprocessing: Remove Punctuation
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	# Change this path value to test if you have a different dataset
	dataFilePath= os.path.abspath('yelp_dataset_test_200.json')
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
		#print polarity+", "+no_punct.replace('\n',' ').encode('utf8')+"\n"
		testActual.write(polarity+", "+no_punct.replace('\n',' ').encode('utf8')+"\n")
		testActualStars.write(str(reviewRating) + ", " + no_punct.replace('\n', ' ').encode('utf8') + "\n")
		testPredict.write(no_punct.replace('\n',' ').encode('utf8')+"\n")

def readData(filePath):
	data = []
	with open(filePath) as f:
   		for line in f:
   			data.append(json.loads(line))
   		return data

main()
