#!/bin/bash


proc=processingDMC.SNOLAB.Default
config=DMCData.HV100mm_uni
i=51240805_000000
dump=$1
outpath=/project/6049244/perry/samples/HV100mm_Ge71/processed_10keV_0V/
rawpath=/project/6049244/perry/samples/HV100mm_Ge71/Raw_10keV_0V/combined_MIDAS_files/$i

export CDMSBATSDIR=cdmsbats_config
export BATNOISE_TEMPLATES=$CDMSBATSDIR/PulseTemplates
export BATROOT_PROC=$CDMSBATSDIR/UserSettings/BatRootSettings/processing
export BATROOT_CONST=$CDMSBATSDIR/UserSettings/BatRootSettings/analysis


export BATROOT_AUXFILES=$outpath/aux
export BATROOT_GPIBFILES=$outpath/gpib
export BATCALIB_RRQDATA=$outpath/rrq
export BATROOT_NOISEFILES=$outpath/noise
export BATROOT_RQDATA=$outpath/rq



export BATROOT_RAWDATA=$rawpath


echo "Proccesing file: "$proc
echo "Config file: "$config

echo "................Starting BatNoise................."

#BatNoise -s $i -d 0001-0035 --max_events 10000 --processing_config $proc --analysis_config $config

echo ".............Finished BatNoise, starting BatRoot................."


BatRoot -s $i -d $dump --max_events 10000 --processing_config $proc --analysis_config $config



echo ".............Finished BatRoot................."

echo ".............Goodbye!................."
