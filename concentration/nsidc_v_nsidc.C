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

#include "ALL.C"


int main(int argc, char *argv[]) {
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  FILE *fin;

// In case of verbose output:
    FILE *verbout;
    verbout = fopen("verboseout","w");

////////////////// skip grid ///////////////////////////////
  fin = fopen(argv[1], "r");
  #include "stub.skip.C"

////////////////// Sea ice analysis ///////////////////////////////
// NSIDC sea ice analysis from netcdf:
// cdr = climate data record
// nt  = nasa team(1)
// bt  = bootstrap
  char *fname;
  fname = argv[2];
  #include "stub.nsidc.C"

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

