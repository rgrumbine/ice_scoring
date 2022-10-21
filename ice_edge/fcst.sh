#!/bin/sh

. ./bootstrap.sh

dy=60
while [ $dy -le 80 ]
do
  time  $EXDIR/cscore_edge $FIXDIR/seaice_alldist.bin rtofs.edge.f24.v20220305.15  cleaned/n.20220$dy.beta 50. > n.0$dy
  dy=`expr  $dy + 1`
done
