#!/bin/sh
#
# Robert Grumbine
# 9 Jun 2018


all : avg2 iabpcheck ifremercheck score iscore
CMD = avg2 iabpcheck ifremercheck score iscore
OBJS = avg2.o iabpcheck.o ifremercheck.o score.o iscore.o

#COPTS=-c -Wall -O2 -DLINUX -Weffc++
COPTS=-c -Wall -O2 -DLINUX 
IBASE=$(HOME)/rgops/mmablib/include
LBASE=$(HOME)/rgops/mmablib/
#CPP=g++
CPP=CC

#----------------------------------------------

%.o : %.C $(IBASE)/buoy.h
	$(CPP)  $(COPTS) -I $(IBASE)  $<


$(CMD) : $(OBJS) 
	$(CPP) $(@).o  $(LBASE)/libombf_4.a -o $(@) -lm

clean :
	rm *.o

distclean : clean 
	rm $(CMD)
