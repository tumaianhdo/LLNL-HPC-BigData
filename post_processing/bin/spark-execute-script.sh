#!/bin/bash
source ${HOME}/my-job-env
${SPARK_HOME}/bin/spark-submit --master spark://${SPARK_MASTER_NODE}:${SPARK_MASTER_PORT} --deploy-mode client "$@"
