# hpc-bigdata
## Howto
### In-situ
1. Get into the main directory and export ${INST_WORK_HOME} evironmental variable
```
cd insitu
export INST_WORK_HOME=$(pwd)
```
2. Submit the Magpie script to deploy a cluster 
```
cd ${INST_WORK_HOME}/magpie
sbatch --ip-isolate=yes magpie.hdfs
```
It is able to adjust the number of cluster nodes by modifying the line #SBATCH --nodes={num_nodes} in the Magpie script, where num_nodes specify the number of nodes that you want to deploy for the cluster. 
3. Install dependency prequisites, such as Condor, Pegasus and export necessary environment varibles on master node of the cluster
```
cp -r software ${HOME}
mrsh {master_node}
cd ${INST_WORK_HOME}/magpie
./magpie-setup-script.sh 
source set-env -hscpy
```
Please make sure to sucessfully install the Condor and Pegasus by being running the following commands:
```
condor_q
condor_status
pegasus-status
```
4. Modify the simulation config file if there is a need.
You can find the Cloverleaf config file as the following path:
> ${INST_WORK_HOME}/simulation/input/clover.in
5. Modify the config files for your in-situ pipeline to setting the trigger configurations. There are two config files event-config.{nvm/lustre} corresponding to each data placement setup (on NVRAM or on Lustre) under the directory in-situ/config. The structure of the files under JSON format as follows:

event-config.nvm template
> {
> "event-dir":"/",
> "event-content":"data_test_*",
> "event-type":"hdfs-dir",
> "event-cycle":20,
> "event-size":0,
> "event-numfiles":2,
> "pegasus-args": "/g/g92/do7/ascent/insitu/analysis/plan_dax.sh",
> "event-script": "/g/g92/do7/ascent/insitu/analysis/dax_generator.sh",
> "event-dax-dir": "/g/g92/do7/ascent/insitu/analysis/workflows"
>}

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

6. Run the insitu pipeline
```
cd ${INST_WORK_HOME}/scripts
./in_situ.sh {data_placement}
```
Setting {data_placement} to 'nvm' if you want to run on NVRAM and 'lustre' if you want to run Lustre.

### Post-processing
1. Get into the main directory and export ${POPR_WORK_HOME} evironmental variable
```
cd post_processing
export POPR_WORK_HOME=$(pwd)
```
2. Repeat step 2 and 3 in In-situ section to deploy the cluster
3. Modify the simulation config file if there is a need.
You can find the Cloverleaf config file as the following path:
> ${POPR_WORK_HOME}/input/simulation/clover.in

3. Run the post-processing pipeline
```
cd ${POPR_WORK_HOME}/scripts
./post_processing.sh {data_placement}
```
Setting {data_placement} to 'nvm' if you want to run on NVRAM and 'lustre' if you want to run Lustre.
