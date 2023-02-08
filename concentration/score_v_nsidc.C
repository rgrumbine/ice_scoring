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
  ijpt loc;
  fijpt floc, sloc;
  latpt ll;

// File of pts to skip
  FILE *fin;

  //debug: printf("C++ code entered model v. nsidc scoring\n"); fflush(stdout); 

////////////////// skip grid ///////////////////////////////
  //debug: printf("skip file = %s\n",argv[3]); fflush(stdout);
  fin = fopen(argv[3], "r");
  #include "stub.skip.C"

  //debug: printf("got the skip file from %s\n", argv[3]); fflush(stdout);

////////////////// Sea ice analysis ///////////////////////////////
// sea ice analysis from netcdf -- NSIDC climate data record

  float *x;
  x = (float*) malloc(sizeof(float)*NX*NY);

  int ncid, varid;
  int retval;
  nsidcnorth<float> obs;
  grid2<float> obslat(obs.ypoints(), obs.xpoints()), obslon(obs.ypoints(), obs.xpoints());
  grid2<float> tmp(obs.ypoints(), obs.xpoints());

  unsigned char *xb;
  double *xd;

  //debug: printf("about to try netcdf read\n"); fflush(stdout);

  xb = (unsigned char*) malloc(sizeof(unsigned char)*obs.xpoints()*obs.ypoints() );
  xd = (double*) malloc(sizeof(double)*obs.xpoints()*obs.ypoints() );

  // V4 doesn't save latitude or longitude. It is map projection, polar stereo, Hughes 1980 ellipsoid
  // V4 puts lat-lon in ancillary files, or in compilation files
  // for ancillary data:
  //debug: printf("ncopen of %s\n",argv[4]); fflush(stdout);
  retval = nc_open(argv[4], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

  //debug: printf("getting latitude\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "latitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, xd); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslat, xd);

  //debug: printf("getting longitude\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "longitude", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_double(ncid, varid, xd); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(obslon, xd);

  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);
  //debug: printf("closed ancillary file\n"); fflush(stdout);

  // for concentrations:
  //debug: printf("ncopen of %s\n",argv[2]); fflush(stdout);
  retval = nc_open(argv[2], NC_NOWRITE, &ncid);
  if (retval != 0) ERR(retval);

  // v3: retval = nc_inq_varid(ncid, "seaice_conc_cdr", &varid);
  //debug: printf("getting cdr_seaice_conc\n"); fflush(stdout);
  retval = nc_inq_varid(ncid, "cdr_seaice_conc", &varid);
  if (retval != 0) ERR(retval);
  retval = nc_get_var_uchar(ncid, varid, xb); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(tmp, xb);

  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

  //////////////// Latlon check and transfer ///////////////////////////////
  obs.set((float) 157.0);
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    ll.lat = obslat[i];
    ll.lon = obslon[i];
    floc = obs.locate(ll);
    obs[floc] = tmp[i];
    #ifdef DEBUG
     fprintf(verbout, "nsidc %6d %.3f %.3f  %3.0f  %.3f %.3f  %f %f\n",i,
         obslat[i], obslon[i], tmp[i], floc.i, floc.j, 
             fabs(floc.i - rint(floc.i)) , fabs(floc.j - rint(floc.j) ) );
    #endif
  }
  for (int i = 0; i < tmp.xpoints()*tmp.ypoints(); i++) {
    if (obs[i] == 157.0) {
      printf("failed to update %d\n",i);
    }
  }
  if (obs.gridmax() > 1.0) obs /= 100.;

  #ifdef DEBUG
    fprintf(verbout, "obs stats %f %f %f %f \n", obs.gridmax(), obs.gridmin(), obs.average(), obs.rms()); 
    fprintf(verbout, "tmp stats %f %f %f %f \n", tmp.gridmax(), tmp.gridmin(), tmp.average(), tmp.rms()); 
    fflush(verbout);
  #endif


////////////////// Hycom variables ///////////////////////////////
// Hycom diag file variables of interest:
  grid2<float> lat(NX, NY), lon(NX, NY), tarea(NX, NY);
  grid2<float> ice_coverage(NX, NY), ice_thickness(NX, NY);

  retval = nc_open(argv[1], NC_NOWRITE, &ncid);
  if (retval != 0) {
  #ifdef DEBUG
    fprintf(verbout, "some problem in nc_open of %s\n",argv[1]);
    fflush(verbout);
  #endif
    printf("some problem in nc_open of %s\n",argv[1]);
    fflush(stdout);
    ERR(retval);
    fflush(stdout);
  }
  #ifdef DEBUG
    fprintf(verbout, "passed nc_open of %s\n",argv[1]);
    fflush(verbout);
  #endif

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

  #if defined(cice_file) || defined(benchmark)
   retval = nc_inq_varid(ncid, "aice_h", &varid);
  #else
   retval = nc_inq_varid(ncid, "ice_coverage", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(ice_coverage, x);
  
  #if defined(cice_file) || defined(benchmark)
    retval = nc_inq_varid(ncid, "hi_h", &varid);
  #else
    retval = nc_inq_varid(ncid, "ice_thickness", &varid);
  #endif
  if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); 
  if (retval != 0) ERR(retval);fflush(stdout);
  enter(ice_thickness, x);

  #ifdef DEBUG
    printf("ice thickness max %f\n",ice_thickness.gridmax() ); fflush(stdout);
    fprintf(verbout, "ice thickness max %f\n",ice_thickness.gridmax() ); fflush(verbout);
  #endif

  retval = nc_close(ncid);
  if (retval != 0) ERR(retval); fflush(stdout);

  #ifdef DEBUG
    fprintf(verbout,"done with reading in netcdf of model\n");
    printf("done with reading in netcdf of model\n");
    fflush(verbout);
  #endif

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

    #ifdef VERBOSE
      if (floc.i <= -0.5 || floc.j <= -0.5) {
        printf("floc %f %f\n", floc.i, floc.j);
      }
      if (floc.i > obs.xpoints()-0.5 || floc.j > obs.ypoints()-0.5) {
        printf("floc %f %f\n", floc.i, floc.j);
      }
    #endif
    #ifdef DEBUG
      fprintf(verbout, "model %d %d  %.3f %.3f %f vs. %f w. skip %d\n",
          loc.i, loc.j, ll.lat, ll.lon,
          ice_coverage[loc], obs[floc], (int) skip[sloc] );
      fflush(verbout);
    #endif
    if (obs[floc] > 1.0) continue;

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

    #ifdef DEBUG
      fprintf(verbout, "out2 %8d %5.3f %5.3f %3d  %7.3f %8.3f  %8.3f %8.3f\n",count,model[count], observed[count], skipped[count], lat[loc], lon[loc], floc.i, floc.j);
      fflush(verbout);
    #endif

    count++;
  }
  }
  #ifdef DEBUG
    fflush(verbout);
  #endif


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

  return 0;
}
