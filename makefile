clean :
	find . -name '*.o' -exec rm {} \;

distclean :
	find . -name '*.o' -exec rm {} \;
	rm -r exec
	rm fix
