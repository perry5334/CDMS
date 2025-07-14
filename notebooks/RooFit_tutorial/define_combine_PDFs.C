#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit;

void define_combine_PDFs()
{
   // S e t u p   m o d e l
   // ---------------------
  
   RooRealVar x("x", "x", -10, 10);
   RooRealVar E0("E0", "E0", 1, 0.1, 10);
   RooFormulaVar Gamma("Gamma", "-1.0/@0", RooArgList(E0)); // Define Gamma = -1 / E0
   RooRealVar mean("mean", "mean of gaussian", 1, -10, 10);
   RooRealVar sigma("sigma", "width of gaussian", 1, 0.1, 10);

   // Build gaussian pdf in terms of x,mean and sigma
   RooGaussian gauss("gauss", "gaussian PDF", x, mean, sigma);

   // Build exponential pdf in terms of x, Gamma
   RooExponential("exp", "exponential PDF", x, Gamma, negateCoefficient = false )

   // Construct plot frame in 'x'
   RooPlot *xframe = x.frame(Title("Gaussian + Exponential pdf."));

   
