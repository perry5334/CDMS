#!/bin/bash
#SBATCH --job-name=HV100mm_readback
#SBATCH --output=/project/6049244/perry/samples/HV100mm_Ge71/output/%x-%j.log
#SBATCH --error=/project/6049244/perry/samples/HV100mm_Ge71/error/%x-%j.err
#SBATCH --account=rrg-mdiamond
#SBATCH --time=05:00:00
#SBATCH --mail-user=warren.perry@mail.utoronto.ca
#SBATCH --mail-type=ALL
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=25G

module load scdms/V05-03
singularity exec $SCDMS_IMAGE CDMS_G4DMC /project/6049244/perry/samples/HV100mm_Ge71/HV100mm_readback.mac
