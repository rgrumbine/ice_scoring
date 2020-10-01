#!/bin/sh

#Bootstrap for ice model verification -- retrieve the scripts and fixed files for a basic run of the system
#Robert Grumbine
# 25 February 2020

BASE=${BASE:-/home/Robert.Grumbine/rgdev/ice_scoring/}

for f in contingency_plots.py 
do
  cp -p ${BASE}/concentration/$f .
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done

for f in verf_files.py setup_verf_ice.py platforms.py all.csh
do
  cp -p ${BASE}/master/$f .
  if [ ! -f $f ] ; then
    echo could not find $f in $BASE, exiting
    exit 1
  fi
done

#create and populate the exec directory if needed:
if [ ! -d ${BASE}/exec ] ; then
  cd ${BASE}
  ./makeall.sh
  if [ $? -eq 0 ] ; then
    echo copy exec dir from $BASE
  else
    echo failed to find or create execs, exiting now
    exit 1
  fi
fi

if [ ! -d ${BASE}/fix ] ; then
  echo You must manually create and populate the fix directory
  exit 1
fi

for d in exec fix
do
  cp -rp ${BASE}/$d .
  if [ ! -d $d ] ; then
    echo could not find directory $d in $BASE, exiting
    exit 2
  fi
done
