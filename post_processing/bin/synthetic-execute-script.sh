#!/bin/bash
# before launching the job set environment variable
source ${HOME}/my-job-env
source ${HOME}/set-env -hs
# lauch the job using srun
srun --jobid=${MAGPIE_JOB_ID} -N ${HADOOP_SLAVE_COUNT} -n ${HADOOP_SLAVE_COUNT} -c 1 --exclude=${HADOOP_MASTER_NODE} python "$@"
