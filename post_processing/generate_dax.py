#!/usr/bin/env python
import sys
import os

# Import the Python DAX library
from Pegasus.DAX3 import *


# The name of the DAX file is the first argument
if len(sys.argv) != 3:
    sys.stderr.write("Usage: %s DAXFILE DATA_PLACEMENT\n" % (sys.argv[0]))
    sys.exit(1)

# Get input arguments
daxfile = sys.argv[1]
data_placement=sys.argv[2]


# Create a abstract dag
print "Creating ADAG..."
post_process_wf = ADAG("post-processing-workflow")
cur_dir = os.getcwd()
work_dir = os.environ['POPR_WORK_HOME']

# Add input file to the DAX-level replica catalog
print "Adding input file paths..."
# Add input for the Simulation
print "Adding input files for the Simulation..."
actions_json = File("ascent_actions.json")
actions_json.addPFN(PFN("file://" + work_dir + "/input/simulation/ascent_actions.json", "catalyst"))
options_json = File("ascent_options.json")
options_json.addPFN(PFN("file://" + work_dir + "/input/simulation/ascent_options.json", "catalyst"))
clover_par = File("cloverleaf3d_par")
clover_par.addPFN(PFN("file://" + work_dir + "/input/simulation/cloverleaf3d_par", "catalyst"))
clover_in = File("clover.in")
clover_in.addPFN(PFN("file://" + work_dir + "/input/simulation/clover.in", "catalyst"))
extract_py = File("extract.py")
extract_py.addPFN(PFN("file://" + work_dir + "/input/simulation/extract.py", "catalyst"))
# generator_py = File("generator.py")
# generator_py.addPFN(PFN("file://" + work_dir + "/input/synthetic/generator.py", "catalyst"))
# generator_in = File("generator.in")
# generator_in.addPFN(PFN("file://" + work_dir + "/input/synthetic/generator.in", "catalyst"))

# Add input for the Analysis
print "Adding input files for the Analysis..."
# spark_jar = File("analysis.py")
# spark_jar.addPFN(PFN("file://" + work_dir + "/input/analysis/analysis.py", "catalyst"))
spark_jar = File("MLTest_rdd.py")
spark_jar.addPFN(PFN("file://" + work_dir + "/input/analysis/MLTest_rdd.py", "catalyst"))

# Add input files to workflow]
post_process_wf.addFile(actions_json)
post_process_wf.addFile(options_json)
post_process_wf.addFile(clover_par)
post_process_wf.addFile(clover_in)
post_process_wf.addFile(extract_py)
post_process_wf.addFile(spark_jar)
# post_process_wf.addFile(generator_in)
# post_process_wf.addFile(generator_py)


# Add Ascent job
print "Adding Ascent job..."
ascent_tst_job = Job(namespace="pegasus", name="ascent_executable")
ascent_tst_job.uses(actions_json, link=Link.INPUT)
ascent_tst_job.uses(options_json, link=Link.INPUT)
ascent_tst_job.uses(clover_par, link=Link.INPUT)
ascent_tst_job.uses(clover_in, link=Link.INPUT)
ascent_tst_job.uses(extract_py, link=Link.INPUT)

ascent_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
post_process_wf.addJob(ascent_tst_job)

# Add synthetic job
# print "Adding synthetic job..."
# synthetic_tst_job = Job(namespace="pegasus", name="synthetic")
# synthetic_tst_job.addArguments(generator_py, generator_in)
# synthetic_tst_job.uses(generator_py, link=Link.INPUT)
# synthetic_tst_job.uses(generator_in, link=Link.INPUT)


# synthetic_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
# post_process_wf.addJob(synthetic_tst_job)

name = "data_test_*"
if data_placement == "nvm":
	# Add input for the HDFS copying
	# print "Adding input files for the HDFS copying..."
	# hdfs_copy = File("hdfs_copy.sh")
	# hdfs_copy.addPFN(PFN("file://" + work_dir + "/input/hdfscopy/hdfs_copy.sh", 
	# 	 "catalyst"))
	# post_process_wf.addFile(hdfs_copy)

	# Add HDFS copying job
	# print "Adding HDFS copying job..."
	# hdfs_copy_job = Job(namespace="pegasus", name="hdfscopy")
	# hdfs_copy_job.uses(hdfs_copy, link=Link.INPUT)
	# post_process_wf.addJob(hdfs_copy_job)

	hdfs_path = "hdfs://"+ os.environ['HADOOP_NAMENODE']+ ":" + os.environ['HADOOP_NAMENODE_PORT'] + "/"
	file_name = hdfs_path + name

else:
	lustre_path = "file:///p/lscratchd/" + os.environ['USER'] +"/data/"
	file_name = lustre_path + name

# Add spark test job
print "Adding Spark job..."
spark_tst_job = Job(namespace="pegasus",name="sprktest")

spark_tst_job.addArguments(spark_jar, file_name)
spark_tst_job.uses(spark_jar, link=Link.INPUT)

spark_tst_job.addProfile(Profile("pegasus", "runtime", "120"))
post_process_wf.addJob(spark_tst_job)

# Add clean up job
print "Adding clean up job..."
clean_up_job = Job(namespace="pegasus",name="cleanup")
clean_up_job.addArguments(data_placement, name)
post_process_wf.addJob(clean_up_job)

# Add dependency between jobs
# if data_placement == "nvm":
# 	post_process_wf.addDependency(Dependency(parent=ascent_tst_job,child=hdfs_copy_job))
# 	post_process_wf.addDependency(Dependency(parent=hdfs_copy_job,child=spark_tst_job))
# 	post_process_wf.addDependency(Dependency(parent=spark_tst_job,child=clean_up_job))
# else:

post_process_wf.addDependency(Dependency(parent=ascent_tst_job,child=spark_tst_job))
# post_process_wf.addDependency(Dependency(parent=synthetic_tst_job,child=spark_tst_job))
post_process_wf.addDependency(Dependency(parent=spark_tst_job,child=clean_up_job))

# Write the DAX to stdout
print "Writing %s" % daxfile
f = open(daxfile, "w")
post_process_wf.writeXML(f)
f.close()
