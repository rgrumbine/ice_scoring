#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in SST speed SSU SSV SSH SSS ePBL MLD_003 MLD_0125 taux tauy latent sensible SW LW LwLatSens evap lprec fprec lrunoff Heat_PmE
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
  wc ${f}.s
done

