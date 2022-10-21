#!/bin/sh

module load python/3.6.3

date
for hh in 024 048 072 096 120 144 168 192
do
  python3 rtofs3d.py data/rtofs_glo_3dz_f${hh}_daily_3ztio.nc ctl/rtofs3zt.extremes a > ztio.f${hh}
done
exit
date
#parm=ice
#parm=prog
#parm=diag
for parm in ice prog diag
do
  n=000
  #while [ $n -le 2 ]
  while [ $n -le 24 ]
  do
    if [ -f data/rtofs_glo_2ds_n${n}_${parm}.nc ] ; then 
      python3 rtofs.py data/rtofs_glo_2ds_n${n}_${parm}.nc ctl/rtofs${parm}.extremes a > n.${n}.$parm
      n=`expr $n + 1`
      if [ $n -lt 10 ] ; then
        n=00$n
      else
        n=0$n
      fi
    fi
  done

  f=000
  #while [ $f -le 3 ]
  while [ $f -le 192 ]
  do
    if [ -f data/rtofs_glo_2ds_f${f}_${parm}.nc ] ; then 
      python3 rtofs.py data/rtofs_glo_2ds_f${f}_${parm}.nc ctl/rtofs${parm}.extremes a > f.${f}.$parm
      f=`expr $f + 3`
      if [ $f -lt 10 ] ; then
        f=00$f
      elif [ $f -lt 100 ] ; then
        f=0$f
      fi
    fi
  done

  date
done
