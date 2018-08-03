#!/usr/bin/env python

import sys
print sys.version

import os
from math import sqrt
import numpy as np
import array
from pyspark import SparkContext, SparkConf
conf=SparkConf()
from pyspark.mllib import fpm
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.util import MLUtils
import pyspark.mllib
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.evaluation import BinaryClassificationMetrics
import time

# initialize spark context
master = "spark://" + os.environ['SPARK_MASTER_NODE'] + ":" + os.environ['SPARK_MASTER_PORT']
print "master: ", master

conf.set("spark.python.profile", "true")
sc = fpm.SparkContext(master, appName="Python MLTest Spark Context")

t1=time.time()

# load alkemi training simulation data

filename = sys.argv[1]
trees = int(sys.argv[2])
num_bytes = 8 # np.float64
num_metrics = 3

recordLength = num_bytes * num_metrics # in bytes
record_rdd = sc.binaryRecords(filename, recordLength)
float_rdd= record_rdd.map(lambda byte_array: array.array('d', byte_array))
trainData = float_rdd.map(lambda line:LabeledPoint(line[2], [line[0:1]]))

# Train a RandomForest model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
#  Note: Use larger numTrees in practice.
#  Setting featureSubsetStrategy="auto" lets the algorithm choose.
model = RandomForest.trainRegressor(trainData, categoricalFeaturesInfo={},
                                     numTrees=trees, featureSubsetStrategy="auto",
                                     impurity='variance', maxDepth=4, maxBins=32)

print('Learned Regression forest model:')
print(model.toDebugString())

print ('Total Time: '+str(time.time()-t1))
