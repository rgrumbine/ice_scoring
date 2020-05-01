// Netcdf inc and utility:
#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 *  * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

// Bringing in to mmablib from netcdf:
void enter(grid2<float> &param, float *x) ;
void enter(grid2<float> &param, double *x) ;
void enter(grid2<float> &param, float *x, float scale) ;
void enter(mvector<float> &param, float *x) ;

// vector of values:
void enter(mvector<float> &param, float *x) {
  int loc;
  for (loc = 0 ; loc < param.xpoints(); loc++) {
    if (x[loc] > 1e20) x[loc] = 0;
    param[loc] = x[loc];
  }
  return;
}
// nsidc
void enter(grid2<float> &param, double *x) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    if (x[loc.i+ param.xpoints()*loc.j] > 1e20) x[loc.i+ param.xpoints()*loc.j] = 0;
    param[loc] = (float) x[loc.i+ param.xpoints()*loc.j];
  }
  }
  #ifdef DEBUG
  printf("stats: %f %f %f %f\n",param.gridmax(), param.gridmin(), param.average(), param.rms() );
  fflush(stdout);
  #endif

  return;
}
// rtofs, analysis
void enter(grid2<float> &param, float *x) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    if (x[loc.i+ param.xpoints()*loc.j] > 1e20) x[loc.i+ param.xpoints()*loc.j] = 0;
    param[loc] = x[loc.i+ param.xpoints()*loc.j];
  }
  }
  #ifdef DEBUG
  printf("stats: %f %f %f %f\n",param.gridmax(), param.gridmin(), param.average(), param.rms() );
  fflush(stdout);
  #endif

  return;
}
//nrl
void enter(grid2<float> &param, float *x, float scale) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    //if (x[loc.i+ param.xpoints()*loc.j] > 1e20) x[loc.i+ param.xpoints()*loc.j] = 0;
    if (x[loc.i+ param.xpoints()*loc.j] < -20000. ) x[loc.i+ param.xpoints()*loc.j] = 0;
    param[loc] = x[loc.i+ param.xpoints()*loc.j] * scale  ;
  }
  }
  #ifdef DEBUG
  printf("stats: %f %f %f %f\n",param.gridmax(), param.gridmin(), param.average(), param.rms() );
  fflush(stdout);
  #endif

  return;
}
