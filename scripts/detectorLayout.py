#!/usr/bin/env python

def usage():
    print("""
                                                                                
Detector Geometry Validation
Contact:
Warren Perry - warren.perry@mail.utoronto.ca
Michael Kelsey - kelsey@slac.stanford.edu

*** Description ****

This tool was developed in order to validate the channel mapping of various SuperCDMS detectors and provide
an interactive utility for drawing the detector outline and channels with optional configurations. 
Given a root file at the command line, this package will read the description of the detector in 
G4SettingsInfoDir.Geometry and save an .eps and .png file of the detector outline and labeled phonon channels
in the working directory. This tool is currently designed to handle detector types 11, 21, 22, 700, 710, and 711.

**** Command Line Usage ****

Usage: ./detectorLayout.py [-h] [-z side] [-c chantype] [-l labels] ROOTfile image_name

Arguments: 
ROOTfile   -- name of ROOT file to be processed
image_name -- name of image file (image_name.png, image_name.eps)

Options: -h          -- display usage information
         -z side     -- side assignment of channels to be drawn (1: side 1, 2: side 2)
         -c chantype -- type of channel to be drawn (1: Phonon, 2: Charge)
         -l labels   -- enable channel labels on diagram (0: no labels, 1: labels)

**** Interactive Usage ****

The detector drawing utility can be used in an interactive Jupyter notebook.
Start by importing the script and dependencies.

import sys
import os, os.path
import matplotlib.pyplot as plt

supersim = os.environ["CDMS_SUPERSIM"]
sys.path.append(os.path.join(supersim,"CDMSscripts","validation"))
import detectorLayout

A simple sketch of a detector outline can be done with the following.
Note that the 'color', 'lw', and 'ls' arguments function the same
as with the matplotlib plotting utilities.

plt.figure(figsize=(4, 4), dpi=200)
detectorLayout.drawDetOutline(iZIP7_file, color='black', lw = 2, ls = '--')
detectorLayout.drawChanOutline(iZIP7_file, color='blue', side=1, chantype=1, labels=1, lw = 1.5, ls = '--')
detectorLayout.drawChanOutline(iZIP7_file, color='red', side=1, chantype=2, labels=1, lw = 1.5, ls = '--')
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')
plt.title('iZIP7 Side 1')

**** Dependencies ****
* numpy
* matplotlib
* ROOT

    """)
    
import sys
import numpy as np
from numpy import pi, arccos, cos, sin, tan, mean
import matplotlib.pyplot as plt
import getopt
import warnings
warnings.filterwarnings("ignore")

def main():
    """Create diagram images of detector layout using specifications from command line arguments"""

    file, image_name, side, chantype, labels = getargs()
    print("Processing {}...".format(file))

    plt.figure(figsize=(4, 4), dpi=200)
    drawDetOutline(file, color='black')
    drawChanOutline(file, color='black', side=int(side), chantype=int(chantype), labels=int(labels))
    plt.xlabel('X [mm]')
    plt.ylabel('Y [mm]')
    
    plt.tight_layout()
    plt.savefig("{}.eps".format(image_name), format='eps')
    plt.savefig("{}.png".format(image_name))
    
def getargs():
    """Return command line arguments to main function"""
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hz:c:l:')

    except getopt.GetoptError as err:
        sys.exit(2)

    # Process command line arguments
    file, image_name, side, chantype, labels = args[0], args[1], 1, 1, 1
    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit(0)
        elif o == "-z":
            side = a
        elif o == "-c":
            chantype = a
        elif o == "-l":
            labels = a
        else:
            assert False, "unhandled option "+o

    
    return file, image_name, side, chantype, labels

def drawDetOutline(file, color='black', lw = 1, ls = '-'):
    """Draw detector outline including X and Y flats with specified color"""
    
    import ROOT # imported later so that ROOT does not display its own usage function

    f = ROOT.TFile(file)
    myTree = f.Get("G4SettingsInfoDir/Geometry")
    for entry in myTree:         
        R = entry.Radius * 1e3
        Xflat, Yflat = entry.Axis1Len * 1e3 / 2, entry.Axis2Len * 1e3 / 2

    # Angle swept by half of Y flat and X flat
    Ytheta, Xtheta = arccos(Yflat / R), arccos(Xflat / R)

    # Half of width of Y flat and X flat
    Ywidth, Xwidth = R*cos(pi / 2 - Ytheta), R*sin(Xtheta)
    
    # Draw Y flats
    plt.plot([-Ywidth, Ywidth], [Yflat, Yflat], lw = lw, ls = ls, color = color)
    plt.plot([-Ywidth, Ywidth], [-Yflat, -Yflat], lw = lw, ls = ls, color = color)
    # Draw X flats
    plt.plot([Xflat, Xflat], [-Xwidth, Xwidth], lw = lw, ls = ls, color = color)
    plt.plot([-Xflat, -Xflat], [-Xwidth, Xwidth], lw = lw, ls = ls, color = color)

    # Draw circular edge between flats
    plt.plot(R * cos(np.linspace(Xtheta, pi / 2 - Ytheta, 1000, endpoint=True)), 
             R * sin(np.linspace(Xtheta, pi / 2 - Ytheta, 1000, endpoint=True)), 
             lw = lw, ls = ls, color = color)
    plt.plot(R * cos(np.linspace(pi / 2 + Ytheta, pi - Xtheta, 1000, endpoint=True)), 
             R * sin(np.linspace(pi / 2 + Ytheta, pi - Xtheta, 1000, endpoint=True)), 
             lw = lw, ls = ls, color = color)
    plt.plot(R * cos(np.linspace(pi + Xtheta, 3 * pi / 2 - Ytheta, 1000, endpoint=True)), 
             R * sin(np.linspace(pi + Xtheta, 3 * pi / 2 - Ytheta, 1000, endpoint=True)), 
             lw = lw, ls = ls, color = color)
    plt.plot(R * cos(np.linspace(3 * pi / 2 + Ytheta, 2 * pi - Xtheta, 1000, endpoint=True)), 
             R * sin(np.linspace(3 * pi / 2 + Ytheta, 2 * pi - Xtheta, 1000, endpoint=True)), 
             lw = lw, ls = ls, color = color)
             
