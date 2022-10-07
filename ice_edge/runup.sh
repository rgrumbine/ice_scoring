#!/bin/sh

. ./bootstrap.sh

dy=1
while [ $dy -le 1 ]
do
  echo working on $dy day lead

  #time python3 dy_score.py 20190301 $dy > /dev/null
  time python3 dy_score.py 20190301 $dy 

  mkdir $dy; mv score.?.20* $dy

  dy=`expr $dy + 1`
done

