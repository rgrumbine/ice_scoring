#include <stdio.h>
#include <stdlib.h>
// Score nsidc concentrations against each other
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
  FILE *fin;

// In case of verbose output:
    FILE *verbout;
    verbout = fopen("verboseout","w");

////////////////// skip grid ///////////////////////////////
  skip.set(0);
  fin = fopen(argv[1], "r");
  skip.binin(fin);
  fclose(fin);
  #ifdef DEBUG
    printf("skip stats %d %d %d %d \n",(int) skip.gridmax(),(int) skip.gridmin(), skip.average(), skip.rms()); 
  #endif

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from netcdf:
// cdr = climate data record
// nt  = nasa team(1)
// bt  = bootstrap
  nsidcnorth<float> obs_cdr, obs_nt, obs_bt;
  grid2<float> obslat(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> obslon(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_cdr(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_nt(obs_cdr.ypoints(), obs_cdr.xpoints());
  grid2<float> tmp_bt(obs_cdr.ypoints(), obs_cdr.xpoints());

  float *xf;
  unsigned char *xb;
  double *xd;

  xf = (float*) malloc(sizeof(float)*obs_cdr.xpoints()*obs_cdr.ypoints() );
  xb = (unsigned char*) malloc(sizeof(unsigned char)*obs_cdr.xpoints()*obs_cdr.ypoints() );
  xd = (double*) malloc(sizeof(double)*obs_cdr.xpoints()*obs_cdr.ypoints() );

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
  enter(tmp_cdr, xb);
  //printf("have cdr concentration\n"); fflush(stdout);

  retval = nc_inq_varid(ncid, "goddard_bt_seaice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp_bt, xb);
  //printf("have bt concentration\n"); fflush(stdout);

  retval = nc_inq_varid(ncid, "goddard_nt_seaice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp_nt, xb);
  //printf("have nt concentration\n"); fflush(stdout);

  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

////////////////// Latlon check and transfer ///////////////////////////////
  obs_cdr.set((float) 157.0);
  obs_nt.set((float) 157.0);
  obs_bt.set((float) 157.0);
  for (int i = 0; i < tmp_nt.xpoints()*tmp_nt.ypoints(); i++) {
    ll.lat = obslat[i];
    ll.lon = obslon[i];
    floc = obs_cdr.locate(ll);
    obs_cdr[floc] = tmp_cdr[i];
    obs_nt[floc] = tmp_nt[i];
    obs_bt[floc] = tmp_bt[i];
    if (obs_cdr[floc] > 100 || obs_nt[floc] > 100 || obs_bt[floc] > 100) {
      obs_cdr[floc] = 157.;
      obs_nt[floc] = 157.;
      obs_bt[floc] = 157.;
    }

    fprintf(verbout, "nsidc %6d %.3f %.3f  %3.0f %3.0f %3.0f  %.3f %.3f  %f %f\n",i,
        obslat[i], obslon[i], tmp_cdr[i], tmp_nt[i], tmp_bt[i], 
        floc.i, floc.j, fabs(floc.i - rint(floc.i)) , fabs(floc.j - rint(floc.j) ) );
  }
  fflush(verbout);

  if (obs_cdr.gridmax() > 1.0) obs_cdr /= 100.;
  if (obs_nt.gridmax() > 1.0) obs_nt /= 100.;
  if (obs_bt.gridmax() > 1.0) obs_bt /= 100.;


///////////////// End of Netcdf portion ////////////////////////////////////////////
//
// Now establish the matchup vectors
  int npts, count = 0;
  
  npts = obs_cdr.xpoints()*obs_cdr.ypoints();
  mvector<float> cdr(npts), nt(npts), bt(npts), cellarea(npts);

  mvector<unsigned char> skipped(npts), north(npts), south(npts);

  for (loc.j = 0; loc.j < obs_cdr.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < obs_cdr.xpoints(); loc.i++) {
    ll.lat = obslat[loc];
    while (obslon[loc] > 360.) obslon[loc] -= 360.;
    ll.lon = obslon[loc];
    
    sloc = skip.locate(ll);
// Don't look at points that have invalid observation values
    if (obs_cdr[loc] > 1.0 || obs_nt[loc] > 1.0 || obs_bt[loc] > 1.0) continue; 

    cdr[count] = obs_cdr[loc];
    nt[count] = obs_nt[loc];
    bt[count] = obs_bt[loc];
    skipped[count]  = skip[sloc];
    cellarea[count] = obs_cdr.cellarea(loc);

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
  float level;
  double a11, a12, a21, a22;
  float pod, far, fcr, pct, ts, bias;

  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(cdr, nt, skipped, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("cdrnt,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(cdr, bt, skipped, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("cdrbt,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(nt, bt, skipped, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("nt_bt,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }

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
