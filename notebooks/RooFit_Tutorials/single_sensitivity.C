#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
using namespace std;
using namespace ROOT;
using namespace RooFit;
using namespace RooStats;


void single_sensitivity()
{
	// Define and combine PDFs

        // Declare variables x, mean, sigma, tau, with associated name, title,
        // initial value and allowed range
        RooRealVar x("E", "Energy", -50, 50); // measured energy
        RooRealVar mean("mu", "Mean of gaussian signal", 1, -50, 50); // DM mass
        RooRealVar sigma("sigma", "Std of gaussian signal", 0.2, 0.1, 10); // resolution
        RooRealVar tau("E0", "fall-time of background exp", 5, 2, 10); // background
        // Define lambda = -1 / tau using a RooFormulaVar
        RooFormulaVar lambda("lambda", "Decay constant", "-1.0 / @0", RooArgList(tau));

        // Build gaussian PDF in terms of x, mean, and sigma
        RooGaussian gauss("gauss", "gaussian PDF", x, mean, sigma);
        RooExponential exp("exp", "falling exponential PDF", x, lambda);

        // Define fraction of events that fall into signal.
        // If following tutorial, this is n_sig
        // n_bkg = 1 - n_sig
        RooRealVar n_s("n_s", "fraction of events in signal", 0.1, 0, 1);

        // Add two defined PDFs together
        RooAddPdf Model("Model", "Gauss + exp model", RooArgList(gauss, exp), RooArgList(n_s));

	// Begin sensitivity test
	// Set true values for model and generate data using Poisson sampling of true values
	// Calculate confidence interval upper limit for signal + background PDF

	cout<<"Starting single sensitivity"<<endl;
	RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR) ;
    	RooMsgService::instance().setSilentMode(kTRUE);

	double n_tot = 10000;
	double n_s_true = 0.1;
	double n_b_true = 1. - n_s_true;
	double n_s_events = n_tot*n_s_true;
	double n_b_events = n_tot*n_b_true;

	// set up histogram for scanning UL vs. mu
	int n_bins = 10;
	double m_array[n_bins];
	double sig_array[n_bins];
	int bin = 0;
	double progress;

	for(double mx = 5; mx<15; mx+=1){
		mean.setVal(mx);
		mean.setConstant();
		
		int n_samples = 1000;
		int sample = 0;
		double sig_array_temp[n_samples];

		for (double i=0; i<=1000; i+=1){

			//generate data with poisson sample of n_b
			RooRandom::randomGenerator()->SetSeed();
			int back_events = RooRandom::randomGenerator()->Poisson(n_b_events);

			std::unique_ptr<RooDataHist> d_b(exp.generateBinned(RooArgSet(x),NumEvents(back_events)));
			RooDataHist d_sb("sumData", "signal + bkg", x);
			d_sb.add(*d_b);

			// Do a PLC fit
			ProfileLikelihoodCalculator *PLC;
			PLC = new ProfileLikelihoodCalculator(d_sb, Model, RooArgSet(n_s));
			PLC->SetConfidenceLevel(0.9);
			LikelihoodInterval *LI = PLC->GetInterval(); 
			double ul = LI->UpperLimit(n_s);

			sig_array_temp[sample] = ul;
			sample +=1;

		}

		m_array[bin] = mx;
		double sum = 0.0;

		for (int j = 0; j < n_samples; j+=1) {
    			sum += sig_array_temp[j];
		}

		double average = sum / n_samples;
		sig_array[bin] = average;
		bin+=1;

		//counter
		int barWidth = 70;
		progress = double(bin)/double(n_bins);
		double pos = barWidth*progress;
		std::cout<<"Progress: [";
		for (int k = 0; k<= barWidth; ++k){
			if (k<pos) std::cout<<"=";
			else std::cout<<" ";
		}
		std::cout<<"] "<<int(progress * 100.0)<<" %\r";
		std::cout.flush();
	}
	std::cout<<std::endl;

	// Plot the exclusion curve
	gStyle->SetPalette(kSolar);
	TGraph* sense = new TGraph(n_bins, m_array, sig_array);
	TCanvas *c1 = new TCanvas("c1", "Sensitivity");
	//c1->SetLogy();
	//c1->SetLogx();
	c1->SetGrid();
	TH1F *senseframe = c1->DrawFrame(0, 0, 20, 0.5);
	senseframe->SetXTitle("DM mass");
	senseframe->SetYTitle("#sigma");

	sense->Draw("l");

}
