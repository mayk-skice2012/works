//This was derived from W635_2e15_CCE

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <fstream>
#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdlib>
#include <TCanvas.h>
#include <TROOT.h>
#include <TDirectory.h>
#include <TStyle.h>
#include <TH1.h>
#include <TH2.h>
#include <TF1.h>
#include <TRegexp.h>
#include <TSystem.h>
#include <TGraphErrors.h>
#include <algorithm>
#include "TProfile.h"
#include "TFile.h"
//#include "AsciiRoot.h"
#include "TVirtualFitter.h"
#include "MollFit.h"
#include "TRandom.h"
//#include "AtlasLabels.h"
//#include "AtlasStyle.h"


#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooLandau.h"
#include "RooDataHist.h"
#include "RooFFTConvPdf.h"
#include "RooPlot.h"
#include "RooNLLVar.h"
#include "RooAddPdf.h"
#include "RooGenericPdf.h"
#include "TAxis.h"
#include "TH1.h"
#include "TRandom.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooPolyVar.h"
#include "RooConstVar.h"
#include "RooChi2Var.h"
#include "RooChi2Var.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TF1.h"
#include "Math/DistFunc.h"
#include "RooTFnBinding.h"
#include "RooTFnPdfBinding.h"   // I added this RSO
#include "RooCFunction1Binding.h"
#include "RooCFunction3Binding.h"
#include <stdio.h> //Avani trying to print variable names 
#define getName(var) # var



using namespace std;
using namespace RooFit ;


MollFit::MollFit()
{
}
MollFit::~MollFit()
{
}
void MollFit::Run()
{
  ReadAnnealingData();
  PlotAnnealingData();
    return ;
}

// function code in C

double short_term (double *t, double *par){
 
  return ( par[0]*exp(-t[0]/par[1]));  
}

double const_term(double *t, double *par) {
    return par[4];
  }
double long_term(double *t, double *par) {
    return  par[2]*( 1 - exp(-t[0]/par[3]));
  }

