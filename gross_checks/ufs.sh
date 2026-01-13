#!/bin/bash
#--- WCOSS2
##PBS -N ufs_ice_eval
##PBS -o ufs_ice_eval
##PBS -j oe
##PBS -A ICE-DEV
##PBS -q hera
##PBS -l walltime=4:00:00
##PBS -l select=1:ncpus=1
#--- WCOSS2

# --- Hera
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
#hera: source /home/Robert.Grumbine/rg/env3.12c/bin/activate
#wcoss2
source $HOME/env3.12/bin/activate

#export modelout=$HOME/clim_data/rtofs_gross
#export modelout=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/
export modelout=/lfs/h2/emc/global/noscrub/emc.global/RETRO_GFSv17/savefailedtest/retrotestgfs03/enkfgdas.2023041712/enkfgdasefcs015.2023041712/fcst.3647035
export modeltag=ufs
export MODEL=ufs_atm

export GDIR=$HOME/rgdev/ice_scoring/gross_checks/
#hera: export GDIR=/home/Robert.Grumbine/rgdev/ice_scoring/gross_checks/


#------------------------ General across platforms --------------
set -x

export level=extremes

export PYTHONPATH=$PYTHONPATH:$GDIR/shared

if [ ! -d $HOME/scratch/gross/$modeltag ] ; then
  mkdir -p  $HOME/scratch/gross/$modeltag
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$modeltag
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$modeltag
ln -sf $GDIR/curves curves

set -x
for model in ufs_atm ufs_ice
do
  export MODEL=$model
  time $GDIR/$MODEL/${MODEL}_scan.sh
  # Now that all results have been scanned, check for errors:
  
  # For plots, last number is dot size. Expect fewer pts as go down list, 
  #    so make pts larger
  python3 $GDIR/graphics/plot_errs.py all all 12.
  mv all all.$MODEL
done

