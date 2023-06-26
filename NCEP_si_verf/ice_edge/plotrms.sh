#!/bin/sh

#Find and plot the rmse for ice edge matchups
# Robert Grumbine 10 January 2023

cd $HOME/noscrub/model_intercompare/edge.eval

#For the persistence scores:
cd persist

for d in 1 2 3 4 5 6 7 8 10 16 365
do
  for pole in n s
  do
    if [ ! -f  $pole.$d ] ; then
      grep rms nic_v_nic.$d/score.${pole}.* > $pole.$d
    fi
  done
done

. $HOME/rgdev/toolbox/python_load.wcoss2

for d in 1 2 3 4 5 6 7 8 10 16
do
  python3 edge_rmse_series_plot.py  s.$d $d SH >> souts
  python3 edge_rmse_series_plot.py  n.$d $d NH >> nouts
done

scp -p edge_rmse_*.png  seaice@emcrzdm.ncep.noaa.gov:/home/www/polar/experimental/ice_edge/nic_v_nic/
