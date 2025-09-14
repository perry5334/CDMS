#!/bin/bash
#SBATCH --job-name=HV100mm_launch
#SBATCH --output=/scratch/user/perry5334/slurm/output/%x-%j.log
#SBATCH --error=/scratch/user/perry5334/slurm/error/%x-%j.err
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=100M



MAX_JOBS=20  # maximum number of concurrent jobs
JOB_NAME_PREFIX="sourcesim_processing"  # used to identify your jobs in squeue
USER="perry5334"
START=$1
END=$2

for i in $(seq $START $END); do
    while true; do
        # Count how many of your jobs are currently running or pending
        NUM_JOBS=$(squeue -u $USER -n $JOB_NAME_PREFIX -h | wc -l)

        if [ "$NUM_JOBS" -lt "$MAX_JOBS" ]; then
            # Submit the job and break out of the while loop
            sbatch --job-name=${JOB_NAME_PREFIX} /scratch/user/perry5334/CDMS/notebooks/CUTE/Ge71_Lines/submit.slrm $i
            echo "Submitted job $i"
            break
        else
            # Wait before checking again
            sleep 5
        fi
    done
done
