#!/bin/bash

vid=(v2 v3 v4 v5 v6 v7 v8 v9 v10)
# nv=${#vid[@]}

name=$(basename `pwd`)
str="../../static_fe-o/$name"
cp $str/entropies/fe-v.dat qha/
cp $str/entropies/1000-vf.dat qha/
cat qha/1000-vf.dat | awk '{print $1, $2}' > qha/vol.dat ### delete last id column
echo "7010.0 ${vid[@]}" >> qha/fe-v.dat #### add a false point, just get Tmax

mkdir -p plot

for i in ${vid[@]}
do
    cd "$i"/
    cp ../../tools/mpi-phonon.slurm .
    sbatch mpi-phonon.slurm $i

    # phonopy -f disp*/vasprun.xml
    # cp ../band.conf .
    # cp ../thermal.conf .
    # phonopy -c CONTCAR band.conf -p -s
    # phonopy -c CONTCAR thermal.conf 
    # phonopy-bandplot --gnuplot band.yaml > phband.dat

    # cp band_dos.pdf ../plot/$i-band_dos.pdf
    # cp phband.dat ../plot/$i-phband.dat
    # cp total_dos.dat ../plot/$i-tdos.dat
    cd ../
done

# python3 ../../plot-phdos.py
# mv ph_tdos.png plot/
