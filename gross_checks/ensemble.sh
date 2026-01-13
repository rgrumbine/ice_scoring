#!/bin/sh

#Model specific names of grid specifications are in 2nd argument (cice.header here)
#Model variable names and their bounds are in ctl/icesubset.high (here)
#'beta' is an optional argument, useful when bounds are unknown but variable names are

source ./nest
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions
export level=extreme


# For a single date:
tag=20201231
yy=`echo $tag | cut -c1-4`
mm=`echo $tag | cut -c5-6`

#ice: 
#time python3 ensemble.py $HOME/clim_data/ep6/gefs.${tag}/ cice.header ctl/gefs_ice.$level gamma > bout.$yy.$mm

#ocean: 
time python3 ensemble.py $HOME/clim_data/ep6/gefs.${tag}/ gefs_ocean.header ctl/ufs_ocean.$level gamma > bout.$yy.$mm

exit

# Looping over an experiment set:
yy=1994
while [ $yy -le 2023 ] 
#while [ $yy -le 1994 ] 
do
  #for mm in 05 11
  for mm in 11 
  do
    tag=${yy}${mm}01
    #time python3 ensemble.py $HOME/clim_data/sfs/gefs.${tag}/ cice.header ctl/sfs.199611 gamma > bout.$yy.$mm
    time python3 ensemble.py $HOME/clim_data/ep6/gefs.${tag}/ cice.header ctl/sfs.199611 gamma > bout.$yy.$mm
  done
  yy=`expr $yy + 1`
done
