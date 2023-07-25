#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent cell
// Netcdf CICE output from RTOFS, UFS CICE (benchmark), NSIDC
// Robert Grumbine 21 May 2018 


#ifdef nsidc_north
// NSIDC CDRv4 NH grid:
  #define NX 304
  #define NY 448 
#elif nsidc_south
// NSIDC CDRv4 SH grid:
  #define NX 316
  #define NY 332 
#endif

#include "small_nc.C"
#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
// metric grid of some kind
  global_12th<unsigned char> skip;
// model:
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

// Get ancillary vars:
  retval = nc_open(argv[3], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

  retval = nc_inq_varid(ncid, "latitude", &varid);
  if (retval != 0) ERR2(retval, "latitude");
  retval = nc_get_var_double(ncid, varid, dx);
  if (retval != 0) ERR2(retval, "latitude");fflush(stdout);
  enter(lat, dx);

  retval = nc_inq_varid(ncid, "longitude", &varid);
  if (retval != 0) ERR2(retval, "longitude");
  retval = nc_get_var_double(ncid, varid, dx);
  if (retval != 0) ERR2(retval, "longitude");fflush(stdout);
  enter(lon, dx);

// Get concentration vars
  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

// v3: seaice_conc_cdr
// v4: cdr_seaice_conc
  retval = nc_inq_varid(ncid, "cdr_seaice_conc", &varid);
  if (retval != 0) ERR2(retval, "cdr_seaice_conc");
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR2(retval, "cdr_seaice_conc");fflush(stdout);
  enter(conc, x);

/////////////////////////////////////////////////////////////////////////////
// Look for ice edge, defined by a concentration tolerance / critical value

  float conc_toler = atof(argv[2]);
  edge_finder(conc, lat, lon, conc_toler);

  return 0;
}
