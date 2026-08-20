#!/bin/sh 

source $HOME/env3.12/bin/activate

export PYTHONPATH=$HOME/rgops/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/gross
export MODDEF=$HOME/rgdev/ice_scoring/gross/model_definitions/

echo zzz moddef $MODDEF
echo zzz module list
module list

set -x

export level=extreme
#export base=202411
#for d in 16 17 18 19 20 21 22 23 24
f=20241116
while [ $f -le 20241207 ]
do
  #f=$base$d
  tag=$f
  j=0
  #gdas -- 3d fields only
  #for fhr in 003 006 009
  #do
  #  
  #done

  #gfs
  fhr=006
  while [ $fhr -le 240 ]
  do
    time python3 $GDIR/universal2d.py \
           $modelout/gfs.$f/00/model/ocean/history/gfs.ocean.t00z.6hr_avg.f${fhr}.nc \
	   ufs_ocean.header \
           $GDIR/ctl/ufs_ocean.$level redone \
         > gfs.ocean.${f}.$level.$fhr.results
    fhr=`expr $fhr + 6`
    if [ $fhr -lt 100 ] ; then
      fhr=0$fhr
    fi
  done

  f=`expr $f + 1`
  f=`$HOME/bin/dtgfix3 $f`
done

cat gfs.ocean.*.results > all.gfs
#cat gdas.ocean.*.results > all.gdas
#cat all.gfs all.gdas > all
#cp all.gfs all
