
opts = -Wall -O2 -DLINUX -I ../formats
NETCDF_INCLUDE=-I $(NETCDF)/include

all : solo_ncep solo_ims solo_nsidc binary

solo_nsidc : solo.C readers.C
	g++ -DNSIDC $(opts) $< $(NETCDF_INCLUDE) -I ../../mmablib/include ../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf -o $(@)

solo_ncep : solo.C readers.C
	g++ -DNCEP $(opts) $< $(NETCDF_INCLUDE) -I ../../mmablib/include ../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf -o $(@)

solo_ims : solo.C readers.C
	g++ -DIMS $(opts) $< $(NETCDF_INCLUDE) -I ../../mmablib/include ../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf -o $(@)

binary : binary.C readers.C
	g++ $(opts) $< $(NETCDF_INCLUDE) -I ../../mmablib/include ../../mmablib/libombf_4.a -L $(NETCDF)/lib -lnetcdf -o $(@)
