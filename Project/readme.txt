Sentiment Analysis of Yelp Reviews

The dataset used for the project can be found at: https://www.yelp.com/dataset_challenge

---------------------------------------------------------------------------------------------------
SETUP INSTRUCTIONS
---------------------------------------------------------------------------------------------------
1. Download this repository.
2. Open Project folder and make sure the .json training and testing sets are downloaded
3. The project needs python 2.7(tested on 2.7)/3.5, nltk,scikitlearn libraries 
4. To run:
	i.  python getTrainFileCsv.py -> converts json train file to csv and stores it in train/ directory
	ii. python getTestFileCsv.py  -> converts json test file to csv and stores it in test/ directory
	iii.python trainAndTestNaiveBayesUserDefined.py(Program with naive bayes implemented from scratch)
	Above command Prompts user to enter-> Select 1 or 2
			 *1-Predicts the review either positive or negative*  *2- Predicts the review with a rating within [1-5]:
	iv. python trainAndTestPredefined.py(Program with naive bayes and svm classification techniques from scikit library - used for benchmarking)
	Above command Prompts user to enter-> Select 1 or 2
			 *1-Predicts the review either positive or negative*  *2- Predicts the review with a rating within [1-5]:


--------------------------------------------------------------------------------------------------
ANALYSIS:
--------------------------------------------------------------------------------------------------
1. Naive Bayes from Scratch:


A. POSITIVE NEGATIVE PREDICTION: Accurarcy =74%

result analysis
Classification report  Naive Bayes User Defined - Positive Negative:

             precision    recall  f1-score   support

   negative       0.42      0.56      0.48        43
   positive       0.87      0.79      0.83       157

avg / total       0.77      0.74      0.75       200


Confusion matrix Naive Bayes User Defined - Positive Negative:
[[ 24  19]
 [ 33 124]]
accuracy Naive Bayes User Defined - Positive Negative: :  0.74
Time in seconds -  Naive Bayes User Defined - Positive Negative:  58.6369998455

B. RATING [1-5] PREDICTION: Accuracy =39.5%

result analysis
Classification report  Naive Bayes User Defined - Stars: 

             precision    recall  f1-score   support

          1       0.35      0.58      0.44        19
          2       0.38      0.25      0.30        24
          3       0.28      0.32      0.30        41
          4       0.47      0.49      0.48        77
          5       0.42      0.28      0.34        39

avg / total       0.40      0.40      0.39       200


Confusion matrix Naive Bayes User Defined - Stars:
[[11  2  3  2  1]
 [ 4  6  7  6  1]
 [ 8  2 13 16  2]
 [ 7  2 19 38 11]
 [ 1  4  5 18 11]]
accuracy Naive Bayes User Defined - Stars :  0.395
Time in seconds -  Naive Bayes User Defined - Stars:  115.355000019



2. Using Scikit Library:

A. POSITIVE NEGATIVE PREDICTION: 
i. Naive Bayes:  Accuracy =78.5%
Naive Bayes training -
Naive Bayes Testing
Classification report  Naive Bayes  Predefined - Positive Negative:
Training Size- No.of reviews: 20000
Testing Size- No.of reviews: 200

             precision    recall  f1-score   support

   negative       0.00      0.00      0.00        43
   positive       0.79      1.00      0.88       157

avg / total       0.62      0.79      0.69       200


Confusion matrix Naive Bayes Predefined - Positive Negative:
[[  0  43]
 [  0 157]]
accuracy Naive Bayes Predefined- Positive Negative: :  0.785
('Time taken Naive Bayes Pos Neg:', 2.2940001487731934)

ii. SVM - Accuracy - 85.5%

SVM Training
SVM Testing
Classification report  SVM  Predefined - Positive Negative:
Training Size- No.of reviews: 20000
Testing Size- No.of reviews: 200

             precision    recall  f1-score   support

   negative       0.77      0.47      0.58        43
   positive       0.87      0.96      0.91       157

avg / total       0.85      0.85      0.84       200


Confusion matrix SVM Predefined - Positive Negative:
[[ 20  23]
 [  6 151]]
accuracy SVM Predefined- Positive Negative: :  0.855
('Time taken SVM Pos Neg:', 2.5320000648498535)

B. RATING [1-5] PREDICTION:

i. Naive Bayes:  Accuracy =40.5%

Naive Bayes training
Naive Bayes Testing
Classification report  Naive Bayes Predefined - Stars:
Training Size- No.of reviews: 20000
Testing Size- No.of reviews: 200

             precision    recall  f1-score   support

          1       0.00      0.00      0.00        19
          2       0.00      0.00      0.00        24
          3       0.00      0.00      0.00        41
          4       0.43      0.66      0.52        77
          5       0.37      0.77      0.50        39

avg / total       0.24      0.41      0.30       200


Confusion matrix Naive Bayes Predefined - Stars:
[[ 0  0  0  9 10]
 [ 0  0  0 21  3]
 [ 0  0  0 28 13]
 [ 0  0  0 51 26]
 [ 0  0  0  9 30]]
accuracy Naive Bayes Predefined - Stars :  0.405
('Time taken Naive Bayes Stars:', 2.2370002269744873)

ii. SVM - Accuracy - 48%

SVM Training
SVM Testing
Classification report  SVM Predefined - Stars:
Training Size- No.of reviews: 20000
Testing Size- No.of reviews: 200

             precision    recall  f1-score   support

          1       0.56      0.53      0.54        19
          2       0.50      0.25      0.33        24
          3       0.43      0.24      0.31        41
          4       0.53      0.51      0.52        77
          5       0.42      0.79      0.55        39

avg / total       0.49      0.48      0.46       200


Confusion matrix SVM Predefined - Stars:
[[10  0  4  3  2]
 [ 6  6  4  7  1]
 [ 2  3 10 16 10]
 [ 0  3  5 39 30]
 [ 0  0  0  8 31]]
accuracy SVM Predefined - Stars :  0.48
('Time taken SVM Stars:', 3.7039999961853027)

--------------------------------------------------------------------------------------------------
Under Development:TeFy: Text Classify
--------------------------------------------------------------------------------------------------

An UI based on Sentiment Analysis: It can be found here: http://nimble33.pythonanywhere.com/




