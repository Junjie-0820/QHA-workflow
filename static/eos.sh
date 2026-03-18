#!/bin/bash

for tt in {0..7000..1000}
do
    echo "#id V(A3/atom) F(eV/atom)" > $tt-vf.dat

    for i in 0.99 1.000 1.01 1.02 1.03 1.04 
    do
        cd $i/$tt/
	# cd $i/encut_400-$tt/
        F=$( vasp6E.py -i OUTCAR -e  | tail -1 | awk '{print $2}')
        V=$( vasp6E.py -i OUTCAR -e  | tail -1 | awk '{print $1}')
        echo "$i $V $F" >> ../../$tt-vf.dat
        cd ../../
    done
done

mkdir -p eos/
mv *-vf.dat eos/

cd eos/
for i in *vf.dat
do
	echo -e "\nfitting $i" >> fitting.log
	eos_PH.py -i $i -p 200 400 >> fitting.log
done
cd ../
