#!/bin/sh

echo "The script is currently running on host"
/usr/bin/hostname

# INST_WORK_HOME is required to run the script
if [ x${INST_WORK_HOME} == x ]; then
    echo "Please set INST_WORK_HOME"
    exit
fi

# Prepare Magpie's evironment variables
source ${HOME}/my-job-env

# Install personal Condor pool
rm -rf ${HOME}/software/install/condor/

${HOME}/software/source/condor-8.6.11/condor_install --install-dir=${HOME}/software/install/condor --local-dir=/tmp/${USER}/condor --verbose

# Prepare Condor's environment variables
source ${HOME}/set-env -c
condor_master

# Prepare Pegasus's environment variables
source ${HOME}/set-env -p 

# Prepare Hadoop & Spark's environment variables 
source ${HOME}/set-env -hs

# Clean up previous runs
# hdfs dfs -rm -f /data_test_*
# rm -rf ${HOME}/.pegasus/workflow.db
# rm -rf ${HOME}/.pegasus/ensembles/*
# rm -rf ${INST_WORK_HOME}/cloverleaf/${USER}
# rm -rf ${INST_WORK_HOME}/cloverleaf/ascenttest/
# rm -rf ${INST_WORK_HOME}/spark-pegasus/workflow/*

# # Prepare Pegasus Ensembles
# pegasus-db-admin update
# pegasus-em server &
# /bin/sleep 10

# # Run jobs
# pegasus-em create -v ${INST_WORK_HOME}/config/event-config a
# pegasus-em config a -P 100 -R 100
# pegasus-em submit a.mpi ${INST_WORK_HOME}/cloverleaf/plan_dax.sh ${INST_WORK_HOME}/cloverleaf/ascent-test.dax

# sleep should be time for sbatch job - (mapgie start + magpie shutdown time)
# /bin/sleep 180000