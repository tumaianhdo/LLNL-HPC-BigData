#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import os
import sys
import numpy as np
import array

# get/create Spark session
spark = SparkSession \
    .builder \
    .appName("HPC and BIG Data") \
    .config("spark.python.profile", "true") \
    .getOrCreate()


filename = sys.argv[1]
print (filename)

num_bytes = 8 # np.float64
num_metrics = 128*128*128 # fixed number of metrics
#
recordLength = num_bytes * num_metrics

# read binary data under rdd of records
record_rdd = spark.sparkContext.binaryRecords(filename, recordLength)
# convert rdd of byte records to rdd of float64 
float_rdd = record_rdd.map(lambda byte_array: array.array('d', byte_array))
# calculate sum
sum_rdd = float_rdd.map(lambda array: np.sum(array))
# print
print (sum_rdd.collect())


