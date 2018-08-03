#!/bin/sh

# ger current directory
DIR=$(cd -P $(dirname $0);pwd)
echo ${DIR}

# create a directory in the NVM mounted point
# mkdir /l/ssd/data

# set environmental variables
source ${HOME}/my-job-env

echo ${SLURM_JOB_ID}
#echo ${SLURM_NODELIST}
echo ${HADOOP_MASTER_NODE}

# run the simulation and use Ascent to extract data insitu
# srun --jobid=${SLURM_JOB_ID} -N ${HADOOP_SLAVE_COUNT} -n ${HADOOP_SLAVE_COUNT} --exclude=${HADOOP_MASTER_NODE} ${DIR}/cloverleaf3d_par
srun -N ${HADOOP_SLAVE_COUNT} -n ${HADOOP_SLAVE_COUNT} --exclude=${HADOOP_MASTER_NODE} /usr/gapps/conduit/ascent/install/toss_3_x86_64_ib/examples/proxies/cloverleaf3d/cloverleaf3d_par

#NODES=($(scontrol show hostname $SLURM_NODELIST))
#nodelist=(${nodelist// / })
#
#
#updatedlist=""
#for i in ${!nodelist[@]}
#do
# if [ "${nodelist[i]}" != "$SPARK_MASTER_NODE" ]; then
#   NUMBER=$(echo ${nodelist[i]} | tr -dc '0-9')
#   updatedlist="$updatedlist$NUMBER,"
# fi
#done
#updatedlist="catalyst[$updatedlist"
#updatedlist=${updatedlist:0:-1}
#updatedlist="$updatedlist]"
#SLURM_NNODES=3
#SLURM_NNODES=$((SLURM_NNODES-1))
#export SLURM_NODELIST=$updatedlist
#export SLURM_NNODES=$((SLURM_NNODES))
#
#echo $SLURM_NODELIST
#echo $SLURM_NNODES

# sleep should be (time for sbatch job - (mapgie start + magpie shutdown time))
/bin/sleep 180000
