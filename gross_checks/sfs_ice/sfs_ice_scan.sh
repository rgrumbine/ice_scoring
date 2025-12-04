#!/bin/sh 

# ursa, WCOSS2
export PYTHONPATH=$HOME/rgdev/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/
export MODDEF=$HOME/rgdev/ice_scoring/model_definitions
# gaea c6
export PYTHONPATH=$HOME/rg6/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/
export MODDEF=$HOME/rg6/ice_scoring/model_definitions

echo zzz module list
module list

set -x

export level=extreme
export cyc=00

tag=20231101
#yy=`echo $tag | cut -c1-4`
#mm=`echo $tag | cut -c5-6`
#dd=`echo $tag | cut -c7-8`
#j=0

if [ -d $modelout ] ; then
  #for fhr in 006 012 
  fhr=024
  while [ $fhr -le 8784 ]
  do
    time python3 $GDIR/universal2d.py \
           $modelout/sfs.t${cyc}z.tripolar.f${fhr}.nc \
           cice.header \
           $GDIR/sfs.199611 redone \
           > gfs.cice.${f}.$level.$fhr.results
    fhr=`expr $fhr + 24`
    if [ $fhr -le 100 ] ; then
      fhr=0$fhr
    fi
  done
fi

cat gfs.cice.*.results > all.gfs

