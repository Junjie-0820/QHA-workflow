#!/bin/bash
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH -N 1
#SBATCH -A sungroup
#SBATCH -p cpu
#SBATCH --ntasks-per-node=64
#SBATCH --job-name=vasp
#SBATCH -t 3:00:00

module load oneapi/2023.2
module load gcc/12.1
#source /public/software/intel/oneapi2021/setvars.sh

srun hostname >./hostfile
echo $SLURM_NTASKS
echo "Date = $(date)"
echo "Hostname = $(hostname -s)"
echo "Working Directory = $(pwd)"
echo ""
echo "Number of Nodes Allocated = $SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated = $SLURM_NTASKS"
echo "Number of Cores/Task Allocated = $SLURM_CPUS_PER_TASK"
echo $SLURM_NPROCS

EXEC=/public/software/vasp/vasp-6.4.1-gam-ncl-std/bin

#mpirun  -np $SLURM_NTASKS $EXEC/vasp_std  > result

nelem=$(grep ZVAL POTCAR | wc -l)
nels=($(grep ZVAL POTCAR | awk '{print $(NF-3)}'))
nats=($(sed -n '7p' 1.000/CONTCAR))
nelect=0
for ((i=0; i<nelem; i++)); do
    nelect=$(python -c "print($nelect + ${nels[i]} * ${nats[i]})")
done
nbands=$(python -c "print(round(0.8 * $nelect))")

for vv  in 0.99  1.000  1.01  1.02  1.03  1.04
do
    cd $vv/

    for j in {0..7000..1000};do
        sigma=$(python -c "print(f'{8.617333262145e-5*$j:.3f}')")
    
    	mkdir -p $j/
        cp CONTCAR $j/POSCAR
        cp ../../INCAR.rlx $j/INCAR
	cp ../../KPOINTS $j/
        cp ../POTCAR $j/

    	cd $j/
        sed -i "/NBANDS/s/.*/NBANDS =    $nbands/" INCAR

        if (( $(echo "$sigma == 0" | bc -l) ));then
            sed -i "/SIGMA/s/.*/SIGMA  =    0.001/" INCAR
        else
            sed -i "/SIGMA/s/.*/SIGMA  =    $sigma/" INCAR
        fi
        
	mpirun  -np $SLURM_NTASKS $EXEC/vasp_std  > result
        cd ../
    done
 
    cd ../
done

