#include <math.h>
#include "ncepgrids.h"
#include "mvector.h"
#include "buoy.h"

// Scoring the distance between two ice edge analyses
// Robert Grumbine 10 May 2018
// Add consideration of distance to land

int main(int argc, char *argv[]) {
  FILE *fin1, *fin2;
  int i, j, nf, no;
  float lat, lon;
  global_12th<float> landdist;
  mvector<latpt> fcst(300000), obsd(300000);
  fijpt floc;
  latpt ll;

  if (argc < 5) {
    printf("need distance to land, edge1, edge2, and land distance tolerance (km)\n");
    fflush(stdout);
    exit(1);
  }

// Distance to land:
  fin1 = fopen(argv[1], "r");
  landdist.binin(fin1);
  fclose(fin1);
  if (landdist.gridmax() > 1e6) landdist /= 1000.; //convert to km
  //debug printf("landdist gridmax = %f\n",landdist.gridmax() ); fflush(stdout);
  float landtoler = atof(argv[4]);
  //debug printf("land toler = %f km\n",landtoler); fflush(stdout);

// Model / forecast to be scoring:
  fin1 = fopen(argv[2], "r");
  if (fin1 == (FILE*) NULL) {
    printf("failed to open %s\n",argv[2]);
    exit(1);
  }
  nf = 0;
  while (!feof(fin1) ) {
    fscanf(fin1, "%f %f\n",&lon, &lat);
    ll.lon = lon;
    ll.lat = lat;
    floc = landdist.locate(ll);
    //debug2 printf("%f %f  %f %f  %f %f  %f\n",lon, lat, ll.lon, ll.lat, floc.i, floc.j, landdist[floc]);
    if (landdist[floc] > landtoler) {
      //debug printf("%f %f\n",lon, lat);
      fcst[nf].lat  = lat;
      fcst[nf].lon  = lon;
      nf += 1;
    }
  }
  //debug printf("nf1 = %d\n", nf);
  fclose(fin1);

// Observed analysis (reference, 'truth')
  fin2 = fopen(argv[3], "r");
  if (fin2 == (FILE*) NULL) {
    printf("failed to open %s\n",argv[3]);
    exit(2);
  }
  no = 0;
  while (!feof(fin2) ) {
    fscanf(fin2, "%f %f\n",&lon, &lat);
    ll.lon = lon;
    ll.lat = lat;
    floc = landdist.locate(ll);
    if (landdist[floc] > landtoler) {
      obsd[no].lat  = lat;
      obsd[no].lon  = lon;
      no += 1;
    }
  }
  //debug printf("nobsd = %d\n", no);
  fflush(stdout);

  /////////////////////////////////////
  //  Begin scoring loop
  //debug printf("beginning scoring loop\n"); fflush(stdout);

  float tolerance = 150., rmin, tdist;
  double sumsq    = 0.0;
  int count = 0, jmin;
  for (i = 0; i < nf; i++) {
    rmin = 9.e6;
    jmin = -1;
    tdist = 0.;
    for (j = 0; j < no; j++) {
      if (obsd[j].lon > 180.) obsd[j].lon -= 360.;
      if (fcst[j].lon > 180.) fcst[j].lon -= 360.;
      if (obsd[j].lon < -180.) obsd[j].lon += 360.;
      if (fcst[j].lon < -180.) fcst[j].lon += 360.;

      if (fabs(obsd[j].lat - fcst[i].lat) > tolerance/111.1) continue;
      tdist = ARCDIS(obsd[j].lon, obsd[j].lat, fcst[i].lon, fcst[i].lat);
      if (tdist < rmin) {
        rmin = tdist;
        jmin = j;
      }
    }
    if (rmin < tolerance) {
      printf("%6d rmin %f  %f %f  %f %f\n",i, rmin, obsd[jmin].lon, obsd[jmin].lat, fcst[i].lon, fcst[i].lat);
      sumsq += rmin*rmin;
      count += 1;
    }
    #ifdef DEBUG
    if ((i % 1000 == 0) && i > 100) {
      printf("rms %6.2f with %5d matchups lon= %f\n",sqrt(sumsq/(float)count), count, fcst[i].lon );
      fflush(stdout);
    }
    #endif
  }
  printf("rms %6.2f with %5d matchups\n",sqrt(sumsq/(float)count), count);
  /////////////////////////////////////

  return 0;
}
