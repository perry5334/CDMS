#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit;

void single_bias_test()
{
	// 1. Defining and combining PDFs
        // ------------------------------

        // Declare variables x, mean, sigma, tau, with associated name, title,
        // initial value and allowed range
        RooRealVar x("E", "Energy", -10, 10);
        RooRealVar mean("mu", "Mean of gaussian signal", 1, -10, 10);
        RooRealVar sigma("sigma", "Std of gaussian signal", 1, 0.1, 10);
        RooRealVar tau("E0", "fall-time of background exp", 5, 2, 10);
        // Define lambda = -1 / tau using a RooFormulaVar
        RooFormulaVar lambda("lambda", "Decay constant", "-1.0 / @0", RooArgList(tau));

        // Build gaussian PDF in terms of x, mean, and sigma
        RooGaussian gauss("gauss", "gaussian PDF", x, mean, sigma);
        RooExponential exp("exp", "falling exponential PDF", x, lambda);

        // Define fraction of events that fall into signal.
        // If following tutorial, this is n_sig
        // n_bkg = 1 - n_sig
        RooRealVar frac("frac", "fraction of events in signal", 0.5, 0, 1);

        // Add two defined PDFs together
        RooAddPdf Model("Model", "Gauss + exp model", RooArgList(gauss, exp), frac);

	cout<<"Starting single bias test"<<endl;

	int samples=1000;
	double 

