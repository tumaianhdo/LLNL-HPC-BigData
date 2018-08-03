import sys, os, time, getopt

try:
    opts,args = getopt.getopt(sys.argv[1:], 't:r:n:q:s:e:p:')

except getopt.GetoptError:
    print 'model.py [-t <train-data>] [-r <test-data>] ' \
          '[-n <int: nodes>] [-q <string:pdebug/pbatch>] [-s <string:pythonScript> [-e <int: numTrees>]'\
	  '[-p <int: par>]'
    sys.exit(1)

TrainData="file:///p/lscratchd/briang/alkemi/data/learning/bigger/biggest.npy"
TestData="file:///p/lscratche/jiang4/spark/piston140density0.17/"
nodes=9
queue='pbatch'
pythonScript='MLTest_rdd.py'
numTrees = 100
par=16

for opt,arg in opts:
    if opt == '-t':
        TrainData = arg
    elif opt == '-r':
        TestData = arg
    elif opt == '-n':
        nodes = arg
    elif opt == '-q':
        queue = arg
    elif opt == '-s':
	pythonScript = arg
    elif opt == '-e':
	numTrees = arg
    elif opt == '-p':  #spark.default parallelism
	par = arg

command = 'msub -V -l walltime=24:00:00 -A workflow -l nodes=%s -q %s magpie.sbatch %s %s %s %s %s --slurm --ip-isolate=yes --clear-ssd' % (nodes, queue, TrainData, TestData, numTrees, pythonScript, par)  

#options = ' %s %s -l nodes=%s -q %s' % (node, queue, TrainData, TestData, pythonScript, numTrees, par)

print command  


os.system(command)


