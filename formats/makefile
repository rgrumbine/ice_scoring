BASE=/usr1/
mmablib_ver=v3.4.3

#Robert Grumbine

all : ncread ncread2 

ncread2 : ncread2.F
	gfortran $< -I /usr/lib64/gfortran/modules/ -L /usr/lib64 -l netcdf -l netcdff -o $(@)
ncread : ncread.F
	gfortran $< -I /usr/lib64/gfortran/modules/ -L /usr/lib64 -l netcdf -l netcdff -o $(@)
	#ifort ncread.F -I/usrx/local/NetCDF/4.2/serial/include/ -L /usrx/local/NetCDF/4.2/serial/lib -lnetcdf -lnetcdff -o $(@)

