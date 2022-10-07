#find edge requires a grid type in the compilation.  
#  global_12th is the high resolution analysis
#Robert Grumbine 15 May 2018

#cice needs the netcdf module as well
#  module load NetCDF

#opts =  -Wall -O2 -DLINUX -DDEBUG
opts = -Wall -O2 -DLINUX -I ../../formats 
#for theia:
NETCDF_INCLUDE=-I $(NETCDF)/include

all: cscore_edge find_edge find_edge_ims find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south

cscore_edge : score_edge.C
	g++ $(opts) score_edge.C -I ../../../mmablib/include ../../../mmablib/libombf_4.a -l imf -o cscore_edge

find_edge_nsidc_north : find_edge_nsidc.C
	$(CC) $(opts) -Dnsidc_north $< $(NETCDF_INCLUDE) -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -o $(@)

find_edge_nsidc_south : find_edge_nsidc.C
	$(CC) -Dnsidc_south $(opts) $< $(NETCDF_INCLUDE) -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -o $(@)

find_edge_nrl : find_edge_nrl.C
	$(CC) $(opts) $< $(NETCDF_INCLUDE) -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -o $(@)

find_edge_consortium : find_edge_consortium.C
	$(CC) $(opts) $< $(NETCDF_INCLUDE) -Dbenchmark -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -o $(@)

find_edge_cice : find_edge_cice.C
	#$(CC) $(opts) $< $(NETCDF_INCLUDE) -Dbenchmark -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -o $(@)
	$(CC) $(opts) $< $(NETCDF_INCLUDE) -I ../../../mmablib/include ../../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS) -limf -lirc -o $(@)

find_edge_ims : find_edge_ims.C
	$(CC) $(opts) $< -I ../../../mmablib/include ../../../mmablib/libombf_4.a -o $(@)

find_edge_cfsv2 : find_edge_cfsv2.C
	$(CC) $(opts) $< -I ../../../mmablib/include ../../../mmablib/libombf_4.a -o $(@)

find_edge : find_edge.C
	$(CC) $(opts) -DGRIDTYPE=global_12th $< -I ../../../mmablib/include ../../../mmablib/libombf_4.a -o $(@)
