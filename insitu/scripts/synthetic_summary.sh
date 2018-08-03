#!/bin/sh


if [ $# -ne 2 ]; then
    echo "Usage: $0 PATH STEPS"
    exit 1
fi
path=$1
steps=$2

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

pegasus-statistics -s all ${INST_WORK_HOME}/scripts/do7/pegasus/synthetic-test-workflow/run0001/ >/dev/null 2>&1
cp -r ${INST_WORK_HOME}/scripts/do7/pegasus/synthetic-test-workflow/run0001/ ${path}/simulation 


for (( i=1; i <= $steps; ++i ))
do 
	pegasus-statistics -s all ${INST_WORK_HOME}/analysis/workflows/do7/pegasus/spark-test-workflow/run000${i}/ >/dev/null 2>&1
	cp -r ${INST_WORK_HOME}/analysis/workflows/do7/pegasus/spark-test-workflow/run000${i}/ ${path}/analysis${i} 
done

echo "************************SUMMARY************************" 
echo "simulation"
cat ${path}/simulation/statistics/jobs.txt | grep synthetic_ID

for (( i=1; i <= $steps; ++i ))
do 
	echo "analysis"${i}
	cat ${path}/analysis${i}/statistics/jobs.txt | grep sprktest_ID
	cat ${path}/analysis${i}/statistics/jobs.txt | grep cleanup_ID
done

start=$(head -n 1 ${path}/simulation/synthetic-test-workflow-0.log | cut -d " " -f 4)
end=$(cat ${path}/analysis$((${i}-1))/spark-test-workflow-0.log | grep "005 (" | tail -1 | cut -d " " -f 4)
# end=$(cat ${path}/analysis3/spark-test-workflow-0.log | grep "005 (" | tail -1 | cut -d " " -f 4)
StartDate=$(date -u -d "$start" +"%s")
FinalDate=$(date -u -d "$end" +"%s")
echo $(( ${FinalDate} - ${StartDate} ))



${INST_WORK_HOME}/scripts/parse_log.py nvm
${INST_WORK_HOME}/scripts/parse_log.py hdfs 
${INST_WORK_HOME}/scripts/parse_log.py lustre