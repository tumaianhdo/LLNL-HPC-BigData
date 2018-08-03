#!/bin/sh

DIR=$(cd -P $(dirname $0);pwd)
echo ${DIR}

echo ${SLURM_JOB_ID}
echo ${SLURM_NODELIST}
echo ${HADOOP_MASTER_NODE}

NODES=($(scontrol show hostname $SLURM_NODELIST))

srun --jobid=${SLURM_JOB_ID} -N $((SLURM_NNODES-1)) -n 8 --exclude=${NODES[0]} ${DIR}/cloverleaf3d_par

source ${HOME}/my-job-env
