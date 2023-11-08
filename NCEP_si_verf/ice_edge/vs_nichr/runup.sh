#!/bin/sh
#PBS -N edge.persist
#PBS -o edge.persist
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=3:00:00
#PBS -l select=1:ncpus=1

cd $HOME/rgdev/edges/

. $HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge/vs_nichr/bootstrap.sh

# For persistence scoring, NIC vs. NIC
./nicedge_parse.sh

for dy in 1 2 3 4 5 6 7 8 10 16 365
do
  echo working on $dy day lead
  time python3 dy_score.py 20230101 $dy 
done
./nic_plot_this_year.sh

# For rtofs scoring (needs nicedge_parse.sh to have run, bt doesn't need 
#   the others between there and here
# Find rtofs edges and score them
time python3 rtofs.py
# Produce graphics (relies on rtofs_edge_rmse.py)
echo zzz make rtofs score graphics
time ./rtofs_score.sh

