#!/bin/sh 

#Hera:
echo zzz HOME = $HOME
export PYTHONPATH=$HOME/rgdev/mmablib/py:$HOME/rgdev/ice_scoring/gross_checks/
export MODDEF=$HOME/rgdev/ice_scoring/gross/model_definitions

echo zzz module list
module list

set -x

export level=extreme

for f in 2023041712
do
  tag=$f
  j=0
  for fhr in 003 004 005 006 007 008 009
  do
      time python3 $GDIR/universal2d.py \
             $modelout/sfcf${fhr}.nc \
             ufs_atm.header \
             $GDIR/$MODEL/first_try redone.$fhr \
             > atm.${f}.$level.$fhr.results
  done

done

cat atm.*.results > all
