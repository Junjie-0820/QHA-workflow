#!/bin/bash
#SBATCH --output=qha.log
#SBATCH --error=qha.log
#SBATCH -N 1
#SBATCH -A sungroup
#SBATCH -p cpu
#SBATCH --ntasks-per-node=8
#SBATCH --job-name=phonopy
#SBATCH --mem=32G
#SBATCH -t 1:00:00

source /public/home/jjj/software/anaconda3/etc/profile.d/conda.sh
conda activate work

EXEC=~/software/anaconda3/envs/work/bin

for i in  feo.b8 #  cdd.*  stb.fe2o-tet stb.fe-hcp stb.ni-fcc
do 
	echo "Processing $i ..."
	cd $i/
	nat=$( grep natom: 1.000/thermal_properties.yaml | awk '{print $NF}')

	cd qha/
	scal_fac=(v2 v3 v4 v5 v6 v7 v8 v9 v10)
	thermal=()
	for j in ${scal_fac[@]}
	do    
		thermal+=("../$j/thermal_properties.yaml")
	done

	files=${thermal[@]}
	$EXEC/phonopy-qha -p --tmax=7000 --eos='birch_murnaghan' --efe fe-v.dat vol.dat $files > phonopy-qha.log

	phonopy_eos.py -i helmholtz-volume.dat -t {0..7000..10} -p 200 400 -nat $nat -c
	# phonopy2PG.py -i helmholtz-volume.dat -t {0..6000..10} -p 200 400
	mkdir -p PG
	mv PG_*K.dat VFfit_*K.dat PG/

	cd ../../ 
done
