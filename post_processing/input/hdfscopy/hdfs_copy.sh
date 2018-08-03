#!/bin/sh
source ${HOME}/my-job-env
source ${HOME}/set-env -h
hdfs dfs -put /l/ssd/data_test_* /