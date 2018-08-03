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
mpi_hw_wf = ADAG("mpi-hello-world")

# Add input file to the DAX-level replica catalog
fin = File("f.in")
fin.addPFN(PFN("file://" + os.getcwd() + "/input/f.in", "catalyst"))
mpi_hw_wf.addFile(fin)
        
# Add executables to the DAX-level transformation catalog
# For submitting MPI jobs directly through condor without GRAM
# we need to refer to wrapper that calls mpiexec with 
# the mpi executable
#e_mpi_hw = Executable(namespace="pegasus", name="mpihw", os="linux", arch="x86_64", installed=True)
#e_mpi_hw.addPFN(PFN("file://" + os.getcwd() + "/mpi-hello-world-wrapper", "catalyst"))
#mpi_hw_wf.addExecutable(e_mpi_hw)


# Add the mpi hello world job
print "Adding MPI hello world job..."
mpi_hw_job = Job(namespace="pegasus", name="mpihw" )
fout = File("f.out")


# Get environment variables 
job_id = os.environ['MAGPIE_JOB_ID']
master_node = os.environ['HADOOP_MASTER_NODE']
nworkers = os.environ['HADOOP_SLAVE_COUNT']
mpi_hw_job.addArguments("--jobid=" + job_id + " -n " + nworkers + " -N " + nworkers + " -c 1 --exclude=" + master_node + " " + os.getcwd() + "/bin/mpi-hello-world-wrapper -o", fout)
mpi_hw_job.uses(fin, link=Link.INPUT)
#mpi_hw_job.uses(fout, link=Link.OUTPUT)
mpi_hw_job.uses(fout, link=Link.OUTPUT, transfer=True, register=False)


# Add profile to the job
print "Adding profile..."
mpi_hw_job.addProfile( Profile("pegasus", "runtime", "80"))
mpi_hw_wf.addJob(mpi_hw_job)


# Write the DAX to stdout
#mpi_hw_wf.writeXML(sys.stdout)
print "Writing %s" % daxfile
f = open(daxfile, "w")
mpi_hw_wf.writeXML(f)
f.close()
