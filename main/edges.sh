#!/bin/bash -login
#SBATCH -J edge_all
#SBATCH -o edge_all.out
#SBATCH -e edge_all.err
#SBATCH -t 7:55:00
#  #SBATCH -t 0:25:00
#SBATCH -q batch
#SBATCH -A marine-cpu
#  #SBATCH -A fv3-cpu
#SBATCH -N 1
#SBATCH --mail-type FAIL
#SBATCH --mail-user USER@system

#Hera:
source /etc/profile.d/modules.csh
module load intel/2020.2
module load impi/2020.2
module load netcdf/4.7.0
module load wgrib2/2.0.8

module use -a /contrib/anaconda/modulefiles
module load anaconda/latest 

module list

set -x

export USER=$user
echo HOME=$HOME
cd $HOME/clim_data/edges/

#Orion
#  tbd
#WCOSS
#  tbd

export EXBASE=$HOME/rgdev/ice_scoring/

export mmablib=$HOME/rgdev/mmablib/
#
echo pre-pythonpath $PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$mmablib/py:$HOME/rgdev/ice_scoring/main
echo post-pythonpath $PYTHONPATH

export XDG_RUNTIME_DIR=/scratch1/NCEPDEV/climate/${USER}/runtime
export MPLCONFIGDIR=/scratch1/NCEPDEV/climate/${USER}/runtime

export expt=edges
export EXDIR=$HOME/clim_data/edges
export RUNBASE=/scratch1/NCEPDEV/stmp2/${USER}/prototype_evaluations/${expt}.verf

#export FCST_BASE=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/ 

#All systems:

if [ ! -d $RUNBASE ] ; then
  mkdir -p -m 700 $RUNBASE
fi
if [ ! -d $EXDIR ] ; then
  mkdir -p -m 700 $EXDIR
fi
cd     $EXDIR
export base=`pwd`


echo env $FCST_BASE $EXDIR $base $RUNBASE

cp $HOME/rgdev/ice_scoring/main/obs_edges_verf.py .

# Fewer changes below here -------------------------------------------------

#For batch python graphics
if [ ! -d $XDG_RUNTIME_DIR ] ; then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
fi
echo $XDG_RUNTIME_DIR for python graphic support

export x=`date`
echo start of loop at dtime $x
export fcst_len=1

python3 obs_edges_verf.py 20150101 20180331 


export x=`date`
echo end of $expt forecast verification at $x
