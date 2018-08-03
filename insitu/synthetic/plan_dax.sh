#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1
DIR=$(cd $(dirname $0) && pwd)

export WF_DIR=$(cd $(dirname $0) && pwd)

# cat > $WF_DIR/bin/ascent-execute-script.sh <<EOF
# #!/bin/bash

# # before launching the job set environment variable
# source \${HOME}/my-job-env
# source \${HOME}/set-env -hs

# # lauch the job using srun
# srun --jobid=\${MAGPIE_JOB_ID} -N \${HADOOP_SLAVE_COUNT} -n \${HADOOP_SLAVE_COUNT} -c 1 --exclude=\${HADOOP_MASTER_NODE} cloverleaf3d_par
# EOF
# chmod +x  $WF_DIR/bin/ascent-execute-script.sh


cat > $WF_DIR/bin/synthetic-execute-script.sh <<EOF
#!/bin/bash
# before launching the job set environment variable
source \${HOME}/my-job-env
source \${HOME}/set-env -hs
# lauch the job using srun
srun --jobid=\${MAGPIE_JOB_ID} -N \${HADOOP_SLAVE_COUNT} -n \${HADOOP_SLAVE_COUNT} -c 1 --exclude=\${HADOOP_MASTER_NODE} python "\$@"
EOF
chmod +x  $WF_DIR/bin/synthetic-execute-script.sh



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
    --sites catalyst
