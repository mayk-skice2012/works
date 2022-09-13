import numpy as np
import matplotlib.pyplot as plt
import os
import ROOT
from ROOT import gSystem
gSystem.Load( "libRooFit" )
import sys
from collections import defaultdict



#stdoutOrigin=sys.stdout

# fitting stuff
#for item, value in os.environ.items():
 #   print('{}: {}'.format(item, value))

#define functions
def shortTerm (t, par):
   return par[0]*np.exp(-t[0]/par[1])
def constTerm (t,par):
   return par[4];
def longTerm(t,par):
   return par[2]*( 1 - np.exp(-t[0]/par[3]))
def N_eff(t,par):
   return (1.0/( shortTerm(t, par)+ constTerm(t, par)+longTerm(t, par)))



# add data here
# import csv data file as a dictionary and create loop or update dictionary from here

#inputTime = np.array([0,40,80,150,210,350,650,1000,2000,3000,4000,10000])
inputTime = np.array([0,20,40,60,80,150,210,350,650,1000,2000,3000,4000,10000]) # for VPX37409W445 and VPA38189W1218
##### DATA
VPX37409W443_400 = ([19.5238,20.8401,21.3159,21.4975,21.5111,20.9199,19.7708,19.1142,17.8289, 16.848,16.2774,15.2291])
VPX37409W443_500 = np.array([21.3149, 21.7208, 21.7368, 22.0423, 22.4798, 21.5609, 21.2228, 21.411, 20.9321, 19.9253,19.4969,18.0352])
VPX37409W443_700 = np.array([21.7428, 22.1111, 22.5282, 22.5729, 22.8966, 22.081, 21.7027, 21.845, 22.0575, 22.0801,21.9819,22.6377])
VPX37409W443_1000 = np.array([22.1167, 22.4772, 22.912, 22.9702, 23.1433, 22.6303, 22.6251, 22.4143, 22.7038, 22.77994,22.7628,23.4903])

VPX37409W444_400 = np.array([10.5907, 11.4966, 11.9012, 12.3431, 12.2744, 11.8357, 10.9316, 10.2018, 9.48495, 8.48475, 8.3243,7.5639])
VPX37409W444_500 =np.array([ 12.4374, 13.5957, 14.1075, 14.6332, 14.598, 14.0643, 13.0157, 12.1025, 10.5715, 10.0532, 9.74607, 8.872])
VPX37409W444_700 =np.array([ 16.1137, 17.4483, 17.9387, 18.412, 18.4725, 17.9245, 16.8391, 15.8969, 13.8983, 13.0747, 12.7549, 11.5402])
VPX37409W444_1000 = np.array([19.7918, 20.5729, 20.617, 20.8457, 20.8692, 20.7835, 20.3241, 20.3772, 18.7621, 17.8312,17.4915, 16.2903])

VPX37409W445_400 = np.array([7.27248, 7.7786, 7.97396, 8.2541,8.33494,9.10734, 9.54263, 8.69054, 7.95919, 7.45714, 6.07452,7.98182,7.89625,5357.19])
VPX37409W445_500 = np.array([8.87673, 9.16574, 9.5654,9.92716,10.0743, 11.1077, 11.4287, 10.5424, 9.33992, 8.50073, 7.28106,7.35751,7.64157,6.13406])
VPX37409W445_700 = np.array([11.4782, 12.1417, 12.7146, 13.0992, 13.286, 14.4654, 14.8525, 13.7659, 12.5554, 11.3306, 9.60845,9.11734,8.64131,8.00391])
VPX37409W445_1000 = np.array([15.556, 16.2983, 16.7022, 17.066, 17.2091, 17.9712, 18.3379, 17.3807, 16.6608, 15.6569, 13.9633,14.1845,13.2726,13.5306])

VPA38189W1218_400 = ([6.11201, 6.23499, 6.43891, 6.6658, 6.80174, 7.23214, 7.23655, 7.36075, 6.78579, 6.17979, 5.36762, 5.13653, 4.97714, 4.42925])
VPA38189W1218_500 = np.array([7.49629, 7.44962, 7.70364, 7.778006, 7.92106, 8.71445, 8.70952, 9.02743, 8.15868, 7.35971, 6.48116, 5.77636, 5.94919, 5.35339])
VPA38189W1218_700 = np.array([9.92302, 10.1103, 10.4107,10.6307, 10.7671, 11.7972, 11.9715, 12.3132, 11.2301, 10.0441,8.93976,7.78444,8.58948, 8.32907])
VPA38189W1218_1000= np.array([13.9524, 14.8879,15.0426, 15.7011, 15.2071, 15.8741, 15.6618, 16.2691, 15.8217, 15.2593, 15.5999,11.5371, 16930.6, 20.0478])


