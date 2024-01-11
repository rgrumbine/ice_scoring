#!/bin/bash

SH=/bin/bash
export base=`pwd`

# --------------  System-dependent modules/paths/... here --------
##netcdf -- WCOSS 3.0
#module load PrgEnv-intel/8.3.3
#module load intel-classic/2022.2.0.262
#module load netcdf/4.7.4
#module load geos
#module load proj
#module load python/3.8.6

##netcdf -- orion
#module load intel/2020   #, 2020
#module load impi/2020    #, 2020
#module load netcdf/4.7.4 #4.7.2-parallel, pnetcdf/1.12.0
#python

#netcdf -- Hera -- update 20221006
module load intel/2022.1.2
module load impi/2022.1.2
module load netcdf/4.7.0
module use -a /contrib/anaconda/modulefiles
module load anaconda/latest

##netcdf -- Gaea
#module load intel
#module load PrgEnv-intel
#module load cray-mpich
#module load cray-hdf5
#module load cray-netcdf
#export NETCDF=$NETCDF_DIR
#export PATH=/ncrc/home1/Robert.Grumbine/anaconda3/bin:$PATH

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
mv cscore_edge find_edge_ims find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_ncep find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south ${EXDIR}

#integrals:
cd ${base}/integral
make
mv cice_solo solo_ncep solo_ims solo_nsidc binary ${EXDIR}

#Concentration:
cd ${base}/concentration
make
mv generic score_cice_inst score_diag score_nsidc score_cfsv2 persistence nsidc_nsidc ${EXDIR}


#Check condition of python3 and libraries
cd ${base}
echo python3 is in `which python3`
python3 main_dir/checkenv.py
