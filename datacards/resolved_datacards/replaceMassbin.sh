#!/bin/bash

regexp="mass0"
mkdir -p mass1 mass2 mass3
#eval cd ${regexp}
for bin in mass1 mass2 mass3
do
    eval cd ${regexp}
    for i in `ls resolved_*.txt`
    do
	echo "sed -e s/${regexp}/${bin}/g $i > ../${bin}/$i"
	sed -e "s/${regexp}/${bin}/g" $i > ../${bin}/$i
    done
    eval cd ..
done