#include <stdio.h>
#include <stdlib.h>
//Robert Grumbine
//8 June 2018

#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

#include "ALL.C"

void get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &hi);

int main(int argc, char *argv[]) {
  FILE *fin;

  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> aice(NX, NY), hi(NX, NY);

  global_12th<float> obs;
  global_12th<unsigned char> skip;

// Get observations and the global skip mask:
  fin = fopen(argv[1], "r");
  obs.binin(fin);
  fclose(fin);
  //printf("obs stats %f %f %f %f\n",obs.gridmax(), obs.gridmin(), obs.average(), obs.rms() );

  // get skip mask
  fin = fopen(argv[2], "r");
  skip.binin(fin);
  fclose(fin);
  //printf("skip stats %d %d %d %d\n",skip.gridmax(), skip.gridmin(), skip.average(), skip.rms() );


///////// NETCDF gets ///////////////////////////////////////////
  get_nc(argv[3], lat, lon, aice, hi);

////////////////////////////////////////////////////////
// Start scoring:
  FILE *fout;
  global_12th<unsigned char> nh, sh;
  ijpt loc;
  latpt ll;

  fout = fopen(argv[4],"w");

  fprintf(fout, "global stats\n");
  scoring(fout, aice, lat, lon, obs);
  scoring(fout, aice, lat, lon, obs, skip, 0.0);
  scoring(fout, aice, lat, lon, obs, skip, 0.05);
  scoring(fout, aice, lat, lon, obs, skip, 0.15);
  scoring(fout, aice, lat, lon, obs, skip, 0.50);
  scoring(fout, aice, lat, lon, obs, skip, 0.70);
  scoring(fout, aice, lat, lon, obs, skip, 0.88);
  scoring(fout, aice, lat, lon, obs, skip, 0.94);
  nh = skip;
  sh = skip;
  #ifdef DEBUG
  int n = 0, s = 0;
  for (loc.j = 0; loc.j < nh.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < nh.xpoints(); loc.i++) {
    ll = nh.locate(loc);
    if (ll.lat > 0) {
      sh[loc] = 1;
      s++;
    }
    else {
      nh[loc] = 1;
      n++;
    }
  }
  }
  printf("n,s = %d %d\n",n,s);
  #endif

  fprintf(fout, "nh stats\n");
  scoring(fout, aice, lat, lon, obs, nh, 0.0);
  scoring(fout, aice, lat, lon, obs, nh, 0.05);
  scoring(fout, aice, lat, lon, obs, nh, 0.15);
  scoring(fout, aice, lat, lon, obs, nh, 0.50);
  scoring(fout, aice, lat, lon, obs, nh, 0.70);
  scoring(fout, aice, lat, lon, obs, nh, 0.88);
  scoring(fout, aice, lat, lon, obs, nh, 0.94);

  fprintf(fout, "sh stats\n");
  scoring(fout, aice, lat, lon, obs, sh, 0.0);
  scoring(fout, aice, lat, lon, obs, sh, 0.05);
  scoring(fout, aice, lat, lon, obs, sh, 0.15);
  scoring(fout, aice, lat, lon, obs, sh, 0.50);
  scoring(fout, aice, lat, lon, obs, sh, 0.70);
  scoring(fout, aice, lat, lon, obs, sh, 0.88);
  scoring(fout, aice, lat, lon, obs, sh, 0.94);

  fclose(fout);

  return 0;
}

void  get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &hi) {
  float *x;
  int ncid, varid;
  int retval;
  x = (float*) malloc(sizeof(float)*lat.xpoints()*lat.ypoints());

//tlat, tlon, aice, hi
  retval = nc_open(fname, NC_NOWRITE, &ncid); if (retval != 0) ERR(retval);

// go over all variables:
  retval = nc_inq_varid(ncid, "TLAT", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lat, x);

  retval = nc_inq_varid(ncid, "TLON", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lon, x);

  retval = nc_inq_varid(ncid, "aice", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(aice, x);

  retval = nc_inq_varid(ncid, "hi", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(hi, x);

// close when done:
  retval = nc_close(ncid); if (retval != 0) ERR(retval);

  return;
}
