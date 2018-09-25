#!/bin/bash

echo $1
if [[ "$1" == "monojet" ]]
then
    python buildModel.py $1
elif [[ "$1" == "boosted" ]]
then
    for mass in 0 1 2 3 ; do
	python buildModel.py $1 --mass $mass
    done
else
    for mass in 0 1 2 3 ; do
	for btag in pass fail ; do
	    python buildModel.py $1 --mass $mass --btag $btag
	done
    done
fi
rm $1.root
hadd $1.root *$1*.root