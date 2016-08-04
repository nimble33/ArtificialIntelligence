import json,os

def main():
	
	dataFilePath= os.path.abspath('yelp_sample_review_data.json')
	dataContainer=readData(dataFilePath)
	sampleReview=dataContainer[0];
	reviewText=sampleReview['text']
	print "Reading"
	print reviewText
	print "Length of the data file entries"
	print len(dataContainer)

def readData(filePath):
	data = []
	with open(filePath) as f:
   		for line in f:
   			data.append(json.loads(line))
   		return data


if __name__ == '__main__':
  main()



