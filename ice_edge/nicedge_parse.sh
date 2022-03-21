#!/bin/sh

yy=2019
ddd=077

while [ $yy -le 2023 ]
do
  if [ -f nedge_${yy}${ddd} ] ; then
    python3 nic_parse.py nedge_${yy}${ddd} > n.${yy}${ddd}
    grep -v '[a-z]' n.${yy}${ddd} > n.${yy}${ddd}.beta
  fi
  if [ -f sedge_${yy}${ddd} ] ; then
    python3 nic_parse.py sedge_${yy}${ddd} > s.${yy}${ddd}
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
