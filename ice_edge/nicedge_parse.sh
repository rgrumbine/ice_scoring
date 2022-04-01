#!/bin/sh

export DCOM=~/rgdev/edges
module load ips/19.0.5.281 python/3.6.3 lsf/10.1 HPSS/5.0.2.5 
module load NetCDF/4.5.0 impi/19.0.5


yy=2019
ddd=077

while [ $yy -le 2023 ]
do
  if [ -f ${DCOM}/nedge_${yy}${ddd} ] ; then
    python3 nic_parse.py ${DCOM}/nedge_${yy}${ddd} > n.${yy}${ddd}
    grep -v '[a-z]' n.${yy}${ddd} > n.${yy}${ddd}.beta
  fi
  if [ -f ${DCOM}/sedge_${yy}${ddd} ] ; then
    python3 nic_parse.py ${DCOM}/sedge_${yy}${ddd} > s.${yy}${ddd}
    grep -v '[a-z]' s.${yy}${ddd} > s.${yy}${ddd}.beta
  fi

  ddd=`expr $ddd + 1`
  if [ $ddd -lt 10 ] ; then
    ddd=00$ddd
  elif [ $ddd -lt 100 ] ; then
    ddd=0$ddd
  fi
  if [ $ddd -gt 366 ] ; then
    yy=`expr $yy + 1`
    ddd=001
  fi  
done
