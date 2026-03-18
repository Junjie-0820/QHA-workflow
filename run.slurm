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
nats=($(sed -n '7p' SPOSCAR))
nelect=0
for ((i=0; i<nelem; i++)); do
    nelect=$(python -c "print($nelect + ${nels[i]} * ${nats[i]})")
done
nbands=$(python -c "print(round(0.8 * $nelect))")

for i in disp_*
do
        cd $i/
        cp ../../input-pho/INCAR.scf INCAR
        cp ../../input-pho/KPOINTS .
        cp ../POTCAR .
        sed -i "/NBANDS/s/.*/NBANDS =    $nbands/" INCAR
        sed -i "/KPAR/d" INCAR
	echo "AMIN   =    0.01" >> INCAR 
        mpirun  -np $SLURM_NTASKS $EXEC/vasp_std  > result
        cd ../
done

