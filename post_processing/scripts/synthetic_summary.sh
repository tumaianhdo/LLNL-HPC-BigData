#!/bin/sh


if [ $# -ne 2 ]; then
    echo "Usage: $0 PATH STEPS"
    exit 1
fi
path=$1
steps=$2

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

pegasus-statistics -s all ${POPR_WORK_HOME}/scripts/do7/pegasus/post-processing-workflow/run0001/ >/dev/null 2>&1
cp -r ${POPR_WORK_HOME}/scripts/do7/pegasus/post-processing-workflow/run0001/ ${path}/all 


echo "************************SUMMARY************************" 
echo "simulation"
cat ${path}/all/statistics/jobs.txt | grep synthetic_ID
cat ${path}/all/statistics/jobs.txt | grep sprktest_ID
cat ${path}/all/statistics/jobs.txt | grep cleanup_ID

start=$(head -n 1 ${path}/all/post-processing-workflow-0.log | cut -d " " -f 4)
end=$(cat ${path}/all/post-processing-workflow-0.log | grep "005 (" | tail -1 | cut -d " " -f 4)
# end=$(cat ${path}/analysis3/spark-test-workflow-0.log | grep "005 (" | tail -1 | cut -d " " -f 4)
StartDate=$(date -u -d "$start" +"%s")
FinalDate=$(date -u -d "$end" +"%s")
echo $(( ${FinalDate} - ${StartDate} ))


${POPR_WORK_HOME}/scripts/parse_log.py nvm
${POPR_WORK_HOME}/scripts/parse_log.py hdfs 
${POPR_WORK_HOME}/scripts/parse_log.py lustre