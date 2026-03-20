#!/bin/sh
#Robert Grumbine

module load intel netcdf
module load prod_envir
#manage in scan.sh: module load python/3.8.6

set -xe
source $HOME/env3.12/bin/activate
export PYTHONPATH=$PYTHONPATH:$HOME/rgdev/mmablib/py
export PYTHONPATH=$PYTHONPATH:~/rgdev/ice_scoring/gross_checks/shared/
echo zzz $PYTHONPATH

export GBASE=~/rgdev/ice_scoring/gross_checks
export EXDIR=$GBASE/
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions/

export OUTBASE=$HOME/noscrub/model_intercompare/rtofs_cice/
#export OUTBASE=$COMROOT/rtofs/v2.4/

#RTOFS HYCOM output:
date
tag=`date +"%Y%m%d"`
tag=20250531
level=extreme

while [ $tag -ge 20250401 ]
do
  for parm in ice prog diag
  do
    n=000
    #while [ $n -le 2 ]
    while [ $n -le 24 ]
    do
      if [ -f $OUTBASE/rtofs.$tag/rtofs_glo_2ds_n${n}_${parm}.nc ] ; then 
        time python3 $EXDIR/universal2d.py \
  	      $OUTBASE/rtofs.$tag/rtofs_glo_2ds_n${n}_${parm}.nc \
  	      rtofs.global.def \
                ${GBASE}/ctl/rtofs${parm}.${level} a > ${model}.n.${n}.$tag.$parm.results
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
        time python3 $EXDIR/universal2d.py \
  	      $OUTBASE/rtofs.${tag}/rtofs_glo_2ds_f${f}_${parm}.nc \
                rtofs.global.def \
       	      ${GBASE}/ctl/rtofs${parm}.${level} a > ${model}.f.${f}.$tag.$parm.results
      fi
      f=`expr $f + 1`
      if [ $f -lt 10 ] ; then
        f=00$f
      elif [ $f -lt 100 ] ; then
        f=0$f
      fi
    done
  
    tag=`expr $tag - 1`
    tag=`$HOME/bin/dtgfix3 $tag`
    date
  done
done

exit


date
for hh in 024 048 072 096 120 144 168 192
do
  python3 $EXDIR/rtofs/rtofs3d.py $OUTBASE/rtofs.${tag}/rtofs_glo_3dz_f${hh}_daily_3ztio.nc \
                     ${GBASE}/ctl/rtofs3zt.${level} a > ${model}.ztio.f${hh}.results
done
