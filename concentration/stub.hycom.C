
// Hycom diag file variables of interest:
  grid2<float> lat(NX, NY), lon(NX, NY), tarea(NX, NY);

// Netcdf:
  float *x;
  int retval, ncid, varid;

////////////////// Hycom variables ///////////////////////////////

  x = (float*) malloc(sizeof(float)*NX*NY);

  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

// go over all variables:
  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "TLAT", &varid);
  #else
   retval = nc_inq_varid(ncid, "Latitude", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lat, x);

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "TLON", &varid);
  #else
   retval = nc_inq_varid(ncid, "Longitude", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lon, x);

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "tarea", &varid);
  #else
   retval = nc_inq_varid(ncid, "tarea", &varid);
  #endif

  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tarea, x);

  float *x35;
  x35 = (float*) malloc(35*lat.xpoints()*lat.ypoints()*sizeof(float) );

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "aice_h", &varid);
  #else
   retval = nc_inq_varid(ncid, "ice_coverage", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x35);
  if (retval != 0) ERR(retval);fflush(stdout);
  //enter(ice_coverage, x);
  slices_enter(&ice_coverage[0], x35);

// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);


