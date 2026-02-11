#!/bin/sh 

export PYTHONPATH=$HOME/rgdev/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions

echo zzz module list
module list

set -x

export level=extreme
export cyc=00

#for f in 20241210 20241211 20241212
f=20251121
while [ $f -le 20260211 ]
do
  tag=$f
  #yy=`echo $f | cut -c1-4`
  #mm=`echo $f | cut -c5-6`
  #dd=`echo $f | cut -c7-8`
  #j=0
  #if [ -d $modelout/gdas.$tag ] ; then
  #  for fhr in 003 006 009
  #  do
  #      time python3 $GDIR/universal2d.py \
  #             $modelout/gdas.$tag/$cyc/model/ice/history/gdas.ice.t${cyc}z.inst.f${fhr}.nc \
  #             cice.header \
  #             $GDIR/ctl/sfs.199611 redone \
  #             > gdas.cice.${f}.$level.$fhr.results
  #  done
  #fi
  if [ -d $modelout/gfs.$tag ] ; then
    #for fhr in 006 012 
    fhr=006
    while [ $fhr -le 384 ]
    do
      time python3 $GDIR/universal2d.py \
             $modelout/gfs.$tag/${cyc}/model/ice/history/gfs.t${cyc}z.6hr_avg.f${fhr}.nc \
             cice.header \
             $GDIR/ctl/sfs.199611 redone \
             > gfs.cice.${f}.$level.$fhr.results
      fhr=`expr $fhr + 6`
      if [ $fhr -le 100 ] ; then
	fhr=0$fhr
      fi
    done
  fi

  f=`expr $f + 1`
  f=`$HOME/bin/dtgfix3 $f`
done

model=ufs
cat ${model}.cice.*.results > all.$model
for lead in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 
do
  fhr=`expr $lead \* 24 + 6`
  if [ $fhr -lt 10 ] ; then
    fhr=00$fhr
  elif [ $fhr -lt 100 ] ; then
    fhr=0$fhr
  fi

  cat ${model}.cice.*.$level.$fhr.results > all.${model}.$fhr
done

#model=gdas
#cat ${model}.cice.*.results > all.$model
#for fhr in 003 006 009
#do
#  cat ${model}.cice.*.$level.$fhr.results > all.${model}.$fhr
#done
