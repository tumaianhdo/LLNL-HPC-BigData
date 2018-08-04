#!/bin/sh

if [ x${POPR_WORK_HOME} == x ]; then
    echo "Please set POPR_WORK_HOME"
    exit
fi

source ${POPR_WORK_HOME}/magpie/my-job-env

mkdir ${POPR_WORK_HOME}/software/

${HOME}/software/source/condor-8.6.11/condor_install --install-dir=${POPR_WORK_HOME}/software/condor --local-dir=/tmp/${USER}/condor --verbose

source ${POPR_WORK_HOME}/magpie/set-env.sh -hscpy

condor_master

cp -r ${HOME}/software/source/pegasus/dist/pegasus-4.8.0dev ${POPR_WORK_HOME}/software/pegasus
