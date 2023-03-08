#!/bin/sh

set -x

export DCOM=~/rgdev/edges
cd $DCOM

. $HOME/rgdev/ice_scoring/NCEP_si_verf/ice_edge/vs_nichr/bootstrap.sh

yy=2022
ddd=250

if [ ! -d cleaned ] ; then
  mkdir cleaned
fi
if [ ! -d first ] ; then
  mkdir first
fi

export tag=${yy}${ddd}

while [ $tag -le `date +"%Y%j"` ] 
do
  if [ ! -f cleaned/n.${yy}${ddd}.beta ] ; then
    if [ -f ${DCOM}/nedge_${yy}${ddd} ] ; then
      python3 nic_parse.py ${DCOM}/nedge_${yy}${ddd} > n.${yy}${ddd}
      grep -v '[a-z]' n.${yy}${ddd} > n.${yy}${ddd}.beta
    elif [ -f ${DCOM}/${yy}/nedge_${yy}${ddd} ] ; then
      python3 nic_parse.py ${DCOM}/${yy}/nedge_${yy}${ddd} > n.${yy}${ddd}
      grep -v '[a-z]' n.${yy}${ddd} > n.${yy}${ddd}.beta
    else
      echo could not find nedge_${yy}${ddd}
    fi
  fi

  if [ ! -f cleaned/s.${yy}${ddd}.beta ] ; then
    if [ -f ${DCOM}/sedge_${yy}${ddd} ] ; then
      python3 nic_parse.py ${DCOM}/sedge_${yy}${ddd} > s.${yy}${ddd}
      grep -v '[a-z]' s.${yy}${ddd} > s.${yy}${ddd}.beta
    elif [ -f ${DCOM}/${yy}/sedge_${yy}${ddd} ] ; then
      python3 nic_parse.py ${DCOM}/${yy}/sedge_${yy}${ddd} > s.${yy}${ddd}
      grep -v '[a-z]' s.${yy}${ddd} > s.${yy}${ddd}.beta
    else
      echo could not find sedge_${yy}${ddd}
    fi
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

  export tag=${yy}${ddd}
done

mv [ns].*.beta cleaned
mv [ns].${yy}??? first
