#!/usr/bin/env python
import sys
import os

# Import the Python DAX library
from Pegasus.DAX3 import *


# The name of the DAX file is the first argument
if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s DAXFILE\n" % (sys.argv[0]))
    sys.exit(1)
daxfile = sys.argv[1]


# Create a abstract dag
print "Creating ADAG..."
synthetic_tst_wf = ADAG("synthetic-test-workflow")
cur_dir = os.getcwd()
work_dir = os.environ['INST_WORK_HOME']

# Add input file to the DAX-level replica catalog
print "Adding input file paths..."
# actions_json = File("ascent_actions.json")
# actions_json.addPFN(PFN("file://" + work_dir + "/simulation/input/ascent_actions.json", "catalyst"))

# options_json = File("ascent_options.json")
# options_json.addPFN(PFN("file://" + work_dir + "/simulation/input/ascent_options.json", "catalyst"))

# clover_par = File("cloverleaf3d_par")
# clover_par.addPFN(PFN("file://" + work_dir + "/simulation/input/cloverleaf3d_par", "catalyst"))

# clover_in = File("clover.in")
# clover_in.addPFN(PFN("file://" + work_dir + "/simulation/input/clover.in", "catalyst"))

# extract_py = File("extract.py")
# extract_py.addPFN(PFN("file://" + work_dir + "/simulation/input/extract.py", "catalyst"))
generator_py = File("generator.py")
generator_py.addPFN(PFN("file://" + work_dir + "/synthetic/input/generator.py", "catalyst"))
generator_in = File("generator.in")
generator_in.addPFN(PFN("file://" + work_dir + "/synthetic/input/generator.in", "catalyst"))

# Add input files to workflow]
print "Adding input files to the workflow..."
# ascent_tst_wf.addFile(actions_json)
# ascent_tst_wf.addFile(options_json)
# ascent_tst_wf.addFile(clover_par)
# ascent_tst_wf.addFile(clover_in)
# ascent_tst_wf.addFile(extract_py)
synthetic_tst_wf.addFile(generator_in)
synthetic_tst_wf.addFile(generator_py)

# Add job
# print "Adding Ascent job..."
# ascent_tst_job = Job(namespace="pegasus", name="ascent_executable")
# ascent_tst_job.uses(actions_json, link=Link.INPUT)
# ascent_tst_job.uses(options_json, link=Link.INPUT)
# ascent_tst_job.uses(clover_par, link=Link.INPUT)
# ascent_tst_job.uses(clover_in, link=Link.INPUT)
# ascent_tst_job.uses(extract_py, link=Link.INPUT)

# Add synthetic job
print "Adding synthetic job..."
synthetic_tst_job = Job(namespace="pegasus", name="synthetic")
synthetic_tst_job.addArguments(generator_py, generator_in)
synthetic_tst_job.uses(generator_py, link=Link.INPUT)
synthetic_tst_job.uses(generator_in, link=Link.INPUT)

# Add profile to the job
print "Adding profile to job..."
synthetic_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
synthetic_tst_wf.addJob(synthetic_tst_job)


# Write the DAX to stdout
print "Writing %s" % daxfile
f = open(daxfile, "w")
synthetic_tst_wf.writeXML(f)
f.close()
