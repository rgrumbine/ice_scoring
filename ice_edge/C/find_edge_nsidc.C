#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent cell
// Netcdf CICE output from RTOFS, UFS CICE (benchmark), NSIDC
// Robert Grumbine 21 May 2018 


#ifdef cice_file
// cice on hycom quarter degree tripolar grid
  #define NX 1500
  #define NY 1099
#elif benchmark
// cice on mom6 quarter degree tripolar grid
  #define NX 1440
  #define NY 1080 
#elif nsidc_north
// NSIDC CDR NH grid:
  #define NX 304
  #define NY 448 
#elif nsidc_south
// NSIDC CDR SH grid:
  #define NX 316
  #define NY 332 
#else
// hycom twelfth degree tripolar grid
  #define NX 4500
  #define NY 3298
#endif

#include "small_nc.C"
#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
// metric grid of some kind
  global_12th<unsigned char> skip;
// rtofs:
  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> conc(NX, NY), tarea(NX, NY);

  FILE *fin;

// /////////////////////////////////////////////////////////////////////////////
// Read in netcdf information 
  float *x;
  double *dx;
  int ncid, varid;
  int retval;

  x = (float*) malloc(sizeof(float)*NX*NY);
  dx = (double*) malloc(sizeof(double)*NX*NY);

  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

// Get vars:
  retval = nc_inq_varid(ncid, "latitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, dx);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lat, dx);

  retval = nc_inq_varid(ncid, "longitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, dx);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lon, dx);

  retval = nc_inq_varid(ncid, "seaice_conc_cdr", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(conc, x);

/////////////////////////////////////////////////////////////////////////////
// Look for ice edge, defined by a concentration tolerance / critical value

  float conc_toler = atof(argv[2]);
  edge_finder(conc, lat, lon, conc_toler);

  return 0;
}
