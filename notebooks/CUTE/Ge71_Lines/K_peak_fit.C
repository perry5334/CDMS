#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "RooUniform.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include "RooFitResult.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TBranch.h>
#include <TCanvas.h>
using namespace RooFit ;


void K_peak_fit() {
    // Open the ROOT file
    TFile* file = TFile::Open("K_shell_OF.root");

    // Check if the file was opened successfully
    if (!file || file->IsZombie()) {
        std::cerr << "Error opening file!" << std::endl;
        return;
    }

    // Get the tree from the directory rqDir
    TTree* tree = (TTree*)file->Get("rqDir/zip1");

    // Check if the tree exists
    if (!tree) {
        std::cerr << "Error: Tree not found!" << std::endl;
        return;
    }

    // Create a branch object to store the data from the branch "PTOFamps"
    std::vector<float> PTOFamps;  // Store branch data in this vector
    TBranch* branch = tree->GetBranch("PTOFamps");

    // Set the branch address so we can read its data
    branch->SetAddress(&PTOFamps);

    // Create a histogram to fill with the data from PTOFamps
    TH1F* hist = new TH1F("PTOFamps_hist", "Histogram of PTOFamps", 40, 22, 30);

    // Loop over the tree entries and fill the histogram
    Long64_t nEntries = tree->GetEntries();
    for (Long64_t i = 0; i < nEntries; i++) {
        tree->GetEntry(i);  // Load the entry from the tree
        for (size_t j = 0; j < PTOFamps.size(); j++) {
            hist->Fill(PTOFamps[j]);
        }
    }

    // Draw the histogram
    //TCanvas* canvas = new TCanvas("canvas", "Canvas", 800, 600);
    //hist->Draw();

    // Save the histogram to a file (optional)
    //hist->SaveAs("K_shell_PTOFamps_hist.png");

    // Clean up
    file->Close();
}



//void K_shell_fit()
//{
   // S e t u p   c o m p o n e n t   p d f s 
   // ---------------------------------------
   // Declare observable x
   //RooRealVar x("x","x",22, 30) ;
   // Create two Gaussian PDFs g1(x,mean1,sigma1) and g2(x,mean2,sigma2) and their parameters
   //RooRealVar mean1("mean1","mean of gaussian 1", 26, 22, 30) ;
   //RooRealVar mean2("mean2","mean of gaussian 2", 27.5, 22, 30) ;
   //RooRealVar sigma1("sigma1","width of gaussian 1", 1, 0.1, 10) ;
   //RooRealVar sigma2("sigma2","width of gaussian 2", 0.5, 0.1, 10) ;
   //RooGaussian g1("g1","Gaussian 1",x,mean1,sigma1) ;  
   //RooGaussian g2("g2","Gaussian 2",x,mean2,sigma2) ;  
   // Build Uniform polynomial p.d.f.  
   //RooUniform flat("flat", "flat", x) ;
   // Sum the signal components into a composite signal p.d.f.
   //RooRealVar frac1("c1", "#c", 0.5, 0.0, 1.0) ;
   //RooRealVar frac2("c2", "#c", 0.2, 0.0, 1.0) ;
   //RooAddPdf pdf("model","model",RooArgList(g1, g2, flat),RooArgList(frac1, frac2)) ;
   // C o n s t r u c t   e x t e n d e d   c o m p s   wi t h   r a n g e   s p e c
   // ------------------------------------------------------------------------------
   // Define signal range in which events counts are to be defined
//}
