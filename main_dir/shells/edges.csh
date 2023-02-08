#!/bin/csh -f
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

set -x

setenv USER $user
echo HOME=$HOME

#Orion
#  tbd
#WCOSS
#  tbd

#Hera:
source /etc/profile.d/modules.csh
module load intel/2020.2
module load impi/2020.2
module load netcdf/4.7.0
module load wgrib2/2.0.8
cd $HOME/clim_data/edges/

setenv mmablib $HOME/rgdev/mmablib/
#
module use -a /contrib/anaconda/modulefiles
module load anaconda/latest 

echo pre-pythonpath $PYTHONPATH
setenv PYTHONPATH $PYTHONPATH:$mmablib/py:$HOME/ice_scoring/main
echo post-pythonpath $PYTHONPATH

setenv XDG_RUNTIME_DIR /scratch1/NCEPDEV/climate/${USER}/runtime
setenv MPLCONFIGDIR    /scratch1/NCEPDEV/climate/${USER}/runtime

setenv expt edges
setenv EXDIR     $HOME/clim_data/edges
setenv RUNBASE   /scratch1/NCEPDEV/stmp2/${USER}/prototype_evaluations/${expt}.verf

#setenv FCST_BASE /scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/ 

#All systems:
module list

if ( ! -d $RUNBASE ) then
  mkdir -p -m 700 $RUNBASE
endif
if ( ! -d $EXDIR ) then
  mkdir -p -m 700 $EXDIR
endif
cd     $EXDIR
setenv base `pwd`


echo env $FCST_BASE $EXDIR $base $RUNBASE

cp $HOME/ice_scoring/main/obs_edges_verf.py .

# Fewer changes below here -------------------------------------------------

#For batch python graphics
if ( ! -d $XDG_RUNTIME_DIR ) then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
endif
echo $XDG_RUNTIME_DIR for python graphic support

setenv x `date`
echo start of loop at dtime $x
setenv fcst_len 1

python3 obs_edges_verf.py 


setenv x `date`
echo end of $expt forecast verification at $x
