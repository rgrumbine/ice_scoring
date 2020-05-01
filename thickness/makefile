#You need to issue this by hand before using the makefile:
#	module load NetCDF

#Details of the paths are set for theia
#Denise Worthen, Robert Grumbine 17 May 2018

#On theia:
#opt = -Dcice_file
#opt = -Dbenchmark 
settings = -I /home/Robert.Grumbine/rgdev/mmablib/mmablib/include -L /home/Robert.Grumbine/rgdev/mmablib/mmablib/
#On wcoss:
#opt = 
#settings = -I /u/Robert.Grumbine/rgdev/mmablib/mmablib/include -L /u/Robert.Grumbine/rgdev/mmablib/mmablib/
#On Mac:
#opt = 
#BASE=/Volumes/ncep/mmablib/mmablib/
#settings=-I $(BASE)/include -L $(BASE) 
#NETCDF=/Users/rmg3/usrlocal/

all : score_cryosat

score_cryosat : score_cryosat.C 
	g++ $(opt) -Dbenchmark -DLINUX -Wall -O2 $< -I$(NETCDF)/include \
           -L $(NETCDF)/lib $(settings) \
        -lombf_4 -lnetcdf -o $(@)

