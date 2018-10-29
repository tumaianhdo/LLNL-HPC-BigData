#!/bin/sh

source ${HOME}/my-job-env

rm -rf ${HOME}/software/install/condor

${HOME}/software/source/condor-8.6.11/condor_install --install-dir=${HOME}/software/install/condor --local-dir=/tmp/${USER}/condor --verbose

source ${HOME}/set-env -hscpy
condor_master
