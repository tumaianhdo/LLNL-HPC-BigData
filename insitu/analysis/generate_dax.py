#!/usr/bin/env python
import sys
import os
import json

# Import the Python DAX library
from Pegasus.DAX3 import *


# The name of the DAX file is the first argument
if len(sys.argv) != 4:
    sys.stderr.write("Usage: %s DAXFILE SPARK_CYCLE_NUMBER CONFIG_FILE\n" % (sys.argv[0]))
    sys.exit(1)

# Get input arguments
daxfile = sys.argv[1]
cycle_num = int(sys.argv[2])
configfile = sys.argv[3]

# Load event configuration file
data = None
with open(configfile) as data_file:
    data = json.load(data_file)

# Get file name to handle in current cycle
name = data["event-dir"] + data["event-content"] + "_" + str(cycle_num * data["event-cycle"]) + ".npy"
if data["event-type"]=="hdfs-dir":
	data_placement="nvm"
	hdfs_path = "hdfs://"+ os.environ['HADOOP_NAMENODE']+ ":" + os.environ['HADOOP_NAMENODE_PORT'] 
	file_name = hdfs_path + name

elif data["event-type"]=="file-dir":
	data_placement="lustre"
	lustre_path = "file://"
	file_name = lustre_path + name

print name
print file_name

# Create a abstract dag
print "Creating ADAG..."
spark_tst_wf = ADAG("spark-test-workflow")
cur_dir = os.getcwd()
work_dir = os.environ['INST_WORK_HOME']
# spark_jar = File("analysis.py")
# spark_jar.addPFN(PFN("file://" + work_dir + "/analysis/input/analysis.py", "catalyst"))
spark_jar = File("MLTest_rdd.py")
spark_jar.addPFN(PFN("file://" + work_dir + "/analysis/input/MLTest_rdd.py", "catalyst"))
spark_tst_wf.addFile(spark_jar)
        
# Add spark test job
print "Adding Spark job..."
spark_tst_job = Job(namespace="pegasus",name="sprktest")
spark_tst_job.addArguments(spark_jar, file_name)
spark_tst_job.uses(spark_jar, link=Link.INPUT)

spark_tst_job.addProfile(Profile("pegasus", "runtime", "120"))
spark_tst_wf.addJob(spark_tst_job)

# Add clean up job
print "Adding clean up job..."
clean_up_job = Job(namespace="pegasus",name="cleanup")
clean_up_job.addArguments(data_placement, name)
spark_tst_wf.addJob(clean_up_job)

# Add dependency between jobs
spark_tst_wf.addDependency(Dependency(parent=spark_tst_job,child=clean_up_job))

# Write the DAX to stdout
print "Writing %s" % daxfile
f = open(daxfile, "w")
spark_tst_wf.writeXML(f)
f.close()
