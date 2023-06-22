#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in uvel_h vvel_h hi_h hs_h Tsfc_h aice_h mlt_onset_h frz_onset_h
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
done
wc *.s | sort -n

