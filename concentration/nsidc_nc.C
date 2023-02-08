// Extract nsidc netcdf file management to its own file
// -- deal more readily with changes like between v3 and v4

#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}


#include "ALL.C"

template <class T>
void slices_enter(grid2<float> *param, T *x) ;

void nsidc_get(char *fname, psgrid<float> &obs) ;

////////////////////////////////////////////////////////////////////////
template <class T>
void slices_enter(grid2<float> *param, T *x) {
  ijpt loc;
  int i, nx, ny;
  nx = param[0].xpoints();
  ny = param[0].ypoints();
  for (i = 0; i < 35; i++) {
  for (loc.j = 0; loc.j < ny; loc.j++) {
  for (loc.i = 0; loc.i < nx; loc.i++) {
    if (x[loc.i+ nx*loc.j+i*nx*ny] > 1e20) x[loc.i+ nx*loc.j+i*nx*ny] = 0;
    param[i].operator[](loc) = x[loc.i+ nx*loc.j + i*nx*ny];
  }
  }
  printf("%d stats: %f %f %f %f\n",i, param[i].gridmax(), param[i].gridmin(), param[i].average(), param[i].rms() );
  }

  return;
}
void nsidc_get(char *fname, psgrid<float> &obs) {
  int ncid, varid;
  int retval;
  fijpt floc, sloc;
  latpt ll;
// High res sea ice analysis from netcdf:
  grid2<float> obslat(obs.ypoints(), obs.xpoints()), obslon(obs.ypoints(), obs.xpoints());
  grid2<float> tmp(obs.ypoints(), obs.xpoints());

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

// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

////////////////// Latlon check and transfer ///////////////////////////////
  obs.set((float) 157.0);
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    ll.lat = obslat[i];
    ll.lon = obslon[i];
    floc = obs.locate(ll);
    obs[floc] = tmp[i];
    //printf("%6d %.3f %.3f  %3.0f  %.3f %.3f  %f %f\n",i,
    //    obslat[i], obslon[i], tmp[i], floc.i, floc.j, 
    //        fabs(floc.i - rint(floc.i)) , fabs(floc.j - rint(floc.j) ) );
  }
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    if (obs[i] == 157.0) {
      printf("failed to update %d\n",i);
    }
  }
  if (obs.gridmax() > 1.0) obs /= 100.;

  fflush(stdout);
  return;
}
