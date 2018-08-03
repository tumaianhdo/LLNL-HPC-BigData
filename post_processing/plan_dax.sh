#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1
DIR=$(cd $(dirname $0) && pwd)

export WF_DIR=$(cd $(dirname $0) && pwd)

cat > $WF_DIR/bin/ascent-execute-script.sh <<EOF
#!/bin/bash
# before launching the job set environment variable
source \${HOME}/my-job-env
source \${HOME}/set-env -hs
# lauch the job using srun
srun --jobid=\${MAGPIE_JOB_ID} -N \${HADOOP_SLAVE_COUNT} --exclude=\${HADOOP_MASTER_NODE} cloverleaf3d_par
EOF
chmod +x  $WF_DIR/bin/ascent-execute-script.sh


cat > $WF_DIR/bin/synthetic-execute-script.sh <<EOF
#!/bin/bash
# before launching the job set environment variable
source \${HOME}/my-job-env
source \${HOME}/set-env -hs
# lauch the job using srun
srun --jobid=\${MAGPIE_JOB_ID} -N \${HADOOP_SLAVE_COUNT} -n \${HADOOP_SLAVE_COUNT} -c 1 --exclude=\${HADOOP_MASTER_NODE} python "\$@"
EOF
chmod +x  $WF_DIR/bin/synthetic-execute-script.sh




# cat > $WF_DIR/bin/hdfs-copying-script.sh <<EOF
# #!/bin/bash
# # before launching the job set environment variable
# source \${HOME}/my-job-env
# source \${HOME}/set-env -h
# # lauch the job using srun
# srun --jobid=\${MAGPIE_JOB_ID} -N \${HADOOP_SLAVE_COUNT} -n \${HADOOP_SLAVE_COUNT} -c 4 --exclude=\${HADOOP_MASTER_NODE} hdfs_copy.sh
# EOF
# chmod +x  $WF_DIR/bin/hdfs-copying-script.sh


# cat > $DIR/bin/spark-execute-script.sh <<EOF
# #!/bin/bash
# source \${HOME}/my-job-env
# \${SPARK_HOME}/bin/spark-submit --master spark://\${SPARK_MASTER_NODE}:\${SPARK_MASTER_PORT} --deploy-mode client --driver-memory 1g --executor-memory 1g --executor-cores 4 --num-executors 2 "\$@"
# EOF
# chmod +x  $DIR/bin/spark-execute-script.sh

cat > $DIR/bin/spark-execute-script.sh <<EOF
#!/bin/bash
source \${HOME}/my-job-env
\${SPARK_HOME}/bin/spark-submit --master spark://\${SPARK_MASTER_NODE}:\${SPARK_MASTER_PORT} --deploy-mode client "\$@"
EOF
chmod +x  $DIR/bin/spark-execute-script.sh

cat > $DIR/bin/clean-up-script.sh <<EOF
#!/bin/bash
source \${HOME}/my-job-env
if [ "\$1" = "nvm" ]; then
	\${HADOOP_HOME}/bin/hdfs dfs -rm -f "/\$2"
	while read slave; do
		echo "Remote login to" \${slave}
		# Remove data from local NVM
		mrsh -n \${slave} "rm -f /l/ssd/\$2"
	done < \${HADOOP_CONF_DIR}/slaves
else
	rm -f /p/lscratchd/\${USER}/data/\$2
fi;
EOF
chmod +x  $DIR/bin/clean-up-script.sh


# This environment variable is used in all of the catalogs to
# determine the paths to transformations, files, and input/output dirs
#export PEGASUS_LLNL_WORK_HOME=$HOME/pegasus-llnl/
source $HOME/set-env -p



cat > $WF_DIR/pegasus.properties << EOF
# This tells Pegasus where to find the Site Catalog
pegasus.catalog.site.file=$WF_DIR/sites.xml

# This tells Pegasus where to find the Replica Catalog
pegasus.catalog.replica=File
pegasus.catalog.replica.file=$WF_DIR/rc.dat

# This tells Pegasus where to find the Transformation Catalog
pegasus.catalog.transformation=Text
pegasus.catalog.transformation.file=$WF_DIR/tc.txt

# This is the name of the application for analytics
pegasus.metrics.app=diamond-llnl	

pegasus.gridstart.arguments= -f
EOF



pegasus-plan \
    --conf $WF_DIR/pegasus.properties \
    --cleanup leaf \
    --dax $DAXFILE \
    --output-site catalyst \
    --sites catalyst \
    --submit
