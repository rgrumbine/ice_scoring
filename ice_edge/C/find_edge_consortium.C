#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent cell
// Netcdf CICE output from RTOFS
// Robert Grumbine 21 May 2018 
// Netcdf CICE output from CICE6 consortium gx1
// Robert Grumbine 11 Aug 2021


#define NX 320
#define NY 384

#include "small_nc.C"
#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
// metric grid of some kind
  global_12th<unsigned char> skip;
// rtofs:
  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> conc(NX, NY), ice_thickness(NX, NY), tarea(NX, NY);

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

// Read in netcdf information from CICE (Consortium)
  float *x;
  int ncid, varid;
  int retval;
  x = (float*) malloc(sizeof(float)*NX*NY);

  retval = nc_open(argv[2], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

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

  retval = nc_inq_varid(ncid, "tarea", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(conc, x);

  retval = nc_inq_varid(ncid, "hi", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(ice_thickness, x);

  retval = nc_inq_varid(ncid, "aice", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(conc, x);

/////////////////////////////////////////////////////////////////////////////
// Look for ice edge, defined by a concentration tolerance / critical value

  float conc_toler = atof(argv[3]);
  edge_finder(conc, lat, lon, conc_toler);

  return 0;
}
