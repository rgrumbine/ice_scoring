#include <stdio.h>
#include <stdlib.h>

// Compute scores for NSIDC CDR vs. itself
// Robert Grumbine -- 25 Feb 2020

#include "netcdf.h"

#include "ALL.C"

#include "nsidc_nc.C"

int main(int argc, char *argv[]) {
  float *x;
  int ncid, varid;
  int retval;
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from nsidc netcdf:
  nsidcnorth<float> obs[2];

  // for scoring matchups
  float level;
  double a11, a12, a21, a22;
  float pod, far, fcr, pct, ts, bias;
  int npts = obs[0].xpoints()*obs[0].ypoints();
  mvector<float> observed(npts), model(npts), cellarea(npts);
  mvector<unsigned char> skipped(npts), north(npts), south(npts);

////////////////// skip grid ///////////////////////////////
// File of pts to skip
  global_12th<unsigned char> skip;

  //fin = fopen(argv[1], "r");
  //skip.binin(fin);
  //fclose(fin);
  skip.set(0);

///////////////// End of Netcdf portion ////////////////////////////////////////////
//
// Now establish the matchup vectors
  int count = 0, timestep = 1;
  nsidc_get(argv[1], obs[0]) ;
  nsidc_get(argv[2], obs[1]) ;
  
  count = 0;
  skipped = 1.0;
  observed = 0.0;
  cellarea = 0.0;

  for (loc.j = 0; loc.j < obs[0].ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < obs[0].xpoints(); loc.i++) {
    ll = obs[0].locate(loc);
    while (ll.lon >=  360.) ll.lon -= 360.;
    while (ll.lon <= -360.) ll.lon += 360.;
    
    floc = obs[0].locate(ll);
    sloc = skip.locate(ll);

    if (obs[0][floc] > 1.0 || obs[timestep][floc] > 1.0) continue;

    observed[count] = obs[0][floc];
    skipped[count]  = skip[sloc];
    cellarea[count] = obs[0].cellarea(loc);
    model[count]    = obs[timestep][loc];
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
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, north, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("nhlevel,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level,
                   a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  fflush(stdout);

  return 0;
}
////////////////////////////////////////////////////////////////////////
