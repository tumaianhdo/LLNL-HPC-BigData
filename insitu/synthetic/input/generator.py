import numpy as np
from mpi4py import MPI
import os
import sys
import json 
import time

# Require configuration file
if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s CONFIG_FILE\n" % (sys.argv[0]))
    sys.exit(1)

configfile = sys.argv[1]

# MPI initialization
comm = MPI.COMM_WORLD
# get number of processes
procs = comm.Get_size()
# get process id
rank = comm.Get_rank()

# load configuration file
with open(configfile) as config_file:
    config = json.load(config_file)

# get configuration parameters
steps = int(config["num_cycles"])
# exp=8;
# length = int(config["size"])/(procs*exp);
length = int(config["size"])/(procs);

# write data to global file system
log_name = "/p/lscratchd/do7/log/log_"+str(rank)
log_file = open(log_name, 'a')

for i in xrange(steps):
	user = os.environ['USER']
	step = (i+1)*int(config["frequency"])
	end = 0

	# for j in xrange(exp):
	# 	data = np.random.uniform(low=0.0, high=5.0, size=(length))

	# 	# save local data to Lustre
	
	# 	data_name = "/p/lscratchd/"+str(user)+"/data/data_test_"+str(rank)+"_"+str(j)+"_"+str(step)+".npy"

	# 	start = time.time()
	# 	data.tofile(data_name)
	# 	end += time.time() - start

	data = np.random.uniform(low=0.0, high=5.0, size=(length))

	# save local data to Lustre

	data_name = "/p/lscratchd/"+str(user)+"/data/data_test_"+str(rank)+"_"+str(step)+".npy"

	start = time.time()
	data.tofile(data_name)
	end += time.time() - start

	log_file.write("Step %s : \n" % str(step))
	log_file.write("lustre_write=%s\n" % str(end) ) 

log_file.close()
