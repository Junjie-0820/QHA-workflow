#!/bin/bash
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH -N 1
#SBATCH -A sungroup
#SBATCH -p cpu
#SBATCH --ntasks-per-node=2
#SBATCH --job-name=phonopy
#SBATCH -t 0:10:00

source /public/home/jjj/software/anaconda3/etc/profile.d/conda.sh
conda activate work

EXEC=~/software/anaconda3/envs/work/bin/

i=${1}

$EXEC/phonopy -f disp*/vasprun.xml
cp ../band.conf .
cp ../thermal.conf .
$EXEC/phonopy -c CONTCAR band.conf -p -s
# sed -i "/TSTEP/s/.*/TSTEP = 10/" thermal.conf
$EXEC/phonopy -c CONTCAR thermal.conf
$EXEC/phonopy-bandplot --gnuplot band.yaml > phband.dat

cp band_dos.pdf ../plot/$i-band_dos.pdf
cp phband.dat ../plot/$i-phband.dat
cp total_dos.dat ../plot/$i-tdos.dat

