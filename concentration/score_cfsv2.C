#include <stdio.h>
#include <stdlib.h>

// Compute scores for the RTOFS-Global, netcdf outputs
// Robert Grumbine -- Hycom grid
// Denise Worthen -- Adding CICE grid

#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

#include "grid_math.h"
#include "ncepgrids.h"
template <class T>
void enter(grid2<float> &param, T *x) ;
template <class T>
void slices_enter(grid2<float> *param, T *x) ;

void nsidc_get(char *fname, psgrid<float> &obs) ;

#include "contingency_ptwise.C"

#ifdef cice_file
  #define NX 1500
  #define NY 1099
#elif benchmark
  #define NX 1440
  #define NY 1080 
#else
  #define NX 4500
  #define NY 3298
#endif

int main(int argc, char *argv[]) {
  float *x;
  int ncid, varid;
  int retval;
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  global_12th<unsigned char> skip;

// Hycom diag file variables of interest:
  grid2<float> lat(NX, NY), lon(NX, NY), tarea(NX, NY);
  //grid2<float> ice_coverage[35](NX, NY);
  grid2<float> *ice_coverage;

  x = (float*) malloc(sizeof(float)*NX*NY);

  ice_coverage = new grid2<float>[35];
  for (int i = 0; i < 35; i++) {
    ice_coverage[i].resize(NX, NY);
  }

  // for scoring matchups
  float level;
  double a11, a12, a21, a22;
  float pod, far, fcr, pct, ts, bias;
  int npts = lat.xpoints()*lat.ypoints();
  mvector<float> observed(npts), model(npts), cellarea(npts);
  mvector<unsigned char> skipped(npts), north(npts), south(npts);

////////////////// skip grid ///////////////////////////////
  //fin = fopen(argv[3], "r");
  //skip.binin(fin);
  //fclose(fin);
  skip.set(0);
  #ifdef DEBUG
  printf("skip stats %d %d %d %d \n", skip.gridmax(), skip.gridmin(), skip.average(), skip.rms()); 
  #endif

////////////////// Hycom variables ///////////////////////////////
  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

// go over all variables:
  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "TLAT", &varid);
  #else
   retval = nc_inq_varid(ncid, "Latitude", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lat, x);
  
  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "TLON", &varid);
  #else
   retval = nc_inq_varid(ncid, "Longitude", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(lon, x);

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "tarea", &varid);
  #else
   retval = nc_inq_varid(ncid, "tarea", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tarea, x);

  float *x35;
  x35 = (float*) malloc(35*lat.xpoints()*lat.ypoints()*sizeof(float) );

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "aice_h", &varid);
  #else
   retval = nc_inq_varid(ncid, "ice_coverage", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x35); 
  if (retval != 0) ERR(retval);fflush(stdout);
  //enter(ice_coverage, x);
  slices_enter(&ice_coverage[0], x35);
  
// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from nsidc netcdf:
  nsidcnorth<float> obs;
//  nsidc_get(argv[2], obs) ;
///////////////// End of Netcdf portion ////////////////////////////////////////////
//
// Now establish the matchup vectors
  int count = 0, timestep = 0;
  for (timestep = 0; timestep < 35; timestep++) {
    count = 0;
    skipped = 1.0;
    observed = 0.0;
    cellarea = 0.0;
    //printf("trying to get at %d fname %s\n",timestep, argv[2+timestep]); fflush(stdout);
    nsidc_get(argv[2+timestep], obs) ;

  for (loc.j = 0; loc.j < lat.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < lat.xpoints(); loc.i++) {
    ll.lat = lat[loc];
    while (lon[loc] > 360.) lon[loc] -= 360.;
    ll.lon = lon[loc];
    
    floc = obs.locate(ll);
    sloc = skip.locate(ll);

    if (obs[floc] > 1.0) continue;

    observed[count] = obs[floc];
    skipped[count]  = skip[sloc];
    cellarea[count] = tarea[loc];
    model[count]    = ice_coverage[timestep][loc];
    if ( ll.lat > 0 ) {
      north[count] = skipped[count];
      south[count] = 1; // 1 means do not use, 0 is to be used
    }
    else {
      north[count] = 1;
      south[count] = skipped[count];
    }

    count++;
  }
  }

// At last, start scoring:
  //for (level = 0.0; level < 1.; level += 0.05) {
  //  contingency(observed, model, skipped, level, a11, a12, a21, a22);
  //  contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  //  printf("  level %4.2f lead %2d  %f %f %f %f  %f %f %f %f %f %f\n",level, timestep,
  //                 a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  //}
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, north, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("nhlevel %4.2f lead %2d  %f %f %f %f  %f %f %f %f %f %f\n",level, timestep,
                   a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  //for (level = 0.0; level < 1.; level += 0.05) {
  //  contingency(observed, model, south, level, a11, a12, a21, a22);
  //  contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  //  printf("shlevel %4.2f lead %2d  %f %f %f %f  %f %f %f %f %f %f\n",level, timestep,
  //                 a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  //}
  fflush(stdout);
  } // timesteps

  return 0;
}
////////////////////////////////////////////////////////////////////////
template <class T>
void enter(grid2<float> &param, T *x) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    if (x[loc.i+ param.xpoints()*loc.j] > 1e20) x[loc.i+ param.xpoints()*loc.j] = 0;
    param[loc] = x[loc.i+ param.xpoints()*loc.j];
  }
  }
  #ifdef DEBUG
    printf("stats: %f %f %f %f\n",param.gridmax(), param.gridmin(), param.average(), param.rms() );
  #endif

  return;
}
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

  //printf("obs stats %f %f %f %f \n", obs.gridmax(), obs.gridmin(), obs.average(), obs.rms());
  //printf("tmp stats %f %f %f %f \n", tmp.gridmax(), tmp.gridmin(), tmp.average(), tmp.rms());
  fflush(stdout);
  return;
}
