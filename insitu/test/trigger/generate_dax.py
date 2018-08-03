#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os
import json
import subprocess

# The name of the DAX file is the first argument
if len(sys.argv) != 4:
    sys.stderr.write("Usage: %s DAXFILE SPARK_CYCLE_NUMBER CONFIG_FILE\n" % (sys.argv[0]))
    sys.exit(1)
daxfile = sys.argv[1]
cycle_num = int(sys.argv[2])
configfile = sys.argv[3]

print(daxfile)
print(cycle_num)
print(configfile)


# Create a abstract dag
trigger_tst_wf = ADAG("trigger-test-workflow")
cur_dir = os.getcwd()

trigger_tst_job = Job(namespace="pegasus",name="triggertest")

trigger_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
trigger_tst_wf.addJob(trigger_tst_job)
        

# Write the DAX to stdout
f = open(daxfile, "w")
trigger_tst_wf.writeXML(f)
f.close()
