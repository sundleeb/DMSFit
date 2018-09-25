#!/bin/bash

for i in `ls boosted_resolved.txt`
do
    echo "sed -e s/..\/..\/..\/combined_model_boosted.root/..\/..\/combined_model_boosted.root/g $i > temp"
    sed -e "s/..\/boosted_datacards\/MASS\/.\/..\/..\/combined_model/..\/..\/combined_model/g" $i > temp
    mv temp $i
done
