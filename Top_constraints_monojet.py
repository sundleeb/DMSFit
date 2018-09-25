import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "ttbar"
convertHistograms = []

### helper functions ###

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "TTbar" # Give a name of the process being modelled
  metname = "met"    # Observable variable name 

  #define nominal (MC) of which process this config will model
  targetmc0tag     = _fin.Get("signal0tag_ttbar")
  targetmc1tag     = _fin.Get("signal1tag_ttbar")
  targetmc2tag     = _fin.Get("signal2tag_ttbar")
  #defines in / out acceptance
  controlmc0tag = _fin.Get("singlemuon0tag_ttbar")
  controlmc1tag = _fin.Get("singlemuon1tag_ttbar")
  controlmc2tag = _fin.Get("singlemuon2tag_ttbar")

  controlmc0tag_e = _fin.Get("singleelectron0tag_ttbar")
  controlmc1tag_e = _fin.Get("singleelectron1tag_ttbar")
  controlmc2tag_e = _fin.Get("singleelectron2tag_ttbar")


  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  TopScales0tag = targetmc0tag.Clone(); TopScales0tag.SetName("topwm0tag_weights_%s"%cid)
  TopScales0tag.Divide(controlmc0tag); _fOut.WriteTObject(TopScales0tag);

  TopScales0tag_e = targetmc0tag.Clone(); TopScales0tag_e.SetName("topwe0tag_weights_%s"%cid)
  TopScales0tag_e.Divide(controlmc0tag_e); _fOut.WriteTObject(TopScales0tag_e);

  TopScales1tag = targetmc1tag.Clone(); TopScales1tag.SetName("topwm1tag_weights_%s"%cid)
  TopScales1tag.Divide(controlmc1tag); _fOut.WriteTObject(TopScales1tag);

  TopScales1tag_e = targetmc1tag.Clone(); TopScales1tag_e.SetName("topwe1tag_weights_%s"%cid)
  TopScales1tag_e.Divide(controlmc1tag_e); _fOut.WriteTObject(TopScales1tag_e);

  TopScales2tag = targetmc2tag.Clone(); TopScales2tag.SetName("topwm2tag_weights_%s"%cid)
  TopScales2tag.Divide(controlmc2tag); _fOut.WriteTObject(TopScales2tag);

  TopScales2tag_e = targetmc2tag.Clone(); TopScales2tag_e.SetName("topwe2tag_weights_%s"%cid)
  TopScales2tag_e.Divide(controlmc2tag_e); _fOut.WriteTObject(TopScales2tag_e);

  TopScales2tagTo1tag = targetmc1tag.Clone(); TopScales2tagTo1tag.SetName("topwm2tagTo1tag_weights_%s"%cid)
  TopScales2tagTo1tag.Divide(controlmc2tag); _fOut.WriteTObject(TopScales2tagTo1tag);

  TopScales2tagTo1tag_e = targetmc1tag.Clone(); TopScales2tagTo1tag_e.SetName("topwe2tagTo1tag_weights_%s"%cid)
  TopScales2tagTo1tag_e.Divide(controlmc2tag_e); _fOut.WriteTObject(TopScales2tagTo1tag_e);

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc0tag.GetNbinsX()+1):
    _bins.append(targetmc0tag.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg TopScales

  CRs = [
   Channel("singlemuonw0tagModel",  _wspace,out_ws,cid+'_'+model,TopScales0tag),
   Channel("singleelectronw0tagModel",  _wspace,out_ws,cid+'_'+model,TopScales0tag_e),
   Channel("singlemuonw1tagModel",  _wspace,out_ws,cid+'_'+model,TopScales1tag),
   Channel("singleelectronw1tagModel",  _wspace,out_ws,cid+'_'+model,TopScales1tag_e),
   Channel("singlemuonw2tagModel",  _wspace,out_ws,cid+'_'+model,TopScales2tag),
   Channel("singleelectronw2tagModel",  _wspace,out_ws,cid+'_'+model,TopScales2tag_e),
   Channel("singlemuonw2tagTo1tagModel",  _wspace,out_ws,cid+'_'+model,TopScales2tagTo1tag),
   Channel("singleelectronw2tagTo1tagModel",  _wspace,out_ws,cid+'_'+model,TopScales2tagTo1tag_e)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=TopScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
 
  def addStatErrs(hx,cr,crname1,crname2):
    for b in range(1,targetmc0tag.GetNbinsX()+1):
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

  addStatErrs(TopScales0tag,CRs[0],'topwm0tag','singlemuonw0tagModel')
  addStatErrs(TopScales0tag_e,CRs[1],'topwe0tag','singleelectronw0tagModel')
  addStatErrs(TopScales1tag,CRs[2],'topwm1tag','singlemuonw1tagModel')
  addStatErrs(TopScales1tag_e,CRs[3],'topwe1tag','singleelectronw1tagModel')
  addStatErrs(TopScales2tag,CRs[4],'topwm2tag','singlemuonw2tagModel')
  addStatErrs(TopScales2tag_e,CRs[5],'topwe2tag','singleelectronw2tagModel')
  addStatErrs(TopScales2tagTo1tag,CRs[6],'topwm2tagTo1tag','singlemuonw2tagTo1tagModel')
  addStatErrs(TopScales2tagTo1tag_e,CRs[7],'topwe2tagTo1tag','singleelectronw2tagTo1tagModel')

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("wjets","ttbarsignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

