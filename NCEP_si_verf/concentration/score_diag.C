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

#include "ALL.C"

int main(int argc, char *argv[]) {
  float *x;
  int ncid, varid;
  int retval;
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  FILE *fin;

// Hycom diag file variables of interest:
  grid2<float> lat(NX, NY), lon(NX, NY), tarea(NX, NY);
  grid2<float> ice_coverage(NX, NY), ice_thickness(NX, NY);
  grid2<float> u_barotropic_velocity(NX, NY), v_barotropic_velocity(NX, NY);

  x = (float*) malloc(sizeof(float)*NX*NY);

////////////////// skip grid ///////////////////////////////
  fin = fopen(argv[3], "r");
  #include "stub.skip.C"

////////////////// Sea ice analysis ///////////////////////////////
// NCEP analysis
  global_12th<float> obs;
  fin = fopen(argv[2], "r");
  obs.ftnin(fin);
  fclose(fin);

  #ifdef NSIDC
// nsidc sea ice analysis from netcdf:
    char* fname;
    fname = argv[2];

    #include "stub.nsidc.C"

//  //////////////// Latlon check and transfer ///////////////////////////////

  obs.set((float) 157.0);
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    ll.lat = obslat[i];
    ll.lon = obslon[i];
    floc = obs.locate(ll);
    obs[floc] = tmp[i];
  }
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    if (obs[i] == 157.0) {
      printf("failed to update %d\n",i);
    }
  }
  if (obs.gridmax() > 1.0) obs /= 100.;

  printf("obs stats %f %f %f %f \n", obs.gridmax(), obs.gridmin(), obs.average(), obs.rms()); 
  printf("tmp stats %f %f %f %f \n", tmp.gridmax(), tmp.gridmin(), tmp.average(), tmp.rms()); 
  fflush(stdout);


  #endif
  // end of selection between NCEP and NSIDC

  printf("obs stats %f %f %f %f \n", obs.gridmax(), obs.gridmin(), obs.average(), obs.rms()); 
  fflush(stdout);

////////////////// Hycom variables ///////////////////////////////

  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);
  printf("now past the ncopen\n"); fflush(stdout);

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

//  #if defined(cice_file) || defined(benchmark)
//   retval = nc_inq_varid(ncid, "tarea", &varid);
//  #else
//   retval = nc_inq_varid(ncid, "tarea", &varid);
//  #endif
//  if (retval != 0) ERR(retval);
//  retval = nc_get_var_float(ncid, varid, x); 
//  if (retval != 0) ERR(retval);fflush(stdout);
//  enter(tarea, x);

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "aice_h", &varid);
  #else
   retval = nc_inq_varid(ncid, "ice_coverage", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(ice_coverage, x);
  #ifdef DEBUG
    palette<unsigned char> gg(19, 65);
    ice_coverage *= 100.;
    ice_coverage.xpm("ice.xpm",7,gg);
    loc.i = 0; loc.j = 0;
    printf("00 lat, ice: %f %f\n",ice_coverage[loc], lat[loc]);
    loc.i = lat.xpoints() - 1; loc.j = lat.ypoints() - 1;
    printf("NM lat, ice: %f %f\n",ice_coverage[loc], lat[loc]);
    return 0;
  #endif
  
  #if defined(cice_file) || defined(benchmark)
  retval = nc_inq_varid(ncid, "hi_h", &varid);
  #else
   retval = nc_inq_varid(ncid, "ice_thickness", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(ice_thickness, x);

// close when done:
  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

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
    model[count]    = ice_coverage[loc];
    //cellarea[count] = tarea[loc];
    cellarea[count] = 1.;
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
    printf("  level %4.2f  %f %f %f %f  %f %f %f %f %f %f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, north, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("nhlevel %4.2f  %f %f %f %f  %f %f %f %f %f %f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }
  for (level = 0.0; level < 1.; level += 0.05) {
    contingency(observed, model, south, cellarea, level, a11, a12, a21, a22);
    contingency_derived(a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
    printf("shlevel %4.2f  %f %f %f %f  %f %f %f %f %f %f\n",level, a11, a12, a21, a22, pod, far, fcr, pct, ts, bias);
  }

  return 0;
}