# storing it in a dictionary:
VPX37409W444 = {
    "400V" : VPX37409W444_400,
    "500V": VPX37409W444_500,
    "700V" : VPX37409W444_700,
    "1000V:": VPX37409W444_1000}

VPX37409W443 = {
    "400V": VPX37409W443_400,
    "500V": VPX37409W443_500,
    "700V": VPX37409W443_700,
    "1000V:": VPX37409W443_1000}

VPX37409W445 = {
    "400V": VPX37409W445_400,
    "500V": VPX37409W445_500,
    "700V": VPX37409W445_700,
    "1000V:": VPX37409W445_1000}

VPA38189W1218 = {
    "400V": VPA38189W1218_400,
    "500V": VPA38189W1218_500,
    "700V": VPA38189W1218_700,
    "1000V:": VPA38189W1218_1000}

# closure test for 500V
#you have to change
voltage500 = {
    "1e14_VPX37409W443_500V": VPX37409W443_500,
    "5e14_VPX37409W444_500V": VPX37409W444_500,
    "1e15_VPX37409W445_500V": VPX37409W445_500,
    "1.6e15_VPA38189W1218_500V:": VPA38189W1218_500}
# add on voltages here to test

# parameter value for closure test
#you have to change
parameter = {
    "1e14_VPX37409W443_500V":[0.0066749794094572825, 0.010850533720878405, 0.04366333],
    "5e14_VPX37409W444_500V":[0.027773924248939055, 0.04218588688015059, 0.059594413],
    "1e15_VPX37409W445_500V":[0.04355711291561264, 0.06201236351113741, 0.07863400000000001],
    "1.6e15_VPA38189W1218_500V:": [0.054530965364589054, 0.07328103032307359, 0.10194778]}
