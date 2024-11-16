#!/bin/bash
##ENVIRONMENT SETTINGS; CHANGE WITH CAUTION
#SBATCH --export=NONE                #Do not propagate environment
#SBATCH --get-user-env=L             #Replicate login environment
##NECESSARY JOB SPECIFICATIONS
#SBATCH --time=00:10:00              #Set the wall clock limit
#SBATCH --mem=1GB                    #Request 8GB
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH -o /scratch/user/perry5334/slurm/output/%A_%a.out
#SBATCH -e /scratch/user/perry5334/slurm/error/%A_%a.err
##OPTIONAL JOB SPECIFICATIONS
[ -z $SLURM_ARRAY_TASK_ID ] && SLURM_ARRAY_TASK_ID=0

#MEMORY PER CORE ON TERRA:
#       64GB Node       128GB Node      96GB KNL Node           96GB KNL Node
#       2048 MB         4096 MB         1300 MB                 1236 MB
for i in $(seq 1 20);
do
    declare -i prev_step=$i-1
    declare -i start_evt=9000+50*$prev_step
    declare -i end_evt=9000+50*$i
    echo $start_evt
    echo $end_evt
    sbatch daqsim_submit.slrm $start_evt $end_evt
done
