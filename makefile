distclean :
	rm fix
	rm -r exec
	find . -name '*.o' -exec rm {} \;
