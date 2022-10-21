#!/bin/sh

export MPLCONFIGDIR=/scratch2/NCEPDEV/climate/Robert.Grumbine/runtime 

yy=2018
for mo in 01 02 03 04 05 06 07 08 09 10 11 12
do
  for dd in 01 15
  do
    tag=${yy}${mo}${dd}
    python3 splice.py $tag  p3.1.figs/  p5.0.figs/ p6.0.figs persistence.figs/
  done
done
