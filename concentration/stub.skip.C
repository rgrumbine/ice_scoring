  //fin = fopen(argv[1], "r");
////////////////// skip grid ///////////////////////////////
  global_12th<unsigned char> skip;

  if (fin != (FILE*) NULL) {
    skip.binin(fin);
    fclose(fin);
  }
  else {
    skip.set(0);
  }

  #ifdef DEBUG
    printf("skip stats %d %d %d %d \n", skip.gridmax(), skip.gridmin(), 
            skip.average(), skip.rms());
  #endif

