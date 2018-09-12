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

bins = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]
systematics=["btag","mistag"]
monojet_category = {}
out_file_name = 'monojet.root'
categories = []

for s in ['0tag','1tag', '2tag']:
     monojet_category[s] = {
        'name':"monojet_"+s
        #,'in_file_name':"/uscms_data/d1/shoh/panda/v_8029_DarkHiggs_v2/flat/limits/fittingForest_monojet_"+s+".root"
       # ,'in_file_name':"/uscms/home/naina25/nobackup/Panda_2018/Panda_Analysis/CMSSW_8_0_29/src/PandaAnalysis/SuperMonoJet/fitting/fittingForest_monojet_"+s+".root"
        ,'in_file_name':"/uscms_data/d3/naina25/panda/80X-v1.5-monojet/fittingForest_"+s+".root"
        ,"cutstring":""
        ,"varstring":["min(999.9999,met)",250,1250]
        ,"weightname":"weight"
        ,"bins":bins[:]
        ,"additionalvars":[]
        ,"pdfmodel":0
	,"samples":
             {  
		  # Signal Region
#		   "VH_signal_"+s    	       :['signal'+s,'vh',1,0]
		  "Zvv_signal_"+s    	       :['signal'+s,'zjets',1,0]
                  ,"Zll_signal_"+s	               :['signal'+s,'zll',1,0]
 		  ,"Wlv_signal_"+s  	       :['signal'+s,'wjets',1,0]
		  ,"Diboson_signal_"+s  	       :['signal'+s,'dibosons',1,0]
		  ,"ttbar_signal_"+s   	       :['signal'+s,'ttbar',1,0]
		  ,"ST_signal_"+s                 :['signal'+s,'stop',1,0]
		  ,"QCD_signal_"+s		       :['signal'+s,'qcd',1,0]
		  ,"Data_signal_"+s	       :['signal'+s,'data',0,0]
		  # signals

		  # Di muon-Control
#                  ,"VH_zmm_"+s                    :['dimuon'+s,'vh',1,0] 
                  ,"Zll_zmm_"+s	               :['dimuon'+s,'zll',1,1]
		  ,"Diboson_zmm_"+s    	       :['dimuon'+s,'dibosons',1,0]
		  ,"ttbar_zmm_"+s    	       :['dimuon'+s,'ttbar',1,0]
		  ,"Data_zmm_"+s    	       :['dimuon'+s,'data',0,0]

                  # Di electron-Control
#                  ,"VH_zee_"+s                    :['dielectron'+s,'vh',1,0] 
                  ,"Zll_zee_"+s                   :['dielectron'+s,'zll',1,1]
                  ,"Diboson_zee_"+s               :['dielectron'+s,'dibosons',1,0]
                  ,"ttbar_zee_"+s                 :['dielectron'+s,'ttbar',1,0]
                  ,"Data_zee_"+s                  :['dielectron'+s,'data',0,0]

                   # Single muon (w) control
#                  ,"VH_mn"                    :['singlemuon'+s,'vh',1,0] 
                  ,"Zll_wmn_"+s                   :['singlemuon'+s,'zll',1,0]
                  ,"Wlv_wmn_"+s                   :['singlemuon'+s,'wjets',1,1]
                  ,"Diboson_wmn_"+s               :['singlemuon'+s,'dibosons',1,0]
                  ,"ttbar_wmn_"+s                 :['singlemuon'+s,'ttbar',1,0]
                  ,"QCD_wmn_"+s                   :['singlemuon'+s,'qcd',1,0]
                  ,"Data_wmn_"+s                  :['singlemuon'+s,'data',0,0]

                   # Single electron (w) control
#                  ,"VH_en"                    :['singleelectron'+s,'vh',1,0] 
                  ,"Zll_wen_"+s                   :['singleelectron'+s,'zll',1,0]
 		  ,"Wlv_wen_"+s                   :['singleelectron'+s,'wjets',1,1]
		  ,"Diboson_wen_"+s               :['singleelectron'+s,'dibosons',1,0]
		  ,"ttbar_wen_"+s                 :['singleelectron'+s,'ttbar',1,1]
		  ,"ST_wen_"+s                    :['singleelectron'+s,'stop',1,0]
		  ,"QCD_wen_"+s                   :['singleelectron'+s,'qcd',1,0]
		  ,"Data_wen_"+s                  :['singleelectron'+s,'data',0,0]

                   # Single photon control
                  ,"Pho_pho_"+s                 :['singlephoton'+s,'gjets',1,1]
                  ,"QCD_pho_"+s                   :['singlephoton'+s,'qcd',1,0]
                  ,"Data_pho_"+s                  :['singlephoton'+s,'data',0,0]
                  }

        }
     categories.append(monojet_category[s])
