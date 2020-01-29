#!/bin/sh

#For wcoss
module load python

#General:
export PYTHONPATH=/u/Robert.Grumbine/rgdev/mmablib/mmablib/py/
export SIDFEXdir=/u/Robert.Grumbine/rgdev/mmablib/ice_scoring/sidfex

if [ ! -d out ] ; then
  mkdir out
fi
if [ ! -f fcstin ] ; then
  echo no fcstin file
  exit 1
fi
if [ ! -f forecast.points ] ; then
  echo no forecast.points file 
  exit 2
fi

time python $SIDFEXdir/sidfex.py
exit

cd out
if [ ! -f uploaded ] ; then
  find . -type f -exec $SIDFEXdir/upload.sh {} \;
else
  find . -type f -newer uploaded -name 'nc*' -exec $SIDFEXdir/upload.sh {} \;
fi
touch uploaded
