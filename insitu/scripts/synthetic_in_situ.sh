#!/bin/sh

echo "The script is currently running on host"
/usr/bin/hostname

if [ $# -ne 1 ]; then
    echo "Usage: $0 DATA_PLACEMENT"
    exit 1
fi
data_placement=$1

# INST_WORK_HOME is required to run the script
if [ x${INST_WORK_HOME} == x ]; then
    echo "Please set INST_WORK_HOME"
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
	rm -rf /p/lscratchd/do7/data/*
fi;
rm -rf ${INST_WORK_HOME}/scripts/${USER}
rm -rf ${HOME}/.pegasus/workflow.db
rm -rf ${HOME}/.pegasus/ensembles/*
rm -rf ${INST_WORK_HOME}/synthetic/${USER}
rm -rf ${INST_WORK_HOME}/analysis/workflows/*
rm -rf /p/lscratchd/do7/do7
rm -rf /p/lscratchd/do7/log/*

# Prepare Pegasus Ensembles
pegasus-db-admin update
pegasus-em server &
/bin/sleep 10

# Run in-situ jobs 
pegasus-em create -v ${INST_WORK_HOME}/config/event-config.${data_placement} a
pegasus-em config a -P 100 -R 100
cp ${INST_WORK_HOME}/synthetic/input/generator.py.${data_placement} ${INST_WORK_HOME}/synthetic/input/generator.py
${INST_WORK_HOME}/synthetic/generate_dax.py ${INST_WORK_HOME}/synthetic/synthetic-test.dax
pegasus-em submit a.mpi ${INST_WORK_HOME}/synthetic/plan_dax.sh ${INST_WORK_HOME}/synthetic/synthetic-test.dax

# sleep should be time for sbatch job - (mapgie start + magpie shutdown time)
# /bin/sleep 180000