#You need to issue this by hand before using the makefile:
#	module load NetCDF

#Details of the paths are set for theia
#Denise Worthen, Robert Grumbine 17 May 2018

#opt = -DDEBUG -Dbenchmark 
opt = -Dbenchmark 

#On theia/hera/orion:
opt = -Dcice_file
#settings = -I /home/Robert.Grumbine/rgdev/mmablib/mmablib/include -L /home/Robert.Grumbine/rgdev/mmablib/mmablib/
settings = -I ../../mmablib/include -L ../../mmablib/
#On wcoss:
#opt = 
#settings = -I /u/Robert.Grumbine/para/mmablib/mmablib/include -L /u/Robert.Grumbine/para/mmablib/mmablib/
#On Mac:
#opt = 
#BASE=/Volumes/ncep/github.work/mmablib/
#settings=-I $(BASE)/include -L $(BASE) 
#NETCDF=/Users/rmg3/usrlocal/

all : score_diag score_nsidc score_cfsv2 persistence

score_cfsv2 : score_v_cfsv2.C 
	g++ $(opt) -DLINUX -Wall -O2 score_v_cfsv2.C -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_nsidc : score_v_nsidc.C 
	g++ $(opt) -DLINUX -Wall -O2 score_v_nsidc.C -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

score_diag : score_diag.C 
	g++ $(opt) -DLINUX -Wall -O2 $(@).C -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)

persistence : persistence.C 
	g++ $(opt) -DLINUX -Wall -O2 $(@).C -I$(NETCDF)/include -L $(NETCDF)/lib \
        $(settings) \
        -lombf_4 -lnetcdf -o $(@)
