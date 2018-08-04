#!/bin/sh

if [ x${POPR_WORK_HOME} == x ]; then
    echo "Please set POPR_WORK_HOME"
    exit
fi

OPTIONS=hspyc
LONGOPTIONS=hadoop,spark,pegasus,python,condor
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
	exit 2
fi
eval set  -- "$PARSED"

hadoop=n
spark=n
pegasus=n
condor=n
python=n
while true; do
	case "$1" in
		-h|--hadoop)
			hadoop=y
			#export PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${PATH}
			shift
			;;
		-s|--spark)
			spark=y
			#export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}
			shift
			;;
		-p|--pegasus)
			pegasus=y
			#SOFT_DIR=${HOME}/software/install
			#export PATH=${SOFT_DIR}/pegasus$1/bin:${PATH}
			#export PYTHONPATH=${SOFT_DIR}/pegasus$1/lib64/python2.7/site-packages:${PYTHONPATH}
			#export MANPATH=${SOFT_DIR}/pegasus$1/share/man:${MANPATH}
			shift
			;;
		-c|--condor)
			#type="$2"
			#if [ $type = "manager" ]; then
			#	source ${HOME}/software/install/condor/condor.sh
			#else
			#	source /l/ssd/condor/condor.sh
			#fi
			#echo ${type}
			condor=y
			#source ${HOME}/software/install/condor$1/condor.sh
			shift
			;;
		-y|--python)
			python=y
			#export PYTHONPATH=${HOME}/.local/lib/python2.7/site-packages:${PYTHONPATH}
			#export PATH=${HOME}/.local/bin:${PATH}
			shift
			;;
		--)
			shift
			break
			;;
		*)
			echo "Error"
			exit 3
			;;
	esac
done

# if [[ $# -ne 1 ]]; then
# 	echo "$0: index is required"
# 	exit 4
# fi

source ${POPR_WORK_HOME}/magpie/my-job-env


if [ "$hadoop" = "y" ]; then
	export PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${PATH}
fi 

if [ "$spark" = "y" ]; then
	export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}
fi 

if [ "$condor" = "y" ]; then
	source ${POPR_WORK_HOME}/software/condor/condor.sh
fi 

if [ "$pegasus" = "y" ]; then
	export PATH=${POPR_WORK_HOME}/software/pegasus/bin:${PATH}
	export PYTHONPATH=${POPR_WORK_HOME}/software/pegasus/lib64/python2.7/site-packages:${PYTHONPATH}
	export MANPATH=${POPR_WORK_HOME}/software/pegasus/share/man:${MANPATH}
fi 

if [ "$python" = "y" ]; then
	export PYTHONPATH=${HOME}/.local/lib/python2.7/site-packages:${PYTHONPATH}
	export PATH=${HOME}/.local/bin:${PATH}
fi
