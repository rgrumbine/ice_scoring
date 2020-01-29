#!/bin/sh

#Bootstrap for ice model verification

BASE=/home/Robert.Grumbine/rgdev/mmablib/ice_scoring/

for f in verf_files.py setup_verf_ice.py contingency_plots.py all.csh
do
  cp ${BASE}/master/$f .
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done
for d in exec fix
do
  cp -rp ${BASE}/$d .
  if [ ! -d $d ] ; then
    echo could not find directory $d in $BASE, exiting
    exit 2
  fi
done


 
