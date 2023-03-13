#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in aice albsni congel divu evap_ai fhocn_ai flat_ai flwdn flwup_ai frazil fresh_ai frzmlt fsalt_ai fsens_ai fswabs fswabs_ai fswdn fswthru_ai hi hs meltb meltl meltt opening rain_ai snoice snow snow_ai sss sst strcorx strcory strength strocnx strocny Tair Tsfc uocn uvel vocn vvel
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
  wc ${f}.s
done

