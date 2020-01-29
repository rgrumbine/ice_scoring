#include <stdio.h>
#include <stdlib.h>

// Compute scores for the CFSv2 ocean
//  -- vs. nsidc netcdf grids

#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

#include "grid_math.h"
#include "ncepgrids.h"
template <class T>
void enter(grid2<float> &param, T *x) ;


#include "contingency_ptwise.C"

int main(int argc, char *argv[]) {
  float *x;
  int ncid, varid;
  int retval;
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  global_12th<unsigned char> skip;
  FILE *fin;

// CFSv2 file variables of interest:
  mrf1deg<float> icec;

////////////////// skip grid ///////////////////////////////
  fin = fopen(argv[3], "r");
  skip.binin(fin);
  fclose(fin);
  skip.set(0);
  #ifdef DEBUG
  printf("skip stats %d %d %d %d \n", skip.gridmax(), skip.gridmin(), skip.average(), skip.rms()); 
  #endif

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from nsidc netcdf:
  nsidcnorth<float> obs;
  grid2<float> obslat(obs.ypoints(), obs.xpoints()), obslon(obs.ypoints(), obs.xpoints());
  grid2<float> tmp(obs.ypoints(), obs.xpoints());

  float *xf;
  unsigned char *xb;
  double *xd;

  xf = (float*) malloc(sizeof(float)*obs.xpoints()*obs.ypoints() );
  xb = (unsigned char*) malloc(sizeof(unsigned char)*obs.xpoints()*obs.ypoints() );
  xd = (double*) malloc(sizeof(double)*obs.xpoints()*obs.ypoints() );

////////////////// Sea ice analysis ///////////////////////////////
  retval = nc_open(argv[2], NC_NOWRITE, &ncid);
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


////////////////// CFSv2 variables ///////////////////////////////

  fin = fopen(argv[1],"r");
  icec.binin(fin);
  fclose(fin); 
  mrf1deg<float> lat, lon, tarea;
  for (loc.j = 0; loc.j < icec.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < icec.xpoints(); loc.i++) {
    ll = icec.locate(loc);
    if (icec[loc] > 300.) icec[loc] = 0;
    lat[loc] = ll.lat;
    lon[loc] = ll.lon;
    tarea[loc] = icec.cellarea(loc);
  }
  }

  #ifdef DEBUG
    palette<unsigned char> gg(19, 65);
    icec *= 100.;
    icec.xpm("ice.xpm",7,gg);
    loc.i = 0; loc.j = 0;
    printf("00 lat, ice: %f %f\n",icec[loc], lat[loc]);
    loc.i = lat.xpoints() - 1; loc.j = lat.ypoints() - 1;
    printf("NM lat, ice: %f %f\n",icec[loc], lat[loc]);
    return 0;
  #endif
  
///////////////// End of acquisition portion ////////////////////////////////////////////
//
// Now establish the matchup vectors
  int npts, count = 0;
  
  npts = icec.xpoints()*icec.ypoints();
  mvector<float> observed(npts), model(npts), cellarea(npts);
  mvector<unsigned char> skipped(npts), north(npts), south(npts);


  for (loc.j = 0; loc.j < icec.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < icec.xpoints(); loc.i++) {
    ll.lat = lat[loc];
    while (lon[loc] > 360.) lon[loc] -= 360.;
    ll.lon = lon[loc];
    
    floc = obs.locate(ll);
    sloc = skip.locate(ll);

    #ifdef DEBUG
    if (floc.i <= -0.5 || floc.j <= -0.5) {
      printf("floc %f %f\n", floc.i, floc.j);
    }
    if (floc.i > obs.xpoints()-0.5 || floc.j > obs.ypoints()-0.5) {
      printf("floc %f %f\n", floc.i, floc.j);
    }
    #endif
    if (obs[floc] > 1.0) continue;

    observed[count] = obs[floc];
    skipped[count]  = skip[sloc];
    model[count]    = icec[loc];
    cellarea[count] = tarea[loc];
    if ( ll.lat > 0 ) {
      north[count] = skipped[count];
      south[count] = 1; // 1 means do not use, 0 is to be used
    }
    else {
      north[count] = 1;
      south[count] = skipped[count];
    }

    #ifdef VERBOSE
    printf("%8d %5.3f %5.3f %3d  %7.3f %8.3f  %8.3f %8.3f\n",count,model[count], observed[count], skipped[count], lat[loc], lon[loc], floc.i, floc.j);
    #endif

    count++;
  }
  }


// At last, start scoring:
  float level;
  double a11, a12, a21, a22;
  float pod, far, fcr, pct, ts, bias;

  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, skipped, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("gllevel,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, north, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("nhlevel,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
//  for (level = 0.0; level < 1.; level += 0.05) {
//    contingency(observed, model, south, cellarea, level, a11, a12, a21, a22);
//    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
//    printf("shlevel %4.2f  %f %f %f %f  %f %f %f %f %f %f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
//  }

  return 0;
}

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
