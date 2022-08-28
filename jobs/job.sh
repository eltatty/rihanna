#!/bin/bash
#
#SBATCH --job-name=test
#
#SBATCH --ntasks=6
#SBATCH --nodes=3

srun -w slurmnode1 -N 1 -n 2 sleep infinity &
srun -w slurmnode2 -N 1 -n 2 sleep infinity &
srun -w slurmnode3 -N 1 -n 2 sleep infinity &
wait