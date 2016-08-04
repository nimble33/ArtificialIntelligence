# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 16:42:48 2016

@author: nephi
"""

from sklearn.datasets import load_iris
iris = load_iris()

from sklearn import svm
svm=svm.SVC()
y_pred = svm.fit(iris.data, iris.target).predict(iris.data)
print "target"
print iris.target
print "predicted"
print y_pred 
print("Number of mislabeled points out of a total %d points : %d"   % (iris.data.shape[0],(iris.target != y_pred).sum()))