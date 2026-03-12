import numpy as np
import ROOT

class ROOplot:
    def __init__(self, _width=700, _height=600, _leftMargin=0.15, _rightMargin=0.15, _topMargin=0.07, _bottomMargin=0.2, _title="", _xlabel="", _ylabel="", _labelsize=0.05, _titlesize=0.05,
                 _xlim=False, _xlow=None, _xhigh=None, _ylim=False, _ylow=None, _yhigh=None, _logx=False, _logy=False):

        self.title=_title
        self.xlabel=_xlabel
        self.ylabel=_ylabel
        self.labelsize=_labelsize
        self.titlesize=_titlesize
        self.xlim=_xlim
        self.ylim=_ylim
        self.xlow=_xlow
        self.xhigh=_xhigh
        self.ylow=_ylow
        self.yhigh=_yhigh

        self.c = ROOT.TCanvas("c", "Canvas", _width, _height)
        self.c.SetLeftMargin(_leftMargin)
        self.c.SetBottomMargin(_bottomMargin)
        self.c.SetRightMargin(_rightMargin)
        self.c.SetTopMargin(_topMargin)

        if _logx:
            self.c.SetLogx()
        if _logy:
            self.c.SetLogy()
        self.graphs = []

    def createScatter(self, x, y, style=21, width=0, size=0.2, color=ROOT.kBlue, label=None, alpha=1):
        
        g = ROOT.TGraph(len(x), x, y)
        g.SetTitle(self.title + ";" + self.xlabel + ";" + self.ylabel)
        g.SetMarkerStyle(style)
        g.SetMarkerSize(size)
        g.SetLineWidth(width)
        g.SetLineColor(color)
        g.SetMarkerColor(color)
        g.SetFillColor(color)
        g.GetXaxis().SetLabelSize(self.labelsize)
        g.GetYaxis().SetLabelSize(self.labelsize)
        g.GetXaxis().SetTitleSize(self.titlesize)
        g.GetYaxis().SetTitleSize(self.titlesize)

        if self.xlim:
            g.GetXaxis().SetLimits(self.xlow, self.xhigh)
        if self.ylim:
            g.SetMinimum(self.ylow)
            g.SetMaximum(self.yhigh)

        self.graphs.append((g, label))

    def createHist(self, data, bins_start, bins_end, nbins, width=3, color=ROOT.kBlue, fillstyle=0, scale=False, label=None):
        
        h = ROOT.TH1F("h", " ", nbins, bins_start, bins_end)
        h.SetTitle(self.title + ";" + self.xlabel + ";" + self.ylabel)
        for value in data: h.Fill(value)
        h.SetLineWidth(width)
        h.SetLineColor(color)
        h.SetFillColor(color)
        h.SetFillStyle(fillstyle)
        h.GetXaxis().SetLabelSize(self.labelsize)
        h.GetYaxis().SetLabelSize(self.labelsize)
        h.GetXaxis().SetTitleSize(self.titlesize)
        h.GetYaxis().SetTitleSize(self.titlesize)

        if scale:
            h.Scale(1.0 / scale)

        if self.xlim:
            h.GetXaxis().SetLimits(self.xlow, self.xhigh)
        if self.ylim:
            h.SetMinimum(self.ylow)
            h.SetMaximum(self.yhigh)

        self.graphs.append((h, label))

    def createEff(self, data, passed, bins_start, bins_end, nbins, width=3, color=ROOT.kBlue, label=None):
        
        eff = ROOT.TEfficiency("eff", " ", nbins, bins_start, bins_end)
        for p, d in zip(passed, data, strict=True): eff.Fill(p, d)

        h = eff.CreateGraph()
        h.SetTitle(self.title + ";" + self.xlabel + ";" + self.ylabel)
        h.SetLineWidth(width)
        h.SetLineColor(color)
        h.GetXaxis().SetLabelSize(self.labelsize)
        h.GetYaxis().SetLabelSize(self.labelsize)
        h.GetXaxis().SetTitleSize(self.titlesize)
        h.GetYaxis().SetTitleSize(self.titlesize)

        if self.xlim:
            h.GetXaxis().SetLimits(self.xlow, self.xhigh)
        if self.ylim:
            h.SetMinimum(self.ylow)
            h.SetMaximum(self.yhigh)

        self.graphs.append((h, label))

    def draw(self, firststyle="", style="", grid=False):
        """Draw all graphs on the same canvas with a legend."""
        if not self.graphs:
            print("No graphs to draw.")
            return

        first_graph, first_label = self.graphs[0]
        first_graph.Draw(firststyle)  # 'A' = axes, 'P' = points

        for graph, label in self.graphs[1:]:
            graph.Draw(style + "SAME")
            
        if grid:
            self.c.SetGrid(1,1)
        self.c.Update()
        self.c.Draw()

    def getGraphs(self):
        return self.graphs