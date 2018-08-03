#!/usr/bin/env python

import sys, os, time, getopt
print sys.version
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
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.feature import StringIndexer
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.sql import *

#create a spark session we need, no need for sparkContext since spark session includes a sparkcontext.
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("HPC and BIG Data") \
    .config("spark.python.profile", "true") \
    .getOrCreate()


# initialize spark context
master = os.environ['MASTER']
print "master: ", master



t1=time.time()

# load alkemi training simulation data

#filename = "file:///p/lscratchd/briang/alkemi/data/learning/v3/train-256.npy"
#filename = "file:///p/lscratchd/briang/alkemi/data/learning/v3/train-1.npy"
#filename = "file:///p/lscratchd/briang/alkemi/data/learning/bigger/big.npy"
#filename = "file:///p/lscratchd/briang/alkemi/data/learning/bigger/biggest.npy"
filename = sys.argv[1]
trees = int(sys.argv[3])

num_bytes = 4 # np.float64
num_metrics = 17
recordLength = num_bytes * num_metrics # in bytes

#Read binary data
record_rdd = spark.sparkContext.binaryRecords(filename, recordLength)
#create a typed RDD
float_rdd= record_rdd.map(lambda byte_array: array.array('f', byte_array))
#group fetures in a dense vector 
trainData = float_rdd.map(lambda line:(Vectors.dense(line[0:15]), line[16]))
#define the schema "label" is the class to be predicted
schema=["features","label"]
#Create a dataframe
df=spark.createDataFrame(trainData,schema)
# Automatically identify categorical features, and index them.
# Set maxCategories so features with > 4 distinct values are treated as continuous.
#featureIndexer =VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(df)
#define the label and index it
#labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)
# Train a RandomForest model.
#rf = RandomForestRegressor(featuresCol="indexedFeatures")
rf= RandomForestRegressor(labelCol="label",numTrees=trees,impurity='variance', maxDepth=4)
# Chain indexer and forest in a Pipeline
#pipeline = Pipeline(stages=[featureIndexer, rf])
# Train a RandomForest model.this also runs the indexer.
#model = pipeline.fit(df)
rfModel=rf.fit(df)
print('Learned Regression forest model:')
#print(rfModel.stages(2))

print ('Total Time: '+str(time.time()-t1))
