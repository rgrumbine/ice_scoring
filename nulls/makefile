
main : main.C nulls.C nulls.h
	g++ -c -Wall -O2 -DLINUX -I ../../mmablib/include -I ~/usrlocal/include main.C 
	g++ main.o  ../../mmablib/libombf_4.a -o $(@)

