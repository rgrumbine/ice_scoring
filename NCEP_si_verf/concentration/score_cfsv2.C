#include <stdio.h>
#include <stdlib.h>

// Compute scores for the RTOFS-Global, netcdf outputs
// Robert Grumbine -- Hycom grid
// Denise Worthen -- Adding CICE grid

#include "netcdf.h"

#include "ALL.C"
#include "nsidc_nc.C"


int main(int argc, char *argv[]) {
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// Hycom diag file variables of interest:
  grid2<float> *ice_coverage;

  ice_coverage = new grid2<float>[35];
  for (int i = 0; i < 35; i++) {
    ice_coverage[i].resize(NX, NY);
  }

  // for scoring matchups
  float level;
  double a11, a12, a21, a22;
  float pod, far, fcr, pct, ts, bias;
  int npts = NX*NY;
  mvector<float> observed(npts), model(npts), cellarea(npts);
  mvector<unsigned char> skipped(npts), north(npts), south(npts);

////////////////// skip grid ///////////////////////////////
  #include "stub.skip.C"

////////////////// Hycom variables ///////////////////////////////
  #include "stub.hycom.C"

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from nsidc netcdf -- nsidc_nc.C from above
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
