#!/bin/sh

. python_load
export EXBASE=$HOME/rgdev/ice_scoring/NCEP_si_verf/
export FCST_BASE=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/
cd $EXBASE/main_dir

#set -xe
set -e

#for yy in 2012 2013 2014 2015 2016 2017 
for yy in 2018
do
  #for mm in 01 02 03 04 05 06 07 08 09 10 11 12
  for mm in 01 02 03
  do
    for dd in 01 15
    do
      start=${yy}${mm}${dd}
      valid=$start
      lead=0
      while [ $lead -lt 35 ]
      do
         python3 fcst_verf_ice.py $start $valid $FCST_BASE
         lead=`expr $lead + 1`
         valid=`expr $valid + 1`
         valid=`$HOME/bin/dtgfix3 $valid`
      done
    done
  done
done
