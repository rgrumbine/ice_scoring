#!/bin/bash

SH=/bin/bash
export base=`pwd`

# --------------  System-dependent modules/paths/... here --------
##netcdf -- WCOSS 3.0
#module load ips/18.0.5.274
#module load impi/18.0.1
#module load NetCDF/4.5.0
#python

#netcdf -- orion
#module load intel/2020   #, 2020
#module load impi/2020    #, 2020
#module load netcdf/4.7.4 #4.7.2-parallel, pnetcdf/1.12.0
#python

#netcdf -- Hera
#module load intel/2020.2
#module load impi/2020.2
#module load netcdf/4.7.0 
#module use -a /contrib/anaconda/modulefiles
#module load anaconda/latest

#netcdf -- Gaea
module purge
module load intel
module load cray-mpich
module load cray-netcdf
module load PrgEnv-intel
export NETCDF=$NETCDF_DIR
export PATH=/ncrc/home1/Robert.Grumbine/anaconda3/bin:$PATH

# --------------  Should need no changes below here --------
module list

if [ ! -d exec ] ; then
  mkdir -p exec
fi
export EXDIR=`pwd`/exec

if [ ! -d ../mmablib ] ; then
  cd ..
  git clone https://github.com/rgrumbine/mmablib.git
  cd $base
fi

if [ ! -f ../mmablib/libombf_4.a ] ; then
  cd ../mmablib
  make
fi

#ice_edge : 
cd ${base}/ice_edge/C
make
mv cscore_edge find_edge find_edge_ims find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south ${EXDIR}

#integrals:
cd ${base}/integral
make
mv solo_ncep solo_ims solo_nsidc binary ${EXDIR}

#Concentration:
cd ${base}/concentration
make
mv generic score_diag score_nsidc score_cfsv2 persistence nsidc_nsidc ${EXDIR}


#Check condition of python3 and libraries
cd ${base}
echo python3 is in `which python3`
python3 main/checkenv.py
