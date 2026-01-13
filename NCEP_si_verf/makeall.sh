#!/bin/bash

SH=/bin/bash
export base=`pwd`

# --------------  System-dependent modules/paths/... here --------
# Wcoss2
module load PrgEnv-intel
module load intel-classic
module load netcdf
module load geos
module load proj
module load python
source ~/env3.12/bin/activate

##netcdf -- orion
#module load intel/2020   #, 2020
#module load impi/2020    #, 2020
#module load netcdf/4.7.4 #4.7.2-parallel, pnetcdf/1.12.0
#python

#netcdf -- Hera -- update 20221006
#module load intel/2022.1.2
#module load impi/2022.1.2
#module load netcdf/4.7.0
#module use -a /contrib/anaconda/modulefiles
#module load anaconda/latest
#source ~/env3.7/bin/activate

#netcdf -- Gaea
#module load PrgEnv-cray
#module load cce/18.0.0
#module load cray-libsci/24.07.0
#module load cray-hdf5/1.14.3.1
#module load cray-netcdf/4.9.0.13
#export NETCDF=$NETCDF_DIR
#export PATH=/ncrc/home1/Robert.Grumbine/anaconda3/bin:$PATH
#source ~/env3.12/bin/activate

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

set -xe
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
python3 main_dir/check_pyenv.py
