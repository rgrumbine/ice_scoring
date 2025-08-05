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
#define ERV(e,v) {printf("Error: %s reading %s\n", nc_strerror(e), v); exit(ERRCODE);}

#include "ALL.C"

int main(int argc, char *argv[]) {
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  FILE *fin;

////////////////// Sea ice analysis ///////////////////////////////
// High res sea ice analysis from netcdf:
  char *fname;
  fname = argv[2];
  #ifdef DEBUG
    FILE *verbout;
    verbout = fopen("verbout","w");
  #endif

  printf("opening osisaf %s\n",fname); fflush(stdout);
  #include "stub.osisaf.C"

////////////////// skip grid ///////////////////////////////
  printf("opening skip\n"); fflush(stdout);
  fin = fopen(argv[3], "r");
  #include "stub.skip.C"
  fclose(fin);

////////////////// Latlon check and transfer ///////////////////////////////
  printf("latlon check and transfer\n"); fflush(stdout);
  obs.set((float) 157.0);
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    ll.lat = obslat[i];
    ll.lon = obslon[i];
    floc = obs.locate(ll);
    obs[floc] = tmp[i];
    #ifdef DEBUG2
    printf("osisaf %6d %.3f %.3f  %3.0f  %.3f %.3f  %f %f\n",i,
             obslat[i], obslon[i], tmp[i], floc.i, floc.j, 
             fabs(floc.i - rint(floc.i)) , fabs(floc.j - rint(floc.j) ) );
    #endif
  }
  for (int i = 0; i < obs.xpoints()*obs.ypoints(); i++) {
    if (obs[i] == 157.0) {
      obs[i] = -1.; // flag value to skip
      #ifdef DEBUG
      ll.lat = obslat[i];
      ll.lon = obslon[i];
      floc = obs.locate(ll);
      printf("failed to update %d nx ny = %d %d\n",i,obs.xpoints(), obs.ypoints() ); 
      printf("osisaf %6d %.3f %.3f  %3.0f  %.3f %.3f  %f %f\n",i,
             obslat[i], obslon[i], obs[i], floc.i, floc.j, 
             fabs(floc.i - rint(floc.i)) , fabs(floc.j - rint(floc.j) ) );
      fflush(stdout);
      #endif
    }
  }
  if (obs.gridmax() > 1000.0) obs /= 100.;
  if (obs.gridmax() > 1.0) obs /= 100.;

  #ifdef DEBUG
    fprintf(verbout, "obs stats %f %f %f %f \n", obs.gridmax(), obs.gridmin(), obs.average(), obs.rms()); 
    fprintf(verbout, "tmp stats %f %f %f %f \n", tmp.gridmax(), tmp.gridmin(), tmp.average(), tmp.rms()); 
    fflush(verbout);
  #endif


////////////////// Model variables ///////////////////////////////
/// 12th degree lat-lon sea ice analysis grid

  global_12th<float> ice_coverage;
  global_12th<float> lat, lon, tarea;

  printf("opening ice binary file\n"); fflush(stdout);
  fin = fopen(argv[1],"r");
  ice_coverage.ftnin(fin);
  fclose(fin);

  for (loc.j = 0; loc.j < lat.ypoints() ; loc.j++) {
  for (loc.i = 0; loc.i < lat.xpoints() ; loc.i++) {
    ll = lat.locate(loc);
    lat[loc] = ll.lat;
    lon[loc] = ll.lon;
    tarea[loc] = lat.cellarea(loc);
  }
  }


///////////////// End of Netcdf portion ////////////////////////////////////////////
//
// Now establish the matchup vectors
  int npts, count = 0;
  
  npts = ice_coverage.xpoints()*ice_coverage.ypoints();
  mvector<float> observed(npts), model(npts), cellarea(npts);
  mvector<unsigned char> skipped(npts), north(npts), south(npts);

  for (loc.j = 0; loc.j < ice_coverage.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < ice_coverage.xpoints(); loc.i++) {
    ll.lat = lat[loc];
    while (lon[loc] > 360.) lon[loc] -= 360.;
    ll.lon = lon[loc];
    
    floc = obs.locate(ll);
    sloc = skip.locate(ll);

      if (floc.i <= -0.5 || floc.j <= -0.5) {
    #ifdef DEBUG
        printf("floc %f %f\n", floc.i, floc.j);
    #endif
	continue;
      }
      if (floc.i > obs.xpoints()-0.5 || floc.j > obs.ypoints()-0.5) {
    #ifdef DEBUG
        printf("floc %f %f\n", floc.i, floc.j);
    #endif
	continue;
      }
    #ifdef DEBUG2
      fprintf(verbout, "model %d %d  %.3f %.3f %f vs. %f w. skip %d\n",
          loc.i, loc.j, ll.lat, ll.lon,
          ice_coverage[loc], obs[floc], (int) skip[sloc] );
      fflush(verbout);
    #endif
    if (obs[floc] > 1.0 || obs[floc] < 0.) continue;

    observed[count] = obs[floc];
    skipped[count]  = skip[sloc];
    model[count]    = ice_coverage[loc];
    cellarea[count] = tarea[loc];
    if ( ll.lat > 0 ) {
      north[count] = skipped[count];
      south[count] = 1; // 1 means do not use, 0 is to be used
    }
    else {
      north[count] = 1;
      south[count] = skipped[count];
    }

    #ifdef DEBUG2
      fprintf(verbout, "out2 %8d %5.3f %5.3f %3d  %7.3f %8.3f  %8.3f %8.3f\n",count,model[count], observed[count], skipped[count], lat[loc], lon[loc], floc.i, floc.j);
      fflush(verbout);
    #endif

    count++;
  }
  }
  #ifdef DEBUG
    fflush(verbout);
  #endif


// At last, start scoring ----------------------------------------------------------------
  float level;
  double a11, a12, a21, a22, iiee;
  float pod, far, fcr, pct, ts, bias;

  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, skipped, cellarea, level, a11, a12, a21, a22, iiee);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("level,%4.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias, iiee);
  }

  return 0;
}
