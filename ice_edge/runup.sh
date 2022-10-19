#!/bin/sh

. ./bootstrap.sh

dy=1
while [ $dy -le 8 ]
do
  echo working on $dy day lead

  #time python3 dy_score.py 20190301 $dy > /dev/null
  time python3 dy_score.py 20190301 $dy 

  mkdir nic_v_nic.$dy; mv score.?.20* nic_v_nic.$dy

  dy=`expr $dy + 1`
done

