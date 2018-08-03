#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1

export WF_DIR=$(cd $(dirname $0) && pwd)
cat > $WF_DIR/bin/mpi-hello-world-wrapper <<EOF
#!/bin/bash

# before launching the job switch to the directory that
# pegasus created for the workflow
# cd \$PEGASUS_SCRATCH_DIR
# unset TMP
# unset TMPDIR
# unset TEMP
$PWD/bin/pegasus-mpi-hw "\$@"
EOF
chmod +x  $WF_DIR/bin/mpi-hello-world-wrapper



# This environment variable is used in all of the catalogs to
# determine the paths to transformations, files, and input/output dirs
export PEGASUS_LLNL_WORK_HOME=$HOME/pegasus-llnl/
#source $HOME/pegasus-llnl/bin/setup.sh



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
