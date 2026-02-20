#!/bin/bash
#--- WCOSS2
##PBS -N sfs_ice_eval
##PBS -o sfs_ice_eval
##PBS -j oe
##PBS -A ICE-DEV
##PBS -q hera
##PBS -l walltime=4:00:00
##PBS -l select=1:ncpus=1
#--- WCOSS2

# --- Ursa
#SBATCH -J hr5
#SBATCH -e hr5.err
#SBATCH -o hr5.out
#SBATCH -t 5:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov
# --- Hera


set -xe
#ursa: 
source /home/Robert.Grumbine/rg/env3.13/bin/activate
#wcoss2, gaea
#source $HOME/env3.12/bin/activate

#ursa:
export modelout=$HOME/clim_data/sfsbeta
#export modelout=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/
#export modelout=$HOME/scratch6/COMROOT/icein2/sfs.20231101/00/mem000/products/ice/netcdf/native

export modeltag=ufs
export MODEL=sfs_ice

#wcoss: export GDIR=$HOME/rgdev/ice_scoring/gross_checks/
#gaeac6:
#export GDIR=$HOME/rg6/ice_scoring/gross_checks/
#ursa: 
export GDIR=/home/Robert.Grumbine/rgdev/ice_scoring/gross_checks/

#wcoss:export SCRATCH=$HOME/scratch/gross
#gaeac6:
#export SCRATCH=$HOME/scratch6/gross
#ursa:
export SCRATCH=$HOME/scratch/gross

#------------------------ General across platforms --------------
set -x

export level=extremes

export PYTHONPATH=$PYTHONPATH:$GDIR/shared

if [ ! -d $SCRATCH/$modeltag ] ; then
  mkdir -p  $SCRATCH/$modeltag
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $SCRATCH/$modeltag
    exit 1
  fi
fi 
cd  $SCRATCH/$modeltag
ln -sf $GDIR/curves curves

set -x
for model in sfs_ice
do
  export MODEL=$model
  time $GDIR/$MODEL/${MODEL}_scan.sh
  # Now that all results have been scanned, check for errors:
  
  # For plots, last number is dot size. Expect fewer pts as go down list, 
  #    so make pts larger
  python3 $GDIR/graphics/plot_errs.py all all 12.
  mv all all.$MODEL
done
