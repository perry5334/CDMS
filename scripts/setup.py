# Contains frequently used functions
import matplotlib.pyplot as plt
import numpy as np
import os, sys 
import ROOT
from cats.cdataframe import CDataFrame

CDMS = os.environ["CDMS"] # set in .bash_profile

# Display the current color cycle with labels
def show_colors(stylesheet):
    with plt.rc_context({
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False
}):

        plt.style.use(stylesheet)
        plt.figure(figsize=(1,3), dpi=200)
        for i, hexcode in enumerate(plt.rcParams['axes.prop_cycle'].by_key()['color']):
            plt.plot([0, 1], [i,i], color = hexcode, lw = 5)
            plt.text(1.8, i, f'C{i}: {hexcode}', horizontalalignment='center', verticalalignment='center', fontsize=8)
            plt.xticks([])
            plt.yticks([])
            
# obtain and show the source macro given the root file path
def getMacro(DMCfile):
    f=ROOT.TFile.Open(DMCfile)
    macro=f.Get("G4SettingsInfoDir/SuperSim_Macro")
    macro.Print()
    
# obtain and show the software versions given the root file path
def getVersions(DMCfile):
    print(CDataFrame("G4SettingsInfoDir/Versions", [DMCfile]).AsNumpy())