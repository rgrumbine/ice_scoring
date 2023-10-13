
ncopts =-I $(NETCDF)/include -L $(NETCDF)/lib -lnetcdf

ccopts = -Wall -O2 -DLINUX
mmabopts = -I ../formats -I ../../mmablib/include ../../mmablib/libombf_4.a

opts = $(ccopts) $(mmabopts) $(ncopts)


all : cice_solo solo_ncep solo_ims solo_nsidc binary

cice_solo : cice_solo.C readers.C
	$(CC) $< -DCICE $(opts) -o $(@)

solo_nsidc : solo.C readers.C
	$(CC) $< -DNSIDC $(opts) -o $(@)

solo_ncep : solo.C readers.C
	$(CC) $< -DNCEP $(opts) -o $(@)

solo_ims : solo.C readers.C
	$(CC) $< -DIMS $(opts) -o $(@)

binary : binary.C readers.C
	$(CC) $< $(opts) -o $(@)
