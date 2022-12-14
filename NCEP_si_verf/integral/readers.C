#include "small_nc.C"

// Reading in concentrations:
template<class T>
int reader(metricgrid<T> &conc, FILE *fin) ;

int reader(psgrid<float> &conc, psgrid<float> &lat, psgrid<float> &lon, FILE *fin) ;

int reader(grid2<float> &lat, grid2<float> &lon, grid2<float> &conc, 
           grid2<float> &thick, int ncid) ;
int reader(mvector<float> &lat, mvector<float> &lon, grid2<float> &conc, 
           grid2<float> &thick, int ncid) ;

// IMS or NCEP analysis
template <class T>
int reader(metricgrid<T> &conc, FILE *fin) {
  conc.binin(fin);
  #ifdef DEBUG
    printf("nx ny = %d %d\n",conc.xpoints(), conc.ypoints() );
    printf("max min etc. %f %f %f %f\n",conc.gridmax(), conc.gridmin(), 
                conc.average(), conc.rms() );
    fflush(stdout);
  #endif
  return 0;
}
// NSIDC grids by hemisphere:
int reader(psgrid<float> &conc, psgrid<float> &lat, psgrid<float> &lon, FILE *fin) {
  float *x;
  double *dx;
  grid2<double> tmpx(lat.xpoints(), lat.ypoints());
  int varid, ncid, retval;
  x = new float[conc.xpoints()*conc.ypoints()];
  dx = new double[conc.xpoints()*conc.ypoints()];
  retval = nc_inq_varid(ncid, "latitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, dx);
  enter(lat, dx);

  retval = nc_inq_varid(ncid, "longitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, dx);
  enter(lon, dx);

  retval = nc_inq_varid(ncid, "concentration", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  enter(conc, x);

  delete x;
  delete dx;
  fflush(stdout);
  return 0;
}
//rtofs reading
int reader(grid2<float> &lat, grid2<float> &lon, grid2<float> &conc, grid2<float> &thick, int ncid) {
  float *x;
  int varid;
  int retval;
  x = (float*) malloc(sizeof(float)*conc.xpoints()*conc.ypoints() );

// Get vars:
  retval = nc_inq_varid(ncid, "TLAT", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lat, x);

  retval = nc_inq_varid(ncid, "TLON", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lon, x);

  retval = nc_inq_varid(ncid, "aice", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(conc, x);

  retval = nc_inq_varid(ncid, "hi", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(thick, x);

  return 0;
}
//gofs/acnfs reading
int reader(mvector<float> &lat, mvector<float> &lon, grid2<float> &conc, grid2<float> &thick, int ncid) {
  float *x;
  int varid;
  int retval;
  x = (float*) malloc(sizeof(float)*conc.xpoints()*conc.ypoints() );
// Get vars:
  retval = nc_inq_varid(ncid, "lat", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lat, x);

  retval = nc_inq_varid(ncid, "lon", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lon, x);

  retval = nc_inq_varid(ncid, "aice", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(conc, x, 1.e-4); // scale_factor

  retval = nc_inq_varid(ncid, "hi", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(thick, x, 1.e-3);

  return 0;
}