for voltage, values in voltage500.items():
    print("VOLTAGE :", voltage)
    # reset the values to zero
    x = np.empty(len(inputTime))
    y = np.empty(len(inputTime))
    ex = np.empty(len(inputTime))
    ey = np.empty(len(inputTime))
    dummy_arr = list(values) #idk if we need this we do
    name = str(voltage)

    # store the values in an array with error
    for i in range(len(dummy_arr)):
        x[i] = inputTime[i]
        y[i] = dummy_arr[i]
        ey[i] = dummy_arr[i] * 0.025 # this is the error, need to increase
        ex[i] = 0
    # loop to set values and errors xt, yt and db
    # resets to zero for each voltage the outerloop goes through
    xin = 0
    yin = 0
    eyin = 0
    xt = ROOT.RooRealVar("xt", "xt", 12, 15000)
    yt = ROOT.RooRealVar("yt", "yt", 0, 100)
    argSet = ROOT.RooArgSet(xt, yt)
    dxy = ROOT.RooDataSet("dxy", "dxy", argSet, ROOT.RooFit.StoreError(argSet))
    db = ROOT.RooDataSet("db", "db", argSet, ROOT.RooFit.StoreError(argSet))
    for i in range(len(dummy_arr)):
        xin = x[i]  # takes each value
        xt.setVal(xin)
        xt.setError(0)
        if i < 5:
            xt.setError(0.5 / 1.)
        else:
            xt.setError(1.0 / 1)
        yin = y[i]
        eyin = ey[i]
        if (y[i] == 0 and i != 0):
            yin = (y[i - 1] + y[i + 1]) / 2
            ey[i] = (ey[i - 1] + ey[i + 1]) / 2
            eyin = ey[i]
        if (eyin == 0.0):
            eyin = 0.19
        yt.setVal(yin)
        yt.setError(eyin)
        print("x,y,dx,dy:", x[i], y[i], ex[i], ey[i])
        dxy.add(ROOT.RooArgSet(xt, yt))
        db.add(ROOT.RooArgSet(xt, yt))


    # define fit parameters


    #you have to change name
    if name == "1e14_VPX37409W443_500V":
        for sensor, par in parameter.items():
            if sensor == name:
                FF_ga = ROOT.RooRealVar("FF_ga", "FF_ga", par[0], par[0], par[0])
                FF_tau_a = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 50., 50., 50.)
                FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY",par[1], par[1], par[1])
                FF_tau_Y = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000., 1000., 1000.)
                #FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC",  par[2], par[2], par[2])
                FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC", .2, 0, 100)

    if name == "5e14_VPX37409W444_500V":
        for sensor, par in parameter.items():
            if sensor == name:
                FF_ga = ROOT.RooRealVar("FF_ga", "FF_ga", par[0], par[0], par[0])
                FF_tau_a = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 50., 50., 50.)
                FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY",par[1], par[1], par[1])
                FF_tau_Y = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000, 1000, 1000)
                #FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC",  par[2], par[2], par[2])
                FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC", .2, 0, 100)
    if name == "1e15_VPX37409W445_500V":
        for sensor, par in parameter.items():
            if sensor == name:
                FF_ga = ROOT.RooRealVar("FF_ga", "FF_ga", par[0], par[0], par[0])
                FF_tau_a = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 50., 50., 50.)
                FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY",par[1], par[1], par[1])
                FF_tau_Y = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000, 1000, 1000)
                FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC",  par[2], par[2], par[2])
    if name == "1.6e15_VPA38189W1218_500V:":
        for sensor, par in parameter.items():
            if sensor == name:
                FF_ga = ROOT.RooRealVar("FF_ga", "FF_ga",par[0], par[0], par[0])
                FF_tau_a = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 50., 50., 50.)
                FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY",par[1], par[1], par[1])
                FF_tau_Y = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000, 1000, 1000)
                FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC", par[2], par[2], par[2])

    #FF_ga = ROOT.RooRealVar("FF_ga", "FF_ga", 0.05453, 0.05453, 0.05453)
    #FF_ga_443 = ROOT.RooRealVar("FF_ga", "FF_ga", .146, 0, 10)
    #FF_tau_a = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 45, 0, 2000)
    #FF_tau_a_443 = ROOT.RooRealVar("FF_tau_a", "FF_tau_a", 50., 50., 50.)
    #FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY", 0.050, 0.050, 0.050)
    #FF_gy = ROOT.RooRealVar("FF_gY", "FF_gY",0.07328, 0.07328, 0.07328)
    #FF_gy_443 = ROOT.RooRealVar("FF_gY", "FF_gY",.096, 0, 200)
    #FF_tau_Y_443 = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000, 1000, 1000)
    #FF_tau_Y = ROOT.RooRealVar("FF_tau_Y", "FF_tau_Y", 1000., 0, 10000.)
    #FF_gc = ROOT.RooRealVar("FF_gC", "FF_gC", 0.06, 0.06, 0.06)
    #FF_gc_443 = ROOT.RooRealVar("FF_gC", "FF_gC",  .2, 0, 100)

    # define function to be fitted
    Neff_CCE = ROOT.TF1("Neff_CCE", N_eff, 0., 20000, 5)

    pars = ROOT.RooArgSet(FF_ga,FF_tau_a,FF_gy,FF_tau_Y,FF_gc)
    CCE = (ROOT.RooFit.bindFunction(Neff_CCE, xt, pars))
    super(ROOT.RooAbsReal, CCE)
    CCE.chi2FitTo(dxy, ROOT.RooFit.YVar(yt))
    CCE.Print()

    #writing parameters in txt file
    #you have to change title
    title = "/Users/maykanda/PycharmProjects/pythonProject/closure_test/" + name + "_test2.txt"
    with open(title, 'w') as f:
        print("name","par value","error",file = f, sep = ",")
    result = CCE.chi2FitTo(dxy, ROOT.RooFit.YVar(yt))
    fitargs = ROOT.RooArgSet(FF_ga, FF_tau_a, FF_gy, FF_tau_Y, FF_gc)
    fitargs.Print()
    iter = fitargs.createIterator()
    var = iter.Next()
    while var:
        param_name = var.GetName()
        value = var.getVal()
        error = var.getError()
        with open(title, "a") as f:
            print(param_name, value, error, file = f, sep = " ")
        var = iter.Next()



    #Plotting
    frame = xt.frame(ROOT.RooFit.Title(" "+name +";Annealing time [mins];CCE[ke]"))
    frame2 = xt.frame(ROOT.RooFit.Title("Chi^2 fit of function set of (X#pmdX,Y#pmdY) values"))
    CCE.plotOn(frame)
    dxy.plotOnXY(frame2, ROOT.RooFit.YVar(yt))
    frame.SetMarkerStyle(20)
    c = ROOT.TCanvas("c5", "Annealing Time", 600, 600)
    ROOT.gPad.SetLeftMargin(0.15)
    frame.GetYaxis().SetTitleOffset(1.6)
    frame.GetYaxis().SetRangeUser(0, 30)
    c.SetLogx()
    frame.Draw()
    frame2.Draw("Same")

    #you have to change name
    c.SaveAs( "/Users/maykanda/PycharmProjects/pythonProject/closure_test/"+name + "_test2.png")
    c.Update()
