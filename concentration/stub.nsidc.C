// set fname outside
////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from nsidc netcdf:
  nsidcnorth<float> obs;
  grid2<float> tmp(obs.ypoints(), obs.xpoints());

  nsidcnorth<float> obs_cdr, obs_nt, obs_bt;
  grid2<float> obslat(obs.ypoints(), obs.xpoints()), obslon(obs.ypoints(), obs.xpoints());

  grid2<float> tmp_cdr(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_nt(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_bt(obs_cdr.ypoints(), obs_cdr.xpoints());


  int ncid, varid;
  int retval;

  unsigned char *xb;
  double *xd;

  xb = (unsigned char*) malloc(sizeof(unsigned char)*obs.xpoints()*obs.ypoints() );
  xd = (double*) malloc(sizeof(double)*obs.xpoints()*obs.ypoints() );

////////////////// Sea ice analysis ///////////////////////////////
  retval = nc_open(fname, NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

  retval = nc_inq_varid(ncid, "latitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, xd);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslat, xd);

  retval = nc_inq_varid(ncid, "longitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, xd);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslon, xd);

  retval = nc_inq_varid(ncid, "seaice_conc_cdr", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp, xb);
  enter(tmp_cdr, xb);

  retval = nc_inq_varid(ncid, "goddard_bt_seaice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp_bt, xb);
  //printf("have bt concentration\n"); fflush(stdout);

  retval = nc_inq_varid(ncid, "goddard_nt_seaice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp_nt, xb);
  //printf("have nt concentration\n"); fflush(stdout);



// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

///////////////////////////////////////////////////////////////////////
