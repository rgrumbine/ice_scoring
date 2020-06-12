#!/bin/bash

SH=/bin/bash
export base=`pwd`

if [ ! -d exec ] ; then
  mkdir -p exec
fi
export EXDIR=`pwd`/exec

if [ ! -f ../mmablib/libombf_4.a ] ; then
  cd ../mmablib
  make
fi

#netcdf:
module load ips/18.0.5.274
module load impi/18.0.1
module load NetCDF/4.5.0

#ice_edge : 
cd ${base}/ice_edge/C
make
mv cscore_edge find_edge find_edge_ims find_edge_cfsv2 find_edge_cice find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south ${EXDIR}

#integrals:
cd ${base}/integral
make
mv solo_ncep solo_ims solo_nsidc binary ${EXDIR}

#Concentration:
cd ${base}/concentration
make
mv score_diag score_nsidc score_cfsv2 persistence ${EXDIR}


