#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
using namespace RooFit;

void tutorial()
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

	// 2. Generating data and basic fits
	// ---------------------------------
	
	//Generate a dataset of 10000 events in x from gauss (n_sig = 2/3)
	RooDataSet *gaussdata = gauss.generate(x, 10000);
	//Generate a dataset of 5000 events in x from exp (n_bkg = 1/3)
	RooDataSet *expdata = exp.generate(x, 5000);

	//Change sigma to 1.15
	sigma.setVal(1.15);

	//Combine datasets
	RooDataSet *combined = new RooDataSet(*gaussdata); // copy of first dataset
	combined->append(*expdata); // append second dataset

	//plot data on frame
	RooPlot* xframe = x.frame();
	//combined->plotOn(xframe);

	//plot and fit to generated data
	//Model.plotOn(xframe);
	RooAbsReal* nll = Model.createNLL(*combined);
	RooMinimizer m(*nll);
	m.migrad();

	//plot data, fit result, and PDF components
	combined->plotOn(xframe, Name("Energy"));
	Model.plotOn(xframe, Name("Fit Result"));
	//Model.plotOn(xframe, Components("gauss"), LineStyle(kDashed), LineColor(kBlue), Name("Components"));
	//Model.plotOn(xframe, Components("exp"), LineStyle(kDashed), LineColor(kBlue));

	//show the chi^2 of the curve w.r.t. the histogram
	cout << "chi^2 = " << xframe->chiSquare() << endl;

	//add box with pdf parameters
	Model.paramOn(xframe, Layout(0.55, 0.99, 0.87));

	//construct histogram with residuals of the data w.r.t. the curve
	RooHist *hresid = xframe->residHist();

	//construct histogram with the pulls of the data w.r.t. the curve
	RooHist *hpull = xframe->pullHist();

	//create new frames for each distribution
	RooPlot *frame2 = x.frame(Title("Residual Distribution"));
	frame2->addPlotable(hresid, "P");

	RooPlot *frame3 = x.frame(Title("Pull Distribution"));
	frame3->addPlotable(hpull, "P");

	// create canvas and draw plot
	TCanvas* c = new TCanvas("c", "RooFit Plot", 900, 300);
	c->Divide(3);
	c->cd(1);
	gPad->SetLeftMargin(0.15);
	xframe->GetYaxis()->SetTitleOffset(1.6);
	xframe->Draw();
	c->cd(2);
	gPad->SetLeftMargin(0.15);
	frame2->GetYaxis()->SetTitleOffset(1.6);
	frame2->Draw();
	c->cd(3);
	gPad->SetLeftMargin(0.15);
	frame3->GetYaxis()->SetTitleOffset(1.6);
	frame3->Draw();
	c->SaveAs("rooplot.png");
}