double Neff (double *t, double *par){
   return 1.0/( short_term(t , par)+ const_term(t, par)+long_term(t, par));
}
void MollFit::ReadAnnealingData()
{
  using namespace std;

//Removed Code to Read data from text file
// This data put in my hand. Comes from IRRAD sensors data on a .py file need to upload 

// Have adapted redundat structure from version which read in from text file
//The dimensions have to be set by hand for each data set
//

//VPX37414W120 //500V 

 /* RunData[0].AnnealingTime[0] = 80  ;
  RunData[0].AnnealingTime[1] = 160 ;
  RunData[0].AnnealingTime[2] = 240 ;
  RunData[0].AnnealingTime[3] = 320 ;
  RunData[0].AnnealingTime[4] = 620 ;
  RunData[0].AnnealingTime[5] = 920 ;
  RunData[0].AnnealingTime[6] = 1920;

  RunData[0].PulseHeight[0] = 6.493 ;
  RunData[0].PulseHeight[1] =7.7357 ;
  RunData[0].PulseHeight[2] =6.9567 ;
  RunData[0].PulseHeight[3] = 7.20242 ;
  RunData[0].PulseHeight[4] =6.9162 ;
  RunData[0].PulseHeight[5] =6.7628 ;
  RunData[0].PulseHeight[6] =6.4559 ;

// this is from Leena data, unchanged 
  RunData[0].DeltaPulseHeight[0] =0.251395   ;
  RunData[0].DeltaPulseHeight[1] = 0.269592 ;
  RunData[0].DeltaPulseHeight[2] = 0.530842 ;
  RunData[0].DeltaPulseHeight[3] = 0.271396  ;
  RunData[0].DeltaPulseHeight[4] = 0.24252  ;
  RunData[0].DeltaPulseHeight[5] = 0.231606  ;
  RunData[0].DeltaPulseHeight[6] = 0.205629 ; */
// running the loop four times instead of 16 

  float VPX37409W443_400[] = {19.5238,20.8401,21.3159,21.4975,21.5111,20.9199,19.7708,19.1142,17.8289, 16.848,16.2774}; 
  float VPX37409W443_500[] = {21.3149, 21.7208, 21.7368, 22.0423, 22.4798, 21.5609, 21.2228, 21.411, 20.9321, 19.9253,19.4969};
  float VPX37409W443_700[] = {21.7428, 22.1111, 22.5282, 22.5729, 22.8966, 22.081, 21.7027, 21.845, 22.0575, 22.0801,21.9819};
  float VPX37409W443_1000[] = {22.1167, 22.4772, 22.912, 22.9702, 23.1433, 22.6303, 22.6251, 22.4143, 22.7038, 22.77994,22.7628};

  float VPX37409W444_400[] = {10.5907, 11.4966, 11.9012, 12.3431, 12.2744, 11.8357, 10.9774, 10.1992, 8.9455,8.45363,8.32728};
  float VPX37409W444_500[] = {12.4374, 13.5957, 14.1075, 14.6332, 14.598, 14.0643, 13.0173, 12.0943, 10.6772,10.1194,9.80394};
  float VPX37409W444_700[] = {16.1137, 17.4483, 17.9387, 18.412, 18.4725, 17.9245, 16.8364, 15.8811, 13.8961,13.0734,12.7528};
  float VPX37409W444_1000[] = {19.7918, 20.5729, 20.617, 20.8457, 20.8692, 20.7835, 20.3208, 20.3673, 18.7591,17.8295,17.4887};

  float VPX37409W445_400[] = {7.27248, 7.7864, 7.93995, 8.2541, 8.33494, 9.10734, 9.54263, 8.69054, 7.86251, 7.04497, 6.08581,5.78089,5473.07};
  float VPX37409W445_500[] = {8.87673, 9.16574, 9.5654, 9.92716, 10.0743, 11.1077, 11.4287, 10.5424, 9.43176, 8.53917, 7.24545,6.85414,6.54227};
  float VPX37409W445_700[] = {11.4782, 12.1417, 12.7146, 13.0992, 13.286, 14.4654, 14.8525, 13.7659, 12.5355, 11.3288, 9.60698,9.11734,8.53616};
  float VPX37409W445_1000[] = {15.556, 16.2983, 16.7022, 17.066, 17.2091, 17.9712, 18.3379, 17.3807, 16.6059, 15.6255, 13.9612,14.1845,13.2877};

  float VPA38189W1218_400[] = {6.11201, 6.23499, 6.43891, 6.65857, 6.80174, 7.23214, 7.23655, 7.36075, 6.78579, 6.17979, 5.36762,5.13653}; //this data has not been updated only until 2000mins 
  float VPA38189W1218_500[] = {7.49629, 7.44962, 7.70364, 7.78006, 7.92106, 8.71445, 8.70952, 9.02743, 8.15868, 7.35971, 6.48116,5.77636};
  float VPA38189W1218_700[] = {9.92302, 10.1103, 10.4107, 10.6307, 10.7671, 11.7972, 11.9715, 12.3132, 11.2301, 10.0441, 8.93976,};
  float VPA38189W1218_1000[] = {13.9524, 14.8879, 15.0426, 15.0711, 15.2071, 15.8741, 15.6618, 16.2691, 15.8217, 15.2593, 15.5999};

  float VPX32471W50_500[] = {7.813854407, 7.87849004, 7.907179688, 8.744569336, 8.0976, 7.09068, 6.46418, 6.2705, 6.07138,6.06264,5.56201,5.90742, 5.45304};
  float VPX32471W50_700[] = {10.57308072,10.52499219,10.41631641,10.74346875,9.75106,9.02023,7.97544,7.59605,7.3378,7.163087,6.88145,6.48112,7.05509};
  float VPX32413W95_500[] = {13.1794912,11.64144043,11.52743,12.0755,11.8863,10.64436,9.88734,9.57337,10.1037,9.42398,9.18225,8.99506,8.83459};
  float VPX32413W95_700[] = {16.94600391,14.49496484,14.24294629,14.96361816,13.78749219,13.1545,12.2178,11.6966,11.3938,10.622084,10.3083,10.2108,9.97159};


  float AnnealingTimes[] = {0,20,40,60,80,150,210,350,650,1000,2000,3000,4000}; // this is for VPX37409W445 and VPA38189W1218
  float AnnealingTimes2[] = {0,40,80,150,210,350,650,1000,2000,3000,4000};
  float AnnealingTimes3[] = {80,150,200,350,650,1000,1500,2000,3000,4000, 5000, 6000, 7000};



  /*float* VPX37409W443[] = {VPX37409W443_400,VPX37409W443_500,VPX37409W443_700,VPX37409W443_1000};
  float* VPX37409W444[] = {VPX37409W444_400,VPX37409W444_500,VPX37409W444_700,VPX37409W444_1000};
  float* VPX37409W445[] = {VPX37409W445_400,VPX37409W445_500,VPX37409W445_700,VPX37409W445_1000}; 
  float* VPA38189W1218[]= {VPA38189W1218_400,VPA38189W1218_500,VPA38189W1218_700,VPA38189W1218_1000}; 

  float** LongTermAnnealingStudySensors[] = {VPX37409W443,VPX37409W444,VPX37409W445,VPA38189W1218}; 
  

 cout << "End of Run     "  << endl;
for (int i = 0; i<4;i++){
  cout <<"Sensor Name:   " << getName(LongTermAnnealingStudy[i]) << endl; // does not work 
  for (int j=0; j<4 ; ++i){
    cout<<"test print:" << LongTermAnnealingStudySensors[i,j] << endl;
  //double val = double(LongTermAnnealingStudySensors[i,j]);
  //RunData[0].PulseHeight[j] = val;
  //RunData[0].DeltaPulseHeight[j] = val * 0.025;
  //RunData[0].AnnealingTime[j] = AnnealingTimes[j];
  }
  }
*/


for (int i=0; i<13; ++i){
  RunData[0].PulseHeight[i] = VPX32413W95_700[i];
  RunData[0].DeltaPulseHeight[i] = VPX32413W95_700[i]*0.025;
  RunData[0].AnnealingTime[i] = AnnealingTimes3[i];
  }

 
}


