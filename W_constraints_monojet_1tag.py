 import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 

model = "wjets"

### helper functions ###

def makeW(cid,_fOut,newName,targetmc,controlmc,systs=None):
  WScales = targetmc.Clone(); WScales.SetName(newName+"_weights_%s"%cid)
  WScales.Divide(controlmc)
  _fOut.WriteTObject(WScales)

  if not(systs==None):
      WScalesUp = systs['targetmcbtagUp'].Clone();
      WScalesUp.SetName(newName+"_weights_%s_btag_Up"%cid)
      WScalesUp.Divide(systs['controlmcbtagUp'])

      WScalesDown = systs['targetmcbtagDown'].Clone(); 
      WScalesDown.SetName(newName+"_weights_%s_Down"%cid)
      WScalesDown.Divide(systs['controlmcbtagDown'])

      _fOut.WriteTObject(WScalesUp)
      _fOut.WriteTObject(WScalesDown)

  return WScales

def addWErrors(WScales,targetmc,newName,crName,_fOut,CRs,cid):
  for b in range(1,targetmc.GetNbinsX()+1):
    err = WScales.GetBinError(b)
    if not WScales.GetBinContent(b)>0:
      continue
    relerr = err/WScales.GetBinContent(b)
    if relerr<0.01:
      continue
    byb_u = WScales.Clone(); byb_u.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Up'%(newName,cid,cid,crName,b-1))
    byb_u.SetBinContent(b,WScales.GetBinContent(b)+err)
    byb_d = WScales.Clone(); byb_d.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Down'%(newName,cid,cid,crName,b-1))
    if err<WScales.GetBinContent(b):
      byb_d.SetBinContent(b,WScales.GetBinContent(b)-err)
    else:
      byb_d.SetBinContent(b,0)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    CRs.add_nuisance_shape('%s_stat_error_%s_bin%d'%(cid,crName,b-1),_fOut)


def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "WJets" # Give a name of the process being modelled
  metname      = "met"    # Observable variable name 

  targetmc1tag     = _fin.Get("signal1tag_wjets")      # define monimal (MC) of which process this config will model
  controlmc1tag    = _fin.Get("singlemuon1tag_wjets")  # defines in / out acceptance
  controlmc1tag_e  = _fin.Get("singleelectron1tag_wjets")  # defines in / out acceptance

  controlmc0tag    = _fin.Get("singlemuon0tag_wjets")  # defines in / out acceptance
  controlmc0tag_e  = _fin.Get("singleelectron0tag_wjets")  # defines in / out acceptance

  systs = {}; systs_e = {}

  # btag systs
  systs['targetmcbtagUp']      = _fin.Get("signal1tag_wjets_btagUp");           systs_e['targetmcbtagUp']      = systs['targetmcbtagUp']
  systs['targetmcbtagDown']    = _fin.Get("signal1tag_wjets_btagDown");         systs_e['targetmcbtagDown']    = systs['targetmcbtagDown']
  
  systs['controlmcbtagUp']     = _fin.Get("singlemuon0tag_wjets_btagUp");       systs_e['controlmcbtagUp']     = _fin.Get("singleelectron0tag_wjets_btagUp")
  systs['controlmcbtagDown']   = _fin.Get("singlemuon0tag_wjets_btagDown");     systs_e['controlmcbtagDown']   = _fin.Get("singleelectron0tag_wjets_btagDown")


  # Create the transfer factors and save them (note here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  WScales               = makeW(cid,_fOut,"wmn",targetmc1tag,controlmc1tag,None)
  WScales_e             = makeW(cid,_fOut,"wen",targetmc1tag,controlmc1tag_e,None)
  WScales_0tagTo1tag    = makeW(cid,_fOut,"wmn_0tagTo1tag",targetmc1tag,controlmc0tag,systs)
  WScales_e_0tagTo1tag  = makeW(cid,_fOut,"wen_0tagTo1tag",targetmc1tag,controlmc0tag_e,systs_e)

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc1tag.GetNbinsX()+1):
    _bins.append(targetmc1tag.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuon1tagModel",          _wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectron1tagModel",      _wspace,out_ws,cid+'_'+model,WScales_e),
   Channel("singlemuon0tagTo1tagModel",    _wspace,out_ws,cid+'_'+model,WScales_0tagTo1tag),
   Channel("singleelectron0tagTo1tagModel",_wspace,out_ws,cid+'_'+model,WScales_e_0tagTo1tag),
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  addWErrors(WScales,             targetmc1tag, "wmn",            "singlemuon1tagModel",           _fOut, CRs[0],cid)
  addWErrors(WScales_e,           targetmc1tag, "wen",            "singleelectron1tagModel",       _fOut, CRs[1],cid)
  addWErrors(WScales_0tagTo1tag,  targetmc1tag, "wmn_0tagTo1tag", "singlemuon0tagTo1tagModel",     _fOut, CRs[2],cid)
  addWErrors(WScales_e_0tagTo1tag,targetmc1tag, "wen_0tagTo1tag", "singleelectron0tagTo1tagModel", _fOut, CRs[3],cid)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc1tag.GetName(),CRs,diag)
  cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat
