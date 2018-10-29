# hpc-bigdata
## Howto
### In-situ
1. Submit the Magpie script to deploy a cluster 
```
cd insitu/magpie
sbatch --ip-isolate=yes magpie.hdfs
```
It is able to adjust the number of cluster nodes by modifying the line #SBATCH --nodes={num_nodes} in the Magpie script, where num_nodes specify the number of nodes that you want to deploy for the cluster. 
2. Install dependency prequisites, such as Condor, Pegasus and export necessary environment varibles on master node of the cluster
```
mrsh {master_node}
cd insitu/magpie
./magpie-setup-script.sh 
source set-env -hscpy
```
Please make sure to sucessfully install the Condor and Pegasus by being running the following commands:
```
condor_q
condor_status
pegasus-status
```
3. Modify the config files for your in-situ pipeline to setting the trigger configurations. There are two config files event-config.{nvm/lustre} corresponding to each data placement setup (on NVRAM or on Lustre) under the directory in-situ/config. The structure of the files under JSON format as follows:

event-config.nvm template
{
 "event-dir":"/",
 "event-content":"data_test_*",
 "event-type":"hdfs-dir",
 "event-cycle":20,
 "event-size":0,
 "event-numfiles":2,
 "pegasus-args": "/g/g92/do7/ascent/insitu/analysis/plan_dax.sh",
 "event-script": "/g/g92/do7/ascent/insitu/analysis/dax_generator.sh",
 "event-dax-dir": "/g/g92/do7/ascent/insitu/analysis/workflows"
}

event-config.lustre template
>{
> "event-dir":"/p/lscratchd/do7/data/",
> "event-content":"data_test_*",
> "event-type":"file-dir",
> "event-cycle":20,
> "event-size":0,
> "event-numfiles":2,
> "pegasus-args": "/g/g92/do7/ascent/insitu/analysis/plan_dax.sh",
> "event-script": "/g/g92/do7/ascent/insitu/analysis/dax_generator.sh",
> "event-dax-dir": "/g/g92/do7/ascent/insitu/analysis/workflows"
>}

The meaning of JSON fields:
- "event-dir": the directory that the pipeline listens to 
- "event-content": the name file patterns
- "event-type": hdfs-dir or file-dir
- "event-cycle": checking interval in a particular number of cycles
- "event-numfiles": the number of files satisfying the "event-content" file name pattern to trigger an event
- "pegasus-args": direct path to plan script of the analytics
- "event-script": direct path to DAX generator script of the analytics
- "event-dax-dir": direct path to the directory keeping intermediate Pegasus files of every events triggered

Please make sure to set your desired "event-cycle" and "event-numfiles" fields 
4. 

