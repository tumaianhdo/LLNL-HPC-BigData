#!/bin/sh
# WORK_HOME is required to run the script
if [ x${WORK_HOME} == x ]; then
    echo "Please set WORK_HOME"
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
rm -rf ${HOME}/.pegasus/workflow.db
rm -rf ${HOME}/.pegasus/ensembles/*
rm -rf ${WORK_HOME}/workflows/*
rm -rf ${WORK_HOME}/test.out

# Prepare Pegasus Ensembles
pegasus-db-admin update
pegasus-em server &
/bin/sleep 10

# Run in-situ jobs 
pegasus-em create -v ${WORK_HOME}/event-config a
pegasus-em config a -P 3 -R 3