#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent cell
// Netcdf CICE output from RTOFS
// Netcdf CICE output from NRL (ACNFS/GOFS 3.1)
// Robert Grumbine 21 May 2018 

#define NX 4500
#define NY 1251

#include "small_nc.C"
#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
// metric grid of some kind
  global_12th<unsigned char> skip;
// NRL:
  mvector<float> lat(NY), lon(NX);
  grid2<float> conc(NX, NY), ice_thickness(NX, NY);
//netcdf:
  float *x;
  int ncid, varid;
  int retval;

  FILE *fin;

// /////////////////////////////////////////////////////////////////////////////
// Get data:
  fin = fopen(argv[1], "r");
  skip.binin(fin);
  fclose(fin);
  #ifdef DEBUG
    printf("skip stats %d %d %d %d \n", skip.gridmax(), skip.gridmin(), skip.average(), skip.rms());
    fflush(stdout);
  #endif

// Read in netcdf information from rtofs
  x = (float*) malloc(sizeof(float)*NX*NY);

  retval = nc_open(argv[2], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

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
  enter(ice_thickness, x, 1.e-3);

/////////////////////////////////////////////////////////////////////////////
  float conc_toler = atof(argv[3]);
  edge_finder(conc, lat, lon, conc_toler);

  return 0;
}
