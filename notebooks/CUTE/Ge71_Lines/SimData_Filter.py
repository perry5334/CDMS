#!/usr/bin/env python

import numpy as np
import os, sys 
import getopt
import ROOT
from cats.cdataframe import CDataFrame
import glob

def main():

    #start, stop = getargs()
    index = getargs()
    #filter_snapshot(int(start), int(stop))
    filter_snapshot(int(index))

def getargs():
    """Return command line arguments to main function"""
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hz:c:l:')

    except getopt.GetoptError as err:
        sys.exit(2)

    # Process command line arguments
    #start, stop = args[0], args[1]
    index = args[0]
    
    return index #start, stop

def createFilter_EvtNum_DetNum():

	ROOT.gInterpreter.Declare("""
	#include <vector>
	#include <algorithm>

	bool eventDetFilter(const double colEventNum, const std::vector<double>& targetEventNums, const double colDetNum, const double DetNum) {
		bool eventMatch = std::find(targetEventNums.begin(), targetEventNums.end(), colEventNum) != targetEventNums.end();
		return eventMatch && (DetNum == colDetNum);
	}
	""")


def createFilter_EvtNum():

	ROOT.gInterpreter.Declare("""
	#include <vector>
	#include <algorithm>

	bool eventFilter(const double colEventNum, const std::vector<double>& targetEventNums) {
		bool eventMatch = std::find(targetEventNums.begin(), targetEventNums.end(), colEventNum) != targetEventNums.end();
		return eventMatch;
	}
	""")

def filter_snapshot(index):
    path = '/scratch/group/mitchcomp/CDMS/data/perry5334/SourceSimOutput_decayAncestor_Isotope/'
    branches = ['EventNum', 'PName', 'Parent', 'KE', 'Edep', 'Time1', 'Time3', 'X1', 'Y1', 'Z1', 'X3', 'Y3', 'Z3']
    DMCfiles = [np.sort(glob.glob(path + f'CUTE_Cf252_????????_??????.root'))[index]]

    det = 3
    #mczipFrame = CDataFrame("G4SimDir/mczip"+str(int(det)), DMCfiles)
    #mcDecaysFrame = CDataFrame("G4SimDir/mcDecays", DMCfiles)
    #mcFluxCounterFrame = CDataFrame("G4SimDir/mcFluxCounter", DMCfiles)

    # Save array of events where neutron capture and Ge71 activation occurred. Determined by recoil/decay of Ga71 nucleus.
    #GeActivEvents = np.unique(mczipFrame.Filter('string(PName.data()) == "Ga71"').AsNumpy(['EventNum'])['EventNum'])
    #targetEventNums = ROOT.std.vector("double")(GeActivEvents)
    #GeActivEventsStr = '{ ' + ', '.join([str(i) for i in GeActivEvents]) + ' }'

    createFilter_EvtNum_DetNum()
    createFilter_EvtNum()

    for file in range(len(DMCfiles)):
        print(file)
        frame = CDataFrame(f"G4SimDir/mcDecays"+str(int(det)), [DMCfiles[file]])
        frame_filtered = frame.Filter('DetNum=='+str(int(det))).Filter('string(decayAncestor.PName.data()) == "Ge71"')

        frame_filtered.Snapshot("mcDecays"+str(int(det)), path+"mcDecays"+str(int(det))+"/mcDecays"+str(int(det))+"_GeActivation_ancestorGe71_" + "%06d" % (index + file,) + ".root", branches)

if __name__ == '__main__':
    main()
