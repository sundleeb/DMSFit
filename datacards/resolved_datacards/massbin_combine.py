#!/bin/python

import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("massbin",type=str,help="Specify mass bin")
args = parser.parse_args()
#cwd = os.getcwd()

naming={
    #config files                            #CR/SR
    "resolved_dielectron_control"             : ["zee"],
    "resolved_dielectron_fail_control"        : ["zee_fail"],
    "resolved_dimuon_control"                 : ["zmm"],
    "resolved_dimuon_fail_control"            : ["zmm_fail"],
    "resolved_signal"                         : ["sig"],
    "resolved_signal_fail"                    : ["sig_fail"],
    "resolved_singleelectrontop_control"      : ["ten"],
    "resolved_singleelectrontop_fail_control" : ["ten_fail"],
    "resolved_singleelectronw_control"        : ["wen"],
    "resolved_singleelectronw_fail_control"   : ["wen_fail"],
    "resolved_singlemuontop_control"          : ["tmn"],
    "resolved_singlemuontop_fail_control"     : ["tmn_fail"],
    "resolved_singlemuonw_control"            : ["wmn"],
    "resolved_singlemuonw_fail_control"       : ["wmn_fail"],
}
command=["combineCards.py"]
for datacard in os.listdir("./"):
    if datacard.endswith(".txt"):
        if datacard == "resolved_datacard.txt" or datacard == "combined_mass0.txt" or not datacard.startswith('resolved'):
            continue
        #print datacard.split('.')[0]
        command.append(args.massbin+"_"+naming[datacard.split('.')[0]][0]+"=./"+datacard)
        #command.append(naming[datacard.split('.')[0]][0]+"=./"+args.massbin+"/"+datacard)
        
command.append("> combine_"+args.massbin+".txt")
print ' '.join(command)

