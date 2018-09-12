 import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
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

  controlmc0tag    = _fin.Get("singlemuon0tag_wjets")  # defines in / out acceptance
  controlmc0tag_e  = _fin.Get("singleelectron0tag_wjets")  # defines in / out acceptance
  targetmc1tag     = _fin.Get("signal1tag_wjets")      # define monimal (MC) of which process this config will model
  controlmc1tag    = _fin.Get("singlemuon1tag_wjets")  # defines in / out acceptance
  controlmc1tag_e  = _fin.Get("singleelectron1tag_wjets")  # defines in / out acceptance
  controlmc2tag    = _fin.Get("singlemuon2tag_wjets")  # defines in / out acceptance
  controlmc2tag_e  = _fin.Get("singleelectron2tag_wjets")  # defines in / out acceptance

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  WScales1tag = targetmc1tag.Clone(); WScales1tag.SetName("wmn1tag_weights_%s"%cid)
  WScales1tag.Divide(controlmc1tag);  _fOut.WriteTObject(WScales1tag)

  WScales1tag_e = targetmc1tag.Clone(); WScales1tag_e.SetName("wen1tag_weights_%s"%cid)
  WScales1tag_e.Divide(controlmc1tag_e);  _fOut.WriteTObject(WScales1tag_e)

  WScales0tagTo1tag = targetmc1tag.Clone(); WScales0tagTo1tag.SetName("wmn0tagto1tag_weights_%s"%cid)
  WScales0tagTo1tag.Divide(controlmc0tag);  _fOut.WriteTObject(WScales0tagTo1tag)

  WScales0tagTo1tag_e = targetmc1tag.Clone(); WScales0tagTo1tag_e.SetName("wen0tagto1tag_weights_%s"%cid)
  WScales0tagTo1tag_e.Divide(controlmc0tag_e);  _fOut.WriteTObject(WScales0tagTo1tag_e)

  WScales2tagTo1tag = targetmc1tag.Clone(); WScales2tagTo1tag.SetName("wmn2tagto1tag_weights_%s"%cid)
  WScales2tagTo1tag.Divide(controlmc2tag);  _fOut.WriteTObject(WScales2tagTo1tag)

  WScales2tagTo1tag_e = targetmc1tag.Clone(); WScales2tagTo1tag_e.SetName("wen2tagto1tag_weights_%s"%cid)
  WScales2tagTo1tag_e.Divide(controlmc2tag_e);  _fOut.WriteTObject(WScales2tagTo1tag_e)

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuon1tagModel",_wspace,out_ws,cid+'_'+model,WScales1tag),
   Channel("singleelectron1tagModel",_wspace,out_ws,cid+'_'+model,WScales1tag_e),
   Channel("singlemuon0tagTo1tagModel",_wspace,out_ws,cid+'_'+model,WScales0tagTo1tag),
   Channel("singleelectron0tagTo1tagModel",_wspace,out_ws,cid+'_'+model,WScales0tagTo1tag_e),
   Channel("singlemuon2tagTo1tagModel",_wspace,out_ws,cid+'_'+model,WScales2tagTo1tag),
   Channel("singleelectron2tagTo1tagModel",_wspace,out_ws,cid+'_'+model,WScales2tagTo1tag_e)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  #CRs[0].add_nuisance("SingleMuonEff",0.01)
  #CRs[1].add_nuisance("SingleElEff",0.02)

  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,targetmc.GetNbinsX()+1):
      err = hx.GetBinError(b)
      if not hx.GetBinContent(b)>0:
        continue
      relerr = err/hx.GetBinContent(b)
      if relerr<0.01:
        continue
      byb_u = hx.Clone(); byb_u.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Up'%(crname1,cid,cid,crname2,b-1))
      byb_u.SetBinContent(b,hx.GetBinContent(b)+err)
      byb_d = hx.Clone(); byb_d.SetName('%s_weights_%s_%s_stat_error_%s_bin%d_Down'%(crname1,cid,cid,crname2,b-1))
      if err<hx.GetBinContent(b):
        byb_d.SetBinContent(b,hx.GetBinContent(b)-err)
      else:
        byb_d.SetBinContent(b,0)
      _fOut.WriteTObject(byb_u)
      _fOut.WriteTObject(byb_d)
      cr.add_nuisance_shape('%s_stat_error_%s_bin%d'%(cid,crname2,b-1),_fOut)

  addStatErrs(WScales1tag,CRs[0],'wmn1tag','singlemuon1tagModel')
  addStatErrs(WScales1tag_e,CRs[1],'wen1tag','singleelectron1tagModel')
  addStatErrs(WScales0tagTo1Tag,CRs[2],'wmn0tagto1tag','singlemuon0tagTo1tagModel')
  addStatErrs(WScales0tagTo1Tag_e,CRs[3],'wen0tagto1tag','singleelectron0tagTo1tagModel')
  addStatErrs(WScales2tagTo1Tag,CRs[4],'wmn2tagto1tag','singlemuon2tagTo1tagModel')
  addStatErrs(WScales2tagTo1Tag_e,CRs[5],'wen2tagto1tag','singleelectron2tagTo1tagModel')
  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat
