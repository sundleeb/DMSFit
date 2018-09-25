# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis

# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#		TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!
#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptpho cuts) if this key is missing, the code will not complain   

# Can define anything useful here outside the catefory dictionary which may be common to several categories, eg binning in MET, systematics ecc
# systematics will expect samples with sample_sys_Up/Down but will skip if not found 

bins = [250,270,350,475,1000]
systematics=["btag","mistag"]
cutstrings=["n2ddt56<0 && fjmass>0 && fjmass<60","n2ddt56<0 && fjmass>60 && fjmass<105","n2ddt56<0 && fjmass>105 && fjmass<150","n2ddt56<0 && fjmass>150 && fjmass<3000"]
#cutstrings=["n2ddt56<0 && fjmass>0 && fjmass<60"]
boosted_category = {}
categories = []
out_file_name = 'boosted.root'

for mass in range(0,len(cutstrings)):
    for s in ['doublebp','doublebf']:
        boosted_category[s+str(mass)] = {
             'name':"boosted_"+s+"_mass"+str(mass)
             ,'in_file_name':"/uscms/home/ahall/nobackup/LPC-DM/CMSSW_8_0_29/src/PandaAnalysis/SuperMonoJet/fitting/boosted_withsignals/fittingForest_boosted_"+s+".root"
            ,"cutstring":cutstrings[mass]
            ,"varstring":["min(999.9999,met)",250,1000]
       	    ,"weightname":"weight"
	    ,"bins":bins[:]
	    ,"additionalvars":[]
            ,"pdfmodel":0
	    ,"samples":
	   	{  
		  # Signal Region
#		   "VH_signal"    	       :['signal','vh',1,0]
                "Zvv_signal"    	       :['signal','zjets',1,0]
                ,"Zll_signal"	               :['signal','zll',1,0]
                ,"Wlv_signal"  	       :['signal','wjets',1,0]
                ,"Diboson_signal"  	       :['signal','dibosons',1,0]
                ,"ttbar_signal"   	       :['signal','ttbar',1,0]
                ,"ST_signal"                 :['signal','stop',1,0]
                ,"QCD_signal"		       :['signal','qcd',1,0]
                ,"Data_signal"	       :['signal','data',0,0]
                #		  signals
                , "BBbarDM_MZprime-1000_Mhs-90_Mchi-100_signal"   :['signal','BBbarDM_MZprime-1000_Mhs-90_Mchi-100_signal',1,1]
                , "BBbarDM_MZprime-1000_Mhs-90_Mchi-250_signal"   :['signal','BBbarDM_MZprime-1000_Mhs-90_Mchi-250_signal',1,1]
                , "BBbarDM_MZprime-1000_Mhs-90_Mchi-400_signal"   :['signal','BBbarDM_MZprime-1000_Mhs-90_Mchi-400_signal',1,1]
                , "BBbarDM_MZprime-1000_Mhs-90_Mchi-50_signal"    :['signal','BBbarDM_MZprime-1000_Mhs-90_Mchi-50_signal',1,1]

#		  Di muon-Control
#                 ,"VH_zmm"                    :['dimuon','vh',1,0] 
                ,"Zll_zmm"	               :['dimuon','zll',1,1]
#                ,"Wlv_zmm"      	       :['dimuon','wjets',1,0]
                ,"Diboson_zmm"    	       :['dimuon','dibosons',1,0]
                ,"ttbar_zmm"    	       :['dimuon','ttbar',1,0]
#                ,"ST_zmm"                    :['dimuon','stop',1,0]
#                ,"QCD_zmm"		       :['dimuon','qcd',1,0]
                ,"Data_zmm"    	       :['dimuon','data',0,0]
		  # Single muon (top) control
#                  ,"VH_tm"                     :['singlemuontop','vh',1,0] 
#                  ,"ttH_tm"                    :['singlemuontop','tth',1,0] 
                ,"Zll_tmn"       	       :['singlemuontop','zll',1,0]
                ,"Wlv_tmn"                    :['singlemuontop','wjets',1,0]
                ,"Diboson_tmn"                :['singlemuontop','dibosons',1,0]
                ,"ttbar_tmn"                  :['singlemuontop','ttbar',1,1]
                ,"ST_tmn"                     :['singlemuontop','stop',1,0]
                ,"QCD_tmn"                    :['singlemuontop','qcd',1,0]
                ,"Data_tmn"        	       :['singlemuontop','data',0,0]

                   # Single muon (w) control
#                  ,"VH_wmn"                    :['singlemuonw','vh',1,0] 
                ,"Zll_wmn"     	       :['singlemuonw','zll',1,0]
                ,"Wlv_wmn"      	       :['singlemuonw','wjets',1,0]
                ,"Diboson_wmn"               :['singlemuonw','dibosons',1,0]
                ,"ttbar_wmn"                 :['singlemuonw','ttbar',1,0]
                ,"ST_wmn"                    :['singlemuonw','stop',1,0]
                ,"QCD_wmn"	               :['singlemuonw','qcd',1,0]
                ,"Data_wmn"	               :['singlemuonw','data',0,0]

		  # Di electron-Control
#                  ,"VH_zee"                    :['dielectron','vh',1,0] 
                ,"Zll_zee"	               :['dielectron','zll',1,0]
# 		  ,"Wlv_zee"  	               :['dielectron','wjets',1,0]
                ,"Diboson_zee"               :['dielectron','dibosons',1,0]
                ,"ttbar_zee"                 :['dielectron','ttbar',1,0]
#		  ,"ST_zee"                    :['dielectron','stop',1,0]
#		  ,"QCD_zee"                   :['dielectron','qcd',1,0]
                ,"Data_zee"	               :['dielectron','data',0,0]


		  # Single electron (top) control
#                  ,"VH_te"                     :['singleelectrontop','vh',1,0] 
#                  ,"ttH_te"                    :['singleelectrontop','tth',1,0] 
                ,"Zll_ten"                    :['singleelectrontop','zll',1,0]
                ,"Wlv_ten"                    :['singleelectrontop','wjets',1,0]
                ,"Diboson_ten"                :['singleelectrontop','dibosons',1,0]
                ,"ttbar_ten"                  :['singleelectrontop','ttbar',1,0]
                ,"ST_ten"                     :['singleelectrontop','stop',1,0]
                ,"QCD_ten"                    :['singleelectrontop','qcd',1,0]
                ,"Data_ten"                   :['singleelectrontop','data',0,0]

                   # Single electron (w) control
#                  ,"VH_wen"                    :['singleelectronw','vh',1,0] 
                ,"Zll_wen"                   :['singleelectronw','zll',1,0]
                ,"Wlv_wen"                   :['singleelectronw','wjets',1,0]
                ,"Diboson_wen"               :['singleelectronw','dibosons',1,0]
                ,"ttbar_wen"                 :['singleelectronw','ttbar',1,0]
                ,"ST_wen"                    :['singleelectronw','stop',1,0]
                ,"QCD_wen"                   :['singleelectronw','qcd',1,0]
                ,"Data_wen"                  :['singleelectronw','data',0,0]
                }
             }


        with open('/uscms/home/ahall/nobackup/LPC-DM/CMSSW_8_0_29/src/PandaAnalysis/LPC_T3/merging/signals.txt', 'r') as signal_file:
            for line in signal_file:
                name = line.rstrip()
                boosted_category[s+str(mass)]['samples'][name+'_signal'] = ['signal',name+'_signal',1,1]
        if 'doublebf' in s:
            for sample in boosted_category[s+str(mass)]['samples']:
                if not 'fail' in sample:
                    boosted_category[s+str(mass)]['samples'][sample+'_fail'] = boosted_category[s+str(mass)]['samples'].pop(sample)

                    
        
        categories.append(boosted_category[s+str(mass)])
