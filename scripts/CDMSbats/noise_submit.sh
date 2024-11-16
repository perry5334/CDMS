#!/bin/bash
#SBATCH --job-name=HV100mm_launch
#SBATCH --output=/project/6049244/perry/samples/HV100mm_Ge71/output/%x-%j.log
#SBATCH --error=/project/6049244/perry/samples/HV100mm_Ge71/error/%x-%j.err
#SBATCH --account=rrg-mdiamond
#SBATCH --time=06:00:00
#SBATCH --mail-user=warren.perry@mail.utoronto.ca
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=10G

module load scdms/V05-02
singularity exec $SCDMS_IMAGE /project/6049244/perry/samples/HV100mm_Ge71/processed_10keV_0V/DMCprocessingTest_sh.sh
