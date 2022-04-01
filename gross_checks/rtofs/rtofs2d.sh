#!/bin/sh

if [ $# -eq 1 ] ; then
  fname=$1
else
  echo need a file to work on
  exit 1
fi

for f in ice_coverage ice_temperature ice_thickness ice_uvelocity ice_vvelocity mixed_layer_thickness ssh sss sst surface_boundary_layer_thickness u_barotropic_velocity u_velocity v_barotropic_velocity v_velocity
do
  grep $f $fname | grep -v excessive | grep pm | sort -nr -k 6,6 > ${f}.s
  wc ${f}.s
done

