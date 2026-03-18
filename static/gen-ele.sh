#!/bin/bash

for tt in {0..7000..1000}
do
   echo "#V(A3/cell) F(eV/cell) id" > $tt-vf.dat

   for i in 0.99 1.000 1.01 1.02 1.03 1.04 
   do
       cd $i/$tt/
       # cd $i/encut_400-$tt
       F=$( vasp6E.py -i OUTCAR -e -c | tail -1 | awk '{print $2}')
       V=$( vasp6E.py -i OUTCAR -e -c | tail -1 | awk '{print $1}')
       echo "$V $F $i" >> ../../$tt-vf.dat
       cd ../../
   done
done

mkdir -p entropies
mv *-vf.dat entropies/

cd entropies/
./../../gen-ele.py

