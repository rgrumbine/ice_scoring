#!/bin/sh

. python_load
export EXBASE=$HOME/rgdev/ice_scoring/
export FCST_BASE=/scratch1/NCEPDEV/climate/Lydia.B.Stefanova/Models/ufs_p8/SeaIce/
cd $EXBASE/main_dir

#set -xe
#set -e

#for yy in 2011
#for yy in 2012 2013 2014 2015 2016 2017 
#for yy in 2018
#do
#  #for mm in 04 05 06 07 08 09 10 11 12
#  #for mm in 01 02 03 04 05 06 07 08 09 10 11 12
#  for mm in 01 02 03
#  do
#    for dd in 01 15
#    do
#      start=${yy}${mm}${dd}
for start in 20160501 20160515 20160601 20160615 20160701 20160715 20160801 20160815 20160901 20160915 20161001 20161015 20161101 20161115 20161201 20161215 20170101 20170115 20170201 20170215 20170301 20170315 20170401 20170415 20170501 20170515 20170601 20170615 20170701 20170715 20170801 20170815 20170901 20170915 20171001 20171015 20171101 20171115 20171201 20171215
do
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
