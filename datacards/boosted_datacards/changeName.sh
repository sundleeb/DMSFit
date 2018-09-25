#!/bin/bash

for bin in mass0 mass1 mass2 mass3
do
    eval cd ${bin}
    for i in `ls boosted_*.txt`
    do
	echo "sed -e s/..\/..\/..\/combined_model_boosted.root/..\/..\/combined_model_boosted.root/g $i > temp"
	sed -e "s/combined_model_boosted_missingsignals.root/combined_model_boosted.root/g" $i > temp
	mv temp $i
    done
    eval cd ..
done