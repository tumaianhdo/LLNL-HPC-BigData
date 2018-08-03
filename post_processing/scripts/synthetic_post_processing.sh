#!/bin/sh

echo "The script is currently running on host"
/usr/bin/hostname

if [ $# -ne 1 ]; then
    echo "Usage: $0 DATA_PLACEMENT"
    exit 1
fi
data_placement=$1

# POPR_WORK_HOME is required to run the script
if [ x${POPR_WORK_HOME} == x ]; then
    echo "Please set POPR_WORK_HOME"
    exit
fi

# Prepare Magpie's evironment variables
source ${HOME}/my-job-env

# Prepare Condor's environment variables
source ${HOME}/set-env -c

# Prepare Pegasus's environment variables
source ${HOME}/set-env -p 

# Prepare Hadoop & Spark's environment variables 
source ${HOME}/set-env -hs

# Clean up previous runs
if [ "${data_placement}" = "nvm" ]; then
	hdfs dfs -rm -f /data_test_*
else 
	rm -rf /p/lscratchd/do7/data/data_test_*
fi;

rm -rf ${POPR_WORK_HOME}/scripts/${USER}
rm -rf ${HOME}/.pegasus/workflow.db
rm -rf ${HOME}/.pegasus/ensembles/*
rm -rf /p/lscratchd/do7/do7
rm -rf /p/lscratchd/do7/log/*

# Pegasus
pegasus-db-admin update
${POPR_WORK_HOME}/generate_dax.py ${POPR_WORK_HOME}/post-process.dax.${data_placement} ${data_placement}
# cp ${POPR_WORK_HOME}/input/simulation/extract.py.${data_placement} ${POPR_WORK_HOME}/input/simulation/extract.py
cp ${POPR_WORK_HOME}/input/synthetic/generator.py.${data_placement} ${POPR_WORK_HOME}/input/synthetic/generator.py
${POPR_WORK_HOME}/plan_dax.sh ${POPR_WORK_HOME}/post-process.dax.${data_placement}