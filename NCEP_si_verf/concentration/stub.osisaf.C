// set fname outside

# include "ncepgrids.h"

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from osisaf netcdf:
  OSISAF_POLE<float> obs;
  OSISAF_POLE<float> obs_cdr, obs_nt, obs_bt;

  grid2<float> tmp(obs.ypoints(), obs.xpoints());
  grid2<float> obslat(obs.ypoints(), obs.xpoints());
  grid2<float> obslon(obs.ypoints(), obs.xpoints());

  grid2<float> tmp_cdr(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_nt(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_bt(obs_cdr.ypoints(), obs_cdr.xpoints());

  int ncid, varid;
  int retval;

  short int *xb;
  float *xd;

  xb = (short int*) malloc(sizeof(short int)*obs.xpoints()*obs.ypoints() );
  xd = (float*) malloc(sizeof(float)*obs.xpoints()*obs.ypoints() );

////////////////// Sea ice analysis ///////////////////////////////
  //debug: printf("opening osisaf\n"); fflush(stdout);
  retval = nc_open(fname, NC_NOWRITE, &ncid);
  if (retval != 0) {
    printf("failed to open %s\n",fname);
    ERR(retval);
  }
  //debug: printf("retval = %d\n",retval);

  //debug: printf("trying to read lat\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "lat", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, xd);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslat, xd);

  //debug: printf("trying to read lon\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "lon", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, xd);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslon, xd);

  //debug: printf("trying to read ice_conc\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "ice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_short(ncid, varid, xb);
  if (retval != 0) {
    printf("failed to read in ice_conc\n");
    printf("retval = %d\n",retval); fflush(stdout);
    ERR(retval);
  }
  enter(tmp, xb);
  enter(tmp_cdr, xb);

// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

///////////////////////////////////////////////////////////////////////
