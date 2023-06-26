#!/bin/bash
# --- Hera
#SBATCH -J hr1
#SBATCH -e hr1.err
#SBATCH -o hr1.out
#SBATCH -t 5:55:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user robert.grumbine@noaa.gov
# --- Hera


#--- WCOSS2
##PBS -N ufs_ice_eval
##PBS -o ufs_ice_eval
##PBS -j oe
##PBS -A ICE-DEV
##PBS -q hera
##PBS -l walltime=4:00:00
##PBS -l select=1:ncpus=1
#--- WCOSS2


#. $HOME/rgdev/toolbox/misc/python_load.wcoss2
. $HOME/rgdev/toolbox/misc/python_load.hera


#------------------------ General across platforms --------------
set -x

#export start=20210701
#export end=20210930

export MODEL=ufs_ice
export level=extremes
#export modelout=$HOME/clim_data/rtofs_gross
export modelout=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/

export GDIR=$HOME/rgdev/ice_scoring/gross_checks/

export PYTHONPATH=$PYTHONPATH:$GDIR/shared

if [ ! -d $HOME/scratch/gross/$MODEL ] ; then
  mkdir -p  $HOME/scratch/gross/$MODEL
  if [ $? -ne 0 ] ; then
    echo zzz could not create rundir  $HOME/scratch/gross/$MODEL
    exit 1
  fi
fi 
cd  $HOME/scratch/gross/$MODEL

ln -sf $GDIR/curves curves
time $GDIR/$MODEL/${MODEL}_scan.sh

# Now that all results have been scanned, check for errors:

# For plots, last number is dot size. Expect fewer pts as go down list, 
#    so make pts larger
python3 $GDIR/graphics/plot_errs.py all all 2.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/physical.exceptions all > nonphysical
python3 $GDIR/graphics/plot_errs.py nonphysical nonphysical 4.

python3 $GDIR/exceptions/exceptions.py $GDIR/exceptions/known.errors nonphysical > unknown
python3 $GDIR/graphics/plot_errs.py unknown unknown 8.

$GDIR/$MODEL/split.sh unknown | sort -n
