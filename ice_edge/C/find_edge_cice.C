#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent cell
// Netcdf CICE output from RTOFS
// Robert Grumbine 21 May 2018 


// RG: This should really detect NX, NY from the netcdf file, obviating
//       the kludge here
#ifdef cice_file
// cice on hycom quarter degree tripolar grid
  #define NX 1500
  #define NY 1099
#elif benchmark
// cice on mom6 quarter degree tripolar grid
  #define NX 1440
  #define NY 1080 
#else
// hycom twelfth degree tripolar grid
  #define NX 4500
  #define NY 3297
#endif

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
// Get skip file data:
  fin = fopen(argv[1], "r");
  if (fin == (FILE*) NULL) {
    printf("find_edge_cice failed to open input file %s\n",argv[1]);
    return 1;
  }
  skip.binin(fin);
  fclose(fin);
  #ifdef DEBUG
  printf("skip stats %d %d %d %d \n", skip.gridmax(), skip.gridmin(), skip.average(), skip.rms());
    fflush(stdout);
  #endif

// Read in netcdf information from rtofs/cice
  float *x;
  int ncid, varid;
  int retval;
  x = (float*) malloc(sizeof(float)*NX*NY);

  retval = nc_open(argv[2], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

// Get vars:
  retval = nc_inq_varid(ncid, "TLAT", &varid);
  if (retval != 0) ERR2(retval, "TLAT");
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR2(retval, "TLAT");fflush(stdout);
  enter(lat, x);

  retval = nc_inq_varid(ncid, "TLON", &varid);
  if (retval != 0) ERR2(retval, "TLAT");
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR2(retval, "TLAT");fflush(stdout);
  enter(lon, x);

  retval = nc_inq_varid(ncid, "tarea", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tarea, x);

  retval = nc_inq_varid(ncid, "hi_h", &varid);
  //consortium retval = nc_inq_varid(ncid, "hi", &varid);
  if (retval != 0) ERR2(retval, "hi_h");
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR2(retval, "hi_h");fflush(stdout);
  enter(ice_thickness, x);

  retval = nc_inq_varid(ncid, "aice_h", &varid);
  //consortium retval = nc_inq_varid(ncid, "aice", &varid);
  if (retval != 0) ERR2(retval, "aice_h");
  retval = nc_get_var_float(ncid, varid, x);
  if (retval != 0) ERR2(retval, "aice_h");fflush(stdout);
  enter(conc, x);
  #ifdef DEBUG
  printf("conc stats in find_edge %f %f\n",conc.gridmax(), conc.gridmin() );
  #endif

/////////////////////////////////////////////////////////////////////////////
// Look for ice edge, defined by a concentration tolerance / critical value

  float conc_toler = atof(argv[3]);
  #ifdef DEBUG
  printf("conc_toler = %f\n",conc_toler);
  #endif

  edge_finder(conc, lat, lon, conc_toler);

  return 0;
}
