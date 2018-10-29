import numpy as np
# from mpi4py import MPI
import os 
import subprocess

# obtain a mpi4py mpi comm object
# comm = MPI.Comm.f2py(ascent_mpi_comm_id())

# get this MPI task's published blueprint data
mesh_data = ascent_data()

# fetch the numpy array for the energy field values
e_vals = mesh_data["fields/energy/values"]
d_vals = mesh_data["fields/density/values"]
p_vals = mesh_data["fields/pressure/values"]     

# concate arrays of field values to row-majored arrays
data = np.column_stack((e_vals, d_vals, p_vals))

# duplicate data
# data = np.concatenate((data, data, data, data, data), axis=1)
# data = np.concatenate((data, data, data, data), axis=1)
# data = np.concatenate((data, data, data, data, data), axis=1)
# data = np.concatenate((data, data), axis=1)


# get the current cycle
cycle = mesh_data["state/cycle"]

# get process id
rank = mesh_data["state/domain_id"]

# save local data to local NVM
data_name = "/l/ssd/data_test_"+str(rank)+"_"+str(cycle)+".npy"
# np.save(data_name , e_vals)
data.tofile(data_name)

# copy local data to HDFS 
hadoop_home = os.environ['HADOOP_HOME']
os.system(str(hadoop_home) + "/bin/hdfs dfs -put " + data_name + " /")


# Improvement: copying to HDFS in background
# os.system(str(hadoop_home) + "/bin/hdfs dfs -put " + data_name + ".npy / &")
# subprocess.Popen([str(hadoop_home) + "/bin/hdfs", "dfs", "-put", data_name + ".npy", "/"], close_fds=True)
# if cycle == 100:
	# os.system("wait < <(jobs -p)")

# synchronize 
# comm.Barrier()



#e_vals.dump("/l/ssd/data.dat")

# find the data extents of the energy field using mpi

# first get local extents
#e_min, e_max = e_vals.min(), e_vals.max()

# declare vars for reduce results
#e_min_all = np.zeros(1)
#e_max_all = np.zeros(1)

# reduce to get global extents
#comm.Allreduce(e_min, e_min_all, op=MPI.MIN)
#comm.Allreduce(e_max, e_max_all, op=MPI.MAX)

# compute bins on global extents 
#bins = np.linspace(e_min_all, e_max_all)

# get histogram counts for local data
#hist, bin_edges = np.histogram(e_vals, bins = bins)

# declare var for reduce results
#hist_all = np.zeros_like(hist)

# sum histogram counts with MPI to get final histogram
#comm.Allreduce(hist, hist_all, op=MPI.SUM)

# print result on mpi task 0
#if comm.Get_rank() == 0:
#    print("\nEnergy extents: {} {}\n".format(e_min_all[0], e_max_all[0]))
#    print("Histogram of Energy:\n")
#    print("Counts:")
#    print(hist_all)
#    print("\nBin Edges:")
#    print(bin_edges)
#    print("")