def drawChanOutline(file, side=1, chantype=1, labels=1, color='black', lw = 1, ls = '-'):
    """Draw outline for specified side and channel type with options for setting color and enabling channel labels"""

    import ROOT # imported later so that ROOT does not display its own usage function

    f = ROOT.TFile(file)
    myTree = f.Get("G4SettingsInfoDir/Geometry")
    for entry in myTree:         
        ChanName = list(entry.ChanName)
        ChanSide = np.array(entry.ChanSide)
        nChan = entry.Channels
        
    # Define ChanType using ChanName
    # This approach can't deal with edge cases with other detectors
    # Should be updated after elog/1934 is on supersim main branch
    ChanType = np.array([2 if i[0] == 'Q' else 1 for i in ChanName])

    side_cut = {1: ChanSide > 0, 2: ChanSide < 0}
    type_cut = {1: ChanType == 1, 2: ChanType == 2}

    for ch in np.arange(0, nChan, 1)[side_cut[side] & type_cut[chantype]]:

        for entry in myTree:       
            # Radius, Radius of Y flat, Radius of X flat
            # Meters are converted to mm.
            minR, minXflat, minYflat = np.array(entry.ChanRMin)[ch]*1e3, np.array(entry.ChanxRMin)[ch]*1e3, np.array(entry.ChanyRMin)[ch]*1e3
            maxR, maxXflat, maxYflat = np.array(entry.ChanRMax)[ch]*1e3, np.array(entry.ChanxRMax)[ch]*1e3, np.array(entry.ChanyRMax)[ch]*1e3
            # Angular boundaries of channels
            # Degrees are converted to radians.
            minPhi, maxPhi = np.array(entry.ChanPhiMin)[ch] * pi / 180, np.array(entry.ChanPhiMax)[ch] * pi / 180

        # X and Y flat values are set to channel radius if there is no flat present.
        minYflat += minR * (minYflat == 0)
        minXflat += minR * (minXflat == 0)
        maxYflat += maxR * (maxYflat == 0)
        maxXflat += maxR * (maxXflat == 0)

        # Add 2pi to values which are below zero
        # Ensure maximum phi is larger than minimum phi
        minPhi += (2 * pi) * (minPhi < 0)
        maxPhi += (2 * pi) * (maxPhi < 0)
        maxPhi += (2 * pi) * (minPhi > maxPhi)

        # Angle swept by half of channel flats
        minYtheta, minXtheta = arccos(minYflat / minR), arccos(minXflat / minR)
        maxYtheta, maxXtheta = arccos(maxYflat / maxR), arccos(maxXflat / maxR)

        # Half of width of Y flat and X flat
        minYwidth, minXwidth = minR*cos(pi / 2 - minYtheta), minR*sin(minXtheta)
        maxYwidth, maxXwidth = maxR*cos(pi / 2 - maxYtheta), maxR*sin(maxXtheta)
    
        # Draw Y flats
        plt.plot([-maxYwidth, maxYwidth], [maxYflat, maxYflat], lw = lw, ls = ls, color = color)
        plt.plot([-maxYwidth, maxYwidth], [-maxYflat, -maxYflat], lw = lw, ls = ls, color = color)
        plt.plot([-minYwidth, minYwidth], [minYflat, minYflat], lw = lw, ls = ls, color = color)
        plt.plot([-minYwidth, minYwidth], [-minYflat, -minYflat], lw = lw, ls = ls, color = color)
        # Draw X flats
        plt.plot([maxXflat, maxXflat],    [-maxXwidth, maxXwidth], lw = lw, ls = ls, color = color)
        plt.plot([-maxXflat, -maxXflat],  [-maxXwidth, maxXwidth], lw = lw, ls = ls, color = color)
        plt.plot([minXflat, minXflat],    [-minXwidth, minXwidth], lw = lw, ls = ls, color = color)
        plt.plot([-minXflat, -minXflat],  [-minXwidth, minXwidth], lw = lw, ls = ls, color = color)


        # Draw circular edge between flats
        # Minimum channel boundary
        plt.plot(minR * cos(np.linspace(minXtheta, pi / 2 - minYtheta, 1000, endpoint=True)), 
                 minR * sin(np.linspace(minXtheta, pi / 2 - minYtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(minR * cos(np.linspace(pi / 2 + minYtheta, pi - minXtheta, 1000, endpoint=True)), 
                 minR * sin(np.linspace(pi / 2 + minYtheta, pi - minXtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(minR * cos(np.linspace(pi + minXtheta, 3 * pi / 2 - minYtheta, 1000, endpoint=True)), 
                 minR * sin(np.linspace(pi + minXtheta, 3 * pi / 2 - minYtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(minR * cos(np.linspace(3 * pi / 2 + minYtheta, 2 * pi - minXtheta, 1000, endpoint=True)), 
                 minR * sin(np.linspace(3 * pi / 2 + minYtheta, 2 * pi - minXtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        # Maximum channel boundary
        plt.plot(maxR * cos(np.linspace(maxXtheta, pi / 2 - maxYtheta, 1000, endpoint=True)), 
                 maxR * sin(np.linspace(maxXtheta, pi / 2 - maxYtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(maxR * cos(np.linspace(pi / 2 + maxYtheta, pi - maxXtheta, 1000, endpoint=True)), 
                 maxR * sin(np.linspace(pi / 2 + maxYtheta, pi - maxXtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(maxR * cos(np.linspace(pi + maxXtheta, 3 * pi / 2 - maxYtheta, 1000, endpoint=True)), 
                 maxR * sin(np.linspace(pi + maxXtheta, 3 * pi / 2 - maxYtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)
        plt.plot(maxR * cos(np.linspace(3 * pi / 2 + maxYtheta, 2 * pi - maxXtheta, 1000, endpoint=True)), 
                 maxR * sin(np.linspace(3 * pi / 2 + maxYtheta, 2 * pi - maxXtheta, 1000, endpoint=True)), 
                 lw = lw, ls = ls, color = color)

        if (minPhi == maxPhi):
            pass
        else:
            # Set radius of adjacent border according to if it 'hits' an X flat or Y flat
            minHitY, minHitX = abs(cos(minPhi)) < 0.01, abs(sin(minPhi)) < 0.01
            maxHitY, maxHitX = abs(cos(maxPhi)) < 0.01, abs(sin(maxPhi)) < 0.01
            plt.plot([( minR * (~minHitY & ~minHitX) + minYflat * minHitY + minXflat * minHitX ) * cos(minPhi),
                      ( maxR * (~minHitY & ~minHitX) + maxYflat * minHitY + maxXflat * minHitX ) * cos(minPhi)], 
                     [( minR * (~minHitY & ~minHitX) + minYflat * minHitY + minXflat * minHitX ) * sin(minPhi),
                      ( maxR * (~minHitY & ~minHitX) + maxYflat * minHitY + maxXflat * minHitX ) * sin(minPhi)], 
                     lw = lw, ls = ls, color = color)

            plt.plot([( minR * (~maxHitY & ~maxHitX) + minYflat * maxHitY + minXflat * maxHitX ) * cos(maxPhi),
                      ( maxR * (~maxHitY & ~maxHitX) + maxYflat * maxHitY + maxXflat * maxHitX ) * cos(maxPhi)], 
                     [( minR * (~maxHitY & ~maxHitX) + minYflat * maxHitY + minXflat * maxHitX ) * sin(maxPhi),
                      ( maxR * (~maxHitY & ~maxHitX) + maxYflat * maxHitY + maxXflat * maxHitX ) * sin(maxPhi)], 
                     lw = lw, ls = ls, color = color)


        if labels:
            if (minPhi == maxPhi):
                if minR == 0:
                    plt.text(-5 * (ChanType[ch] == 1) + 5  * (ChanType[ch] == 2), 0, ChanName[ch], 
                             ha='center', va='center', fontsize = 8)
                else:
                    plt.text(-5 * (ChanType[ch] == 1) + 5  * (ChanType[ch] == 2), np.mean([minYflat, maxYflat]), 
                             ChanName[ch], ha='center', va='center', fontsize = 6.5)

            else:
                PhiMean, RMean = mean([minPhi, maxPhi]), mean([minR, maxR])
                plt.text(RMean * cos(PhiMean), RMean * sin(PhiMean), ChanName[ch], ha='center', va='center', fontsize = 8)
                
def drawAll(file, det_color='black', channel_color='black', side=1, chantype=1, labels=1, det_lw = 1, chan_lw = 1, det_ls = '-', chan_ls = '-'):
    """Draw detector and channel outlines with options for colors, side, channel types, and labels"""
    
    drawDetOutline(file, color=det_color, lw = det_lw, ls = det_ls)
    drawChanOutline(file, color=channel_color, side=side, chantype=chantype, labels=labels, lw = chan_lw, ls = chan_ls)
        
if __name__ == '__main__':
    main()