//
void MollFit::PlotAnnealingData()
{
  using namespace std;


  int i=0;
 
 
   for (i=0; i<13; ++i){
     cout << i <<  "    Anneal " <<  RunData[0].AnnealingTime[i] << " Pulse Ht  " << RunData[0].PulseHeight[i] << endl ;
}
  cout << endl ;


 double x[30];
 double y[30];
 double ex[30];
 double ey[30];
int j=0;
 for (j=0;j< 13; ++j){
  x[j] = RunData[0].AnnealingTime[j];

  // 3 is 400 Volts
  // we only run for one data set at present

  y[j] = RunData[0].PulseHeight[j];
  ex[j] = 0.0;
  ey[j] = RunData[0].DeltaPulseHeight[j];
}

   // C r e a t e   d a t a s e t   w i t h   X   a n d   Y   v a l u e s
   // -------------------------------------------------------------------
   // Make weighted XY dataset with asymmetric errors stored
   // The StoreError() argument is essential as it makes
   // the dataset store the error in addition to the values
   // of the observables. If errors on one or more observables
   // are asymmetric, one can store the asymmetric error
   // using the StoreAsymError() argument
   RooRealVar xt("xt", "xt", 10, 6000);   //exclude zero
   RooRealVar yt("yt", "yt", 0, 100);
   RooDataSet dxy("dxy", "dxy", RooArgSet(xt, yt), StoreError(RooArgSet(xt, yt)));
   RooDataSet db("db", "db", RooArgSet(xt, yt), StoreError(RooArgSet(xt, yt)));


// eliminate x=0 , i only goes to 17
   for (int i = 0; i < 13; ++i) {

  double xin = x[i];

  //   xt =  xin;
  xt.setVal(xin);
   xt.setError(i < 5 ? 0.5 / 1. : 1.0 / 1.);

     double yin = y[i];
     double eyin=ey[i];;

     if (y[i]==0.0 && i!=0){
     	yin = (y[i-1]+y[i+1])/2;
	ey[i] = ( ey[i-1]+ ey[i+1])/2;
        eyin = ey[i];

     }
     if (eyin == 0.0){eyin = 0.19;}

     //      yt = yin;
     yt.setVal(yin);  
      yt.setError(eyin);
      cout << " x,  y, dx, dy,    " << x[i] << "       " << y[i] << "          " << ex[i] << "  " << ey[i] << endl;
      dxy.add(RooArgSet(xt, yt));
      db.add(RooArgSet(xt,yt));
   }
 

// This sets the starting parameters for the fit 

    RooRealVar FF_ga("FF_ga", "FF_ga", .146, 0, 10);
   //     RooRealVar FF_tau_a("FF_tau_a", "FF_tau_a", 45 ,0, 2000);
    RooRealVar FF_tau_a("FF_tau_a", "FF_tau_a", 54.98 , 54.98, 54.98);
    RooRealVar FF_gY("FF_gY", "FF_gY", .096, 0, 200);
   // RooRealVar FF_tau_Y("FF_tau_Y", "FF_tau_Y", 1000, 0, 10000);
   RooRealVar FF_tau_Y("FF_tau_Y", "FF_tau_Y", 2091, 2091, 2091);
   RooRealVar FF_gC("FF_gC", "FF_gC", .2,0, 100);


// This defines the function to be fitted
// Neff is a function defined earlier
// 
   TF1 *Neff_CCE  = new TF1("Neff_CCE",Neff,0.,+6000, 5);
// This binds the RootFit variable f to function Neff_CCE from TF1 above
 
// Create an observable
// Create binding of above TF1 to observable

   RooArgSet pars(FF_ga,FF_tau_a,FF_gY,FF_tau_Y,FF_gC); // 
   RooAbsReal *CCE = bindFunction(Neff_CCE, xt, pars);
 
// Print CCE definition
   CCE->Print();

    // try approach from fitgen3 exampl

   // RooDataHist* db = new RooDataHist("db", "db", RooArgSet(xt,yt) ) ;
   // RooChi2Var chi2("chi2", "chi2", CCE, db);
   //
  RooPlot *frame3 = xt.frame(Title(" Sensor VPX32413W95_700, 5.1e14 ; Annealing Time in min; Collected Charge in ke"));
 
// P e r f o r m   c h i 2   f i t   t o   X + / - d x   a n d   Y + / - d Y   v a l u e s
// --------------------------------------------------------------------------------------
// Plot dataset in X-Y interpretation
  RooPlot *frame4 = xt.frame(Title("Chi^2 fit of function set of (X#pmdX,Y#pmdY) values"));
   
   dxy.plotOnXY(frame4, YVar(yt));
   cout << " After dxy.Plot    " << endl;
  
   //   Fit chi^2 using X and Y errors
    RooFitResult *result = CCE->chi2FitTo(dxy, YVar(yt), Save(1));
    RooArgSet fitargs = result->floatParsFinal();
    TIterator* iter(fitargs.createIterator());

    cout << "Final parameters:" << endl;

    //clear text file
    std::ofstream writing_file;
    std::string filename = "VPX32413W95_700_param.txt";
    writing_file.open(filename, std::ofstream::out | std::ofstream::trunc);
    writing_file.close();

    //write text file
    std::string chipname = "VPX32413W95_700";  //have to change depending on which chip to draw
    writing_file.open(filename, std::ofstream::app);
    writing_file <<"[" << chipname << "]"<< endl;
    writing_file.close();
    

    for (TObject *a = iter->Next(); a != 0; a = iter->Next()) 
    {
      RooRealVar *rrv = dynamic_cast<RooRealVar *>(a); 
      std::string name = rrv->GetName();
      Double_t val = rrv ->getVal();
      Double_t error = rrv -> getError();
      cout<< name << ":" << val <<"  +/-  "<< error << endl;
      writing_file.open(filename, std::ios::app);
      writing_file << name << ":" << val << "  +/-  "<< error << endl;
      writing_file.close();
    }
    

    cout << "########################" << endl;

   // Overlay fitted function
    CCE->plotOn(frame3, LineColor(kGreen));
   // Draw the plot on a canvas
   auto c5 =  new TCanvas("c5", "Annealing Time", 900, 600);
   TLegend *fitleg = new TLegend(.15,.8,.4,.9);
   fitleg->SetHeader( "LongTermAnnealingStudy");
   fitleg->AddEntry((TObject*)0," 700 Volts", "");
   fitleg -> AddEntry((TObject*)0, "");
   //fitleg->AddEntry(CCE) 
  // gStyle->SetLegendTextSize(0.);
   gPad->SetLeftMargin(0.15);
   frame3->GetYaxis()->SetTitleOffset(1.4);
   frame3->GetYaxis()->SetRangeUser(0.,20.);
   c5->SetLogx();
   frame3->Draw();
   fitleg->DrawClone("Same");
   frame4->Draw("Same");
   c5->SaveAs("Annealing_vs_Time_DB2B_700V.eps");
   return ;

}
//

#ifndef __CINT__
int main()
{
  //instantiates instance of class MollFit called obj
  //which is what you can call
//
  MollFit obj;
  obj.Run();
 return 0;
}
#endif
