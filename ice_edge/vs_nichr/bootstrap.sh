#!/bin/sh

# execute this as . ./bootstrap.sh

module load craype PrgEnv-intel intel
module load python
module load netcdf

export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/ice_scoring/ice_edge
export EXDIR=$HOME/rgdev/ice_scoring/exec
export FIXDIR=$HOME/rgdev/fix/
export OBSDIR=$HOME/rgdev/edges

base=$HOME/rgdev/ice_scoring/ice_edge
for f in bootstrap.sh dy_score.py nic_parse.py nicedge_parse.sh runup.sh rtofs.py
do
	if [ ! -f $f ] ; then
          cp -p $base/$f .
	fi
done

