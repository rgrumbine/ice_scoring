#!/bin/sh
# Wcoss2
#PBS -N trial
#PBS -o trial
#PBS -j oe
#PBS -q "dev"
#PBS -A ICE-DEV
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=1

# gaeac5
#SBATCH -J yrexpt
#SBATCH -e yrexpt%j.err
#SBATCH -o yrexpt%j.out
#SBATCH --partition=batch
#SBATCH --account=nggps_emc
#SBATCH --clusters=c5
#SBATCH --time=5:59:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

#----------------------------------------------------------------------------

cd $HOME/rgdev/ice_scoring/NCEP_si_verf/evolve/
# gaea or wcoss2
source ~/env3.12/bin/activate

module load intel netcdf imagemagick

# args are CICE testid, number of experiments, and concentration cutoff
time python3 year_cice.py gx1_5 30 0.15
