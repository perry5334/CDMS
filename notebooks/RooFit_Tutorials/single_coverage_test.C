#include "RooRealVar.h"
#include "RooDataSet.h"
//#include "RooGaussian.h"
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


void single_coverage_test()
{

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
        RooRealVar n_s("n_s", "fraction of events in signal", 0.5, 0, 1);
	//RooRealVar n_b("n_b", "fraction of events in background", 0.5, 0, 1);

        // Add two defined PDFs together
        RooAddPdf Model("Model", "Gauss + exp model", RooArgList(gauss, exp), RooArgList(n_s));

	cout<<"Starting single bias test"<<endl;
	RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR) ;
    	RooMsgService::instance().setSilentMode(kTRUE);


	int samples=1000;
	double n_tot = 1000;
	double n_s_true = 0.3;
	double n_b_true = 1. - n_s_true;
	double n_s_events = n_tot*n_s_true;
	double n_b_events = n_tot*n_b_true;
	double progress;

	TH1F* n_s_coverage = new TH1F("sig_coverage", "Coverage Test;UL;frequency",100,0,1);


	for(int i=0;i<samples;i++){
		RooRandom::randomGenerator()->SetSeed();
        	int back_events = RooRandom::randomGenerator()->Poisson(n_b_events);
        	int sig_events = RooRandom::randomGenerator()->Poisson(n_s_events);

		//generate data
		std::unique_ptr<RooDataHist> d_b(exp.generateBinned(RooArgSet(x),NumEvents(back_events)));
		std::unique_ptr<RooDataHist> d_s(gauss.generateBinned(RooArgSet(x),NumEvents(sig_events)));

		RooDataHist d_sb("sumData", "signal + bkg", x);
		d_sb.add(*d_s);
		d_sb.add(*d_b);

		// Do a PLC fit 
        	ProfileLikelihoodCalculator *PLC;
		PLC = new ProfileLikelihoodCalculator(d_sb,Model,RooArgSet(n_s)); // set up the profile likelihood. Our parameter of interest is the DM cross section
        
        	PLC->SetConfidenceLevel(0.8);
        	LikelihoodInterval *LI = PLC->GetInterval(); // get the likelihood interval object
        	double ul = LI->UpperLimit(n_s);


		//store UL values for n_s		
		n_s_coverage->Fill(ul);

		//counter
		int barWidth = 70;
		progress = (double(i)+1.)/(double(samples));
		double pos = barWidth*progress;
		std::cout<<"Progress: [";
		for (int i = 0; i<= barWidth; ++i){
			if (i<pos) std::cout<<"=";
			else std::cout<<" ";
		}
		std::cout<<"] "<<int(progress * 100.0)<<" %\r";
		std::cout.flush();
	}
	std::cout<<std::endl;

	TCanvas *c1 = new TCanvas("c1", "Coverage for nsig");
	TH1F *frame1 = c1->DrawFrame(0, 0, 1, 10);
	frame1->SetXTitle("n_s coverage");
	n_s_coverage->Draw();

}
