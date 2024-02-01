#!/bin/sh

module load craype PrgEnv-intel intel
module load netcdf

. $HOME/rgdev/toolbox/misc/python_load.wcoss2

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge
export EXDIR=$HOME/rgdev/ice_scoring/exec
export FIXDIR=$HOME/rgdev/fix/
export OBSDIR=$HOME/rgdev/edges

base=$HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge/vs_nichr

python3 rtofs.py
