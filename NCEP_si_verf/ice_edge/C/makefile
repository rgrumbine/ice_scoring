#find edge requires a grid type in the compilation.
#  global_12th is the high resolution analysis
#Robert Grumbine 15 May 2018

#cice needs the netcdf module as well
#  module load NetCDF

#opts = -Wall -O2 -DLINUX -DDEBUG
ccopts = -Wall -O2 -DLINUX
mmabopts = -I ../../formats -I ../../../mmablib/include ../../../mmablib/libombf_4.a 
opts = $(ccopts) $(mmabopts)

finds = find_edge_ncep find_edge_ims find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south

all: cscore_edge $(finds)

ncopts=-I $(NETCDF)/include -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS)

#--------
cscore_edge : score_edge.C
	$(CC) $< $(opts) -l imf -o $(@)


find_edge_ims : find_edge_ims.C
	$(CC) $< $(opts) -o $(@)

find_edge_cfsv2 : find_edge_cfsv2.C
	$(CC) $< $(opts) -o $(@)

find_edge_nrl : find_edge_nrl.C
	$(CC) $< $(opts) $(ncopts) -o $(@)

find_edge_ncep : find_edge.C
	$(CC) -DGRIDTYPE=global_12th $< $(opts) -o $(@)

find_edge_nsidc_north : find_edge_nsidc.C
	$(CC) -Dnsidc_north $< $(opts) $(ncopts) -o $(@)

find_edge_nsidc_south : find_edge_nsidc.C
	$(CC) -Dnsidc_south $< $(opts) $(ncopts) -o $(@)

find_edge_consortium : find_edge_consortium.C
	$(CC) -Dbenchmark $< $(opts) $(ncopts) -o $(@)

find_edge_cice : find_edge_cice.C
	$(CC) $< $(opts) $(ncopts) -limf -lirc -o $(@)


install :
	mv cscore_edge find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_ims find_edge_ncep find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south ../../../exec 
