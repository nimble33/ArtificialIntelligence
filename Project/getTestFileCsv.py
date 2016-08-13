import json,os

testActual = open('test/testActual.csv','w+')
testActualStars = open('test/testActualStars.csv','w+')
testPredict=open('test/testPredict.csv','w+')

def main():
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	dataFilePath= os.path.abspath('yelp_dataset_test_5000.json')
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
		testActual.write(polarity+", "+no_punct.replace('\n',' ').encode('utf8')+"\n")
		testActualStars.write(str(reviewRating) + ", " + no_punct.replace('\n', ' ').encode('utf8') + "\n")
		testPredict.write(no_punct.replace('\n',' ').encode('utf8')+"\n")

def readData(filePath):
	data = []
	with open(filePath) as f:
   		for line in f:
   			data.append(json.loads(line))
   		return data
if __name__ == '__main__':
  main()
