#!/bin/bash
source ${HOME}/my-job-env
if [ "$1" = "nvm" ]; then
	${HADOOP_HOME}/bin/hdfs dfs -rm -f "/$2"
	while read slave; do
		echo "Remote login to" ${slave}
		# Remove data from local NVM
		mrsh -n ${slave} "rm -f /l/ssd/$2"
	done < ${HADOOP_CONF_DIR}/slaves
else
	rm -f /p/lscratchd/${USER}/data/$2
fi;
