#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1
DIR=$(cd $(dirname $0) && pwd)

cat > $DIR/bin/trigger-execute-script <<EOF
#!/bin/bash
DIR=$(cd $(dirname $0) && pwd)
echo ${DIR}
echo "Pegasus has triggered an event" >> ${DIR}/test.out
EOF
chmod +x  $DIR/bin/trigger-execute-script


# This environment variable is used in all of the catalogs to
# determine the paths to transformations, files, and input/output dirs
export WF_DIR=$(cd $(dirname $0) && pwd)
export CUR_DIR=$(pwd)

cat > $DIR/pegasus.properties << EOF
# This tells Pegasus where to find the Site Catalog
pegasus.catalog.site.file=$DIR/sites.xml

# This tells Pegasus where to find the Replica Catalog
pegasus.catalog.replica=File
pegasus.catalog.replica.file=$DIR/rc.dat

# This tells Pegasus where to find the Transformation Catalog
pegasus.catalog.transformation=Text
pegasus.catalog.transformation.file=$DIR/tc.txt

# This is the name of the application for analytics
pegasus.metrics.app=diamond-llnl

pegasus.gridstart.arguments= -f
EOF



pegasus-plan \
    --conf $DIR/pegasus.properties \
    --cleanup leaf \
    --dax $DAXFILE \
    --output-site catalyst \
    --sites catalyst
