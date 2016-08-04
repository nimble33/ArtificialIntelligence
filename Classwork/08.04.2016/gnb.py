# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 16:30:03 2016

@author: nephi
"""

from sklearn.datasets import load_iris
iris = load_iris()

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
print "target"
print iris.target
print "predicted"
print y_pred 