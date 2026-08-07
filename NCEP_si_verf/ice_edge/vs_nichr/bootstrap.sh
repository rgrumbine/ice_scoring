#!/bin/sh

# execute this as . ./bootstrap.sh
# Robert Grumbine 15 April 2026

##Wcoss
#module load craype PrgEnv-intel intel
#module load python
#module load netcdf
##ursa
source ~/rg/env3.13/bin/activate
module load intel-oneapi-compilers/2025.3.1  intel-oneapi-mpi/2021.17.1
module load netcdf-c/4.9.2 netcdf-fortran/4.6.1

# Shouldn't need changes below here

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge
export EXDIR=$HOME/rgdev/ice_scoring/NCEP_si_verf/exec
export OBSDIR=$HOME/rgdev/edges
export FIXDIR=$HOME/rg/alt.fix/

base=$HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge/vs_nichr

for f in bootstrap.sh dy_score.py nic_parse.py nicedge_parse.sh runup.sh rtofs.py edge_rmse_series_plot.py this_year.sh nic_plot_this_year.sh
do
	if [ ! -f $f ] ; then
          cp -p $base/$f .
	fi
done

