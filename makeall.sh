#!/bin/bash

SH=/bin/bash
export base=`pwd`

# --------------  System-dependent modules/paths/... here --------
#WCOSS2-cactus
module load PrgEnv-intel/8.1.0
module load intel/19.1.3.304
module load netcdf/4.7.4
module load python/3.8.6

#libjpeg/9c           netcdf/4.7.4  (D)    w3emc/2.9.1      (D)
#cfitsio/3.2.40        grib_util/1.2.2 (D)    libpng/1.6.37        perl/5.32.0          w3emc/2.9.2
#crtm/2.3.0            grib_util/1.2.3        libtiff/4.1.0        pigz/2.3.4           w3nco/2.4.1
#curl/7.72.0           grib_util/1.2.4        libxml2/2.9.10       pixman/0.40.0        wgrib2/2.0.7
#g2/3.4.1              gsl/2.7                libxmlparse/2.0.0    proj/7.1.0           wgrib2/2.0.8_wmo (D)
#g2/3.4.4              hdf5/1.10.6            libxrender/0.9.10    python/3.8.6 

 

##netcdf -- WCOSS 3.0
#module load ips/19.0.5.281
#module load impi/19.0.5
#module load NetCDF/4.5.0
#module load python/3.6.3

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
#module purge
#module load intel
#module load cray-mpich
#module load cray-netcdf
#module load PrgEnv-intel
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
