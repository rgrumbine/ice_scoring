#!/bin/sh 
#
## WCOSS2 27 July 2023
#module load intel-classic/2022.2.0.262
#module load PrgEnv-intel/8.3.3
#module load netcdf/4.7.4
#module load wgrib2/2.0.8

## Ursa 13 April 2026
## ursa:
module load intel-oneapi-compilers
module load hpc-x/2.18.1-icc
module load netcdf-c/4.9.2
module load netcdf-fortran/4.6.1
export NETCDF=$NETCDF_C_ROOT

make -i
