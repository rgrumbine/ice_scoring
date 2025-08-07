#You need to issue this by hand before using the makefile:
#	module load NetCDF

#Details of the paths are set for theia
#Denise Worthen, Robert Grumbine 17 May 2018

#On theia/hera/orion:
#opt = -Dcice_file
#settings = -I /home/Robert.Grumbine/rgdev/mmablib/mmablib/include -L /home/Robert.Grumbine/rgdev/mmablib/mmablib/
#settings = -I ../../mmablib/include -L ../../mmablib/

#On wcoss:
opt = 
settings = -I /u/robert.grumbine/rgops/mmablib/include -L /u/robert.grumbine/rgops/mmablib/

#On Mac:
#opt = 
#BASE=/Volumes/ncep/github.work/mmablib/
#settings=-I $(BASE)/include -L $(BASE) 
#NETCDF=/Users/rmg3/usrlocal/

all : twelfth_osisaf_north twelfth_osisaf_south ufs_osisaf_north ufs_osisaf_south generic_osisaf
#all : generic score_diag score_nsidc nsidc_nsidc score_cfsv2 persistence score_cice_inst

ufs_osisaf_north : ufs_osisaf.C
	g++ $(opt) -DOSISAF_POLE=osisaf_north -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

ufs_osisaf_south : ufs_osisaf.C
	g++ $(opt) -DOSISAF_POLE=osisaf_south -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

twelfth_osisaf_north : twelfth_osisaf.C
	g++ $(opt) -DOSISAF_POLE=osisaf_north -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

twelfth_osisaf_south : twelfth_osisaf.C
	g++ $(opt) -DOSISAF_POLE=osisaf_south -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

generic_osisaf : generic_osisaf.C
	g++ $(opt) -DOSISAF_POLE=osisaf_north -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_cfsv2 : score_v_cfsv2.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

nsidc_nsidc : nsidc_v_nsidc.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_nsidc : score_v_nsidc.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_diag : score_diag.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

persistence : persistence.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

generic : generic.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_cice_inst : score_cice_inst.C 
	g++ $(opt) -DLINUX -Wall -O2 $< -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)
