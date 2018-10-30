#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os

if len(sys.argv) != 2:
	print "Usage: %s PEGASUS_HOME" % (sys.argv[0])
	sys.exit(1)

# Create a abstract dag
diamond = ADAG("diamond")

# Add input file to the DAX-level replica catalog
a = File("f.a")
a.addPFN(PFN("file://" + os.getcwd() + "/f.a", "local"))
diamond.addFile(a)
	
# Add executables to the DAX-level replica catalog
# In this case the binary is keg, which is shipped with Pegasus, so we use
# the remote PEGASUS_HOME to build the path.
e_preprocess = Executable(namespace="diamond", name="preprocess", version="4.0", os="linux", arch="x86_64", installed=True)
e_preprocess.addPFN(PFN("file://" + sys.argv[1] + "/bin/pegasus-keg", "pbs-cluster"))
diamond.addExecutable(e_preprocess)
	
e_findrange = Executable(namespace="diamond", name="findrange", version="4.0", os="linux", arch="x86_64", installed=True)
e_findrange.addPFN(PFN("file://" + sys.argv[1] + "/bin/pegasus-keg", "pbs-cluster"))
diamond.addExecutable(e_findrange)
	
e_analyze = Executable(namespace="diamond", name="analyze", version="4.0", os="linux", arch="x86_64", installed=True)
e_analyze.addPFN(PFN("file://" + sys.argv[1] + "/bin/pegasus-keg", "pbs-cluster"))
diamond.addExecutable(e_analyze)

# Add a preprocess job
preprocess = Job(namespace="diamond", name="preprocess", version="4.0")
b1 = File("f.b1")
b2 = File("f.b2")
preprocess.addArguments("-a preprocess","-T60","-i",a,"-o",b1,b2)
preprocess.uses(a, link=Link.INPUT)
preprocess.uses(b1, link=Link.OUTPUT)
preprocess.uses(b2, link=Link.OUTPUT)

# add profiles indicating PBS specific parameters for pbs-cluster
# the globus key hostCount is NODES
preprocess.addProfile( Profile("globus", "hostcount", "4" ))
# the globus key xcount is PROCS or PPN
preprocess.addProfile( Profile("globus", "xcount", "2" ))    
#  the globus key maxwalltime is WALLTIME in minutes
preprocess.addProfile( Profile("globus", "maxwalltime", "120"))
diamond.addJob(preprocess)

# Add left Findrange job
frl = Job(namespace="diamond", name="findrange", version="4.0")
c1 = File("f.c1")
frl.addArguments("-a findrange","-T60","-i",b1,"-o",c1)
frl.uses(b1, link=Link.INPUT)
frl.uses(c1, link=Link.OUTPUT)
diamond.addJob(frl)

# Add right Findrange job
frr = Job(namespace="diamond", name="findrange", version="4.0")
c2 = File("f.c2")
frr.addArguments("-a findrange","-T60","-i",b2,"-o",c2)
frr.uses(b2, link=Link.INPUT)
frr.uses(c2, link=Link.OUTPUT)
diamond.addJob(frr)

# Add Analyze job
analyze = Job(namespace="diamond", name="analyze", version="4.0")
d = File("f.d")
analyze.addArguments("-a analyze","-T60","-i",c1,c2,"-o",d)
analyze.uses(c1, link=Link.INPUT)
analyze.uses(c2, link=Link.INPUT)
analyze.uses(d, link=Link.OUTPUT, register=True)
diamond.addJob(analyze)

# Add control-flow dependencies
diamond.addDependency(Dependency(parent=preprocess, child=frl))
diamond.addDependency(Dependency(parent=preprocess, child=frr))
diamond.addDependency(Dependency(parent=frl, child=analyze))
diamond.addDependency(Dependency(parent=frr, child=analyze))

# Write the DAX to stdout
diamond.writeXML(sys.stdout)



