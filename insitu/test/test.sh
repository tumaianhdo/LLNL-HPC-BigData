#!/bin/sh
source ${HOME}/my-job-env
source ${HOME}/set-env -hs
a=$((${HADOOP_SLAVE_COUNT}*2))
echo $a
