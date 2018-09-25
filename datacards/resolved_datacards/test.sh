source MegaScript.sh
cp MASS/combine_all.txt ./combine_all_take2.txt
sed -s/XX-SIGNAL-XX/BBbarDM_MZprime-1000_Mhs-90_Mchi-100/ combine_all_take2.txt
combine -M AsymptoticLimits -t -1 combine_all_take2.txt --rAbsAcc 0 --rMax 30  | tee limits_tmp.txt 