#You need to issue this by hand before using the makefile:
#	module load NetCDF

#Details of the paths are set for theia
#Denise Worthen, Robert Grumbine 17 May 2018

opt = -Dcice_file

#On theia:
#-I /home/Robert.Grumbine/save/mmab/include -L /home/Robert.Grumbine/save/mmab/
#On wcoss:
settings = -I /u/Robert.Grumbine/rgdev/mmablib/mmablib/include -L /u/Robert.Grumbine/rgdev/mmablib/mmablib/
#At RG Home
settings = -I /Users/rmg3/usrlocal/mmab/v3.5.0/include -L /Users/rmg3/usrlocal/mmab/v3.5.0
NETCDF= /Users/rmg3/usrlocal/

all : cice_seam hycom_seam hycom_seam_prog

cice_seam : cice_seam.C 
	g++ $(opt) -DLINUX -Wall -O2 $(@).C -I$(NETCDF)/include -L $(NETCDF)/lib \
	$(settings) \
        -lombf_4 -lnetcdf -o $(@)
hycom_seam : hycom_seam.C 
	g++ $(opt) -DLINUX -Wall -O2 $(@).C -I$(NETCDF)/include -L $(NETCDF)/lib \
	$(settings) \
        -lombf_4 -lnetcdf -o $(@)

hycom_seam_prog : hycom_seam_prog.C 
	g++ $(opt) -DLINUX -Wall -O2 $(@).C -I$(NETCDF)/include -L $(NETCDF)/lib \
	$(settings) \
        -lombf_4 -lnetcdf -o $(@)


