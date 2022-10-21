#!/bin/sh
#PBS -N edge8.persist
#PBS -o edge8.persist
#PBS -j oe
#PBS -A ICE-DEV
#PBS -q dev
#PBS -l walltime=6:00:00
#PBS -l select=1:ncpus=1

pid=$$
mkdir /lfs/h2/emc/ptmp/wx21rg/nicedge.$pid
cd /lfs/h2/emc/ptmp/wx21rg/nicedge.$pid

#cd $HOME/rgdev/edge.eval/

. $HOME/rgdev/ice_scoring/ice_edge/bootstrap.sh

dy=8
#while [ $dy -le 8 ]
#do
  echo working on $dy day lead

  #time python3 dy_score.py 20190301 $dy > /dev/null
  time python3 dy_score.py 20190301 $dy 

  mkdir nic_v_nic.$dy; mv score.?.20* nic_v_nic.$dy

#  dy=`expr $dy + 1`
#done
