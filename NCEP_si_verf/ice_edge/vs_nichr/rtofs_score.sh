#!/bin/sh

cd $HOME/rgdev/edges/rtofs_scores

. ~/rgdev/toolbox/misc/python_load.wcoss2

for crit in 00 01 15 03 05 10
do
  for lead in 0 1 2 3 4 5 6 7 8
  do
    #if [ ! -f rtofs_rms.${lead}.${crit} ] ; then
      grep rms *.$lead.*0.$crit > rtofs_rms.${lead}.${crit}
    #fi
    python3 $HOME/rgdev/edges/rtofs_edge_rmse_plot.py  rtofs_rms.${lead}.${crit} $lead crit_$crit
  done
done
