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

#ncopts=-I $(NETCDF)/include -L $(NETCDF)/lib -lnetcdf $(HDF5_LINK_OPTS)
ncopts=-I $(NETCDF)/include -L $(NETCDF)/lib -lnetcdf -lm

#--------
find_edge_nrl : find_edge_nrl.C
	$(CXX) $< $(opts) $(ncopts) -o $(@)

find_edge_nsidc_north : find_edge_nsidc.C
	$(CXX) -Dnsidc_north $< $(opts) $(ncopts) -o $(@)

find_edge_nsidc_south : find_edge_nsidc.C
	$(CXX) -Dnsidc_south $< $(opts) $(ncopts) -o $(@)

find_edge_consortium : find_edge_consortium.C
	$(CXX) -Dbenchmark $< $(opts) $(ncopts) -o $(@)

find_edge_cice : find_edge_cice.C
	#$(CXX) $< $(opts) $(ncopts) -limf -lirc -o $(@)
	$(CXX) $< $(opts) $(ncopts) -o $(@)

# Don't use netcdf:
cscore_edge : score_edge.C
	#$(CXX) $< $(opts) -l imf -o $(@)
	$(CXX) $< $(opts) -o $(@)

find_edge_ims : find_edge_ims.C
	$(CXX) $< $(opts) -o $(@)

find_edge_cfsv2 : find_edge_cfsv2.C
	$(CXX) $< $(opts) -o $(@)

find_edge_ncep : find_edge.C
	$(CXX) -DGRIDTYPE=global_12th $< $(opts) -o $(@)


install :
	mv cscore_edge find_edge_cfsv2 find_edge_cice find_edge_consortium find_edge_ims find_edge_ncep find_edge_nrl find_edge_nsidc_north find_edge_nsidc_south ../../../exec 
