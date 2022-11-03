#!/bin/sh
#Robert Grumbine

#module load python
module load intel
module load python/3.8.6

set -xe
export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/mmablib/py
echo zzz $PYTHONPATH

export GBASE=~/rgdev/ice_scoring/gross_checks
export PYTHONPATH=$PYTHONPATH:~/rgdev/ice_scoring/gross_checks/shared/
echo zzz $PYTHONPATH
export EXDIR=$GBASE/rtofs/
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions/

export OUTBASE=~/noscrub/model_intercompare/rtofs_cice/

#RTOFS CICE output

#RTOFS HYCOM output:
date
tag=`date +"%Y%m%d"`
tag=20221031

set +e
for parm in ice prog diag
do
  n=000
  #while [ $n -le 2 ]
  while [ $n -le 24 ]
  do
    if [ -f $OUTBASE/rtofs.$tag/rtofs_glo_2ds_n${n}_${parm}.nc ] ; then 
      python3 $EXDIR/rtofs.py $OUTBASE/rtofs.$tag/rtofs_glo_2ds_n${n}_${parm}.nc \
              ${GBASE}/ctl/rtofs${parm}.extremes a > n.${n}.$parm
    fi
    n=`expr $n + 1`
    if [ $n -lt 10 ] ; then
      n=00$n
    else
      n=0$n
    fi
  done

  f=000
  #while [ $f -le 3 ]
  while [ $f -le 192 ]
  do
    if [ -f $OUTBASE/rtofs.${tag}/rtofs_glo_2ds_f${f}_${parm}.nc ] ; then 
      python3 $EXDIR/rtofs.py $OUTBASE/rtofs.${tag}/rtofs_glo_2ds_f${f}_${parm}.nc \
                       ${GBASE}/ctl/rtofs${parm}.extremes a > f.${f}.$parm
    fi
    f=`expr $f + 1`
    if [ $f -lt 10 ] ; then
      f=00$f
    elif [ $f -lt 100 ] ; then
      f=0$f
    fi
  done

  date
done

exit
date
for hh in 024 048 072 096 120 144 168 192
do
  python3 $EXDIR/rtofs3d.py $OUTBASE/rtofs.${tag}/rtofs_glo_3dz_f${hh}_daily_3ztio.nc \
                     ${GBASE}/ctl/rtofs3zt.extremes a > ztio.f${hh}
done
exit
