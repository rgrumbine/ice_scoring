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
#source /etc/profile.d/modules.csh
module load intel/2022.1.2
module load impi/2022.1.2
module load netcdf/4.7.0
module load wgrib2/2.0.8

module use -a /contrib/anaconda/modulefiles
module load anaconda/latest 

module list

set -x
#set -e

#Hera:
export USER=$USER
#debug: echo zzz HOME=$HOME
cd $HOME/clim_data/edges/

#Orion
#  tbd
#WCOSS
#  tbd

export EXBASE=$HOME/rgdev/ice_scoring/
export mmablib=$HOME/rgdev/mmablib/
#
#debug: echo zzz pre-pythonpath $PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$mmablib/py:$HOME/rgdev/ice_scoring/NCEP_si_verf/main_dir
#debug: echo zzz post-pythonpath $PYTHONPATH

export XDG_RUNTIME_DIR=/scratch1/NCEPDEV/climate/${USER}/runtime
export MPLCONFIGDIR=/scratch1/NCEPDEV/climate/${USER}/runtime

export expt=edges
export EXDIR=$HOME/clim_data/edges
export RUNBASE=/scratch1/NCEPDEV/stmp2/${USER}/hr1/${expt}

export FCST_BASE=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_hr1/SeaIce/ 

#All systems:

if [ ! -d $RUNBASE ] ; then
  mkdir -p -m 700 $RUNBASE
fi
if [ ! -d $EXDIR ] ; then
  mkdir -p -m 700 $EXDIR
fi
cd     $EXDIR
export base=`pwd`

#debug: echo zzz env $FCST_BASE $EXDIR $base $RUNBASE

cp $HOME/rgdev/ice_scoring/NCEP_si_verf/main_dir/obs_edges_verf.py .
#cp $HOME/rgdev/ice_scoring/NCEP_si_verf/main_dir/statview.py .

# Fewer changes below here -------------------------------------------------

#For batch python graphics
if [ ! -d $XDG_RUNTIME_DIR ] ; then
  mkdir -p -m 700 $XDG_RUNTIME_DIR
fi
echo $XDG_RUNTIME_DIR for python graphic support

export x=`date`
#debug: echo zzz start of loop at dtime $x
export fcst_len=15

#python3 -m cProfile -o statsout obs_edges_verf.py 20110401 20180331 $fcst_len 
#python3 statview.py statsout > stats.evaluation 

for initial in 20191203 20191206 20191209 20191212 20191215 20191218 20191221 20191224 20191227 20191230 20200102 20200105 20200108 20200111 20200114 20200117 20200120 20200123 20200126 20200129 20200201 20200204 20200207 20200210 20200213 20200216 20200219 20200222 20200225 20200601 20200604 20200607 20200610 20200613 20200616 20200619 20200622 20200625 20200628 20200701 20200704 20200707 20200710 20200713 20200716 20200719 20200722 20200725 20200728 20200731 20200803 20200806 20200809 20200812 20200815 20200818 20200821 20200824 20200827 20200830
do
  python3 obs_edges_verf.py $FCST_BASE $initial $fcst_len 
done

export x=`date`
echo zzz end of $expt forecast verification at $x
