#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent page
// Robert Grumbine 10 May 2018 

#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
  // CFS ocnf grid 
  mrf1deg<float> conc;
  // CFS flxf grid:
  //gaussian<float> conc(126);
  float conc_toler; // cutoff for finding ice edge.  IMS is about 0.40
  // distance to land:
  global_12th<float> dist;
  float dist_toler = 25.*1000.; // meters.  require being > this distance away from land to score
  FILE *fin;

  //printf("t126 nx ny %d %d\n",conc.xpoints(), conc.ypoints() );
  //return 0;

//////////////////////////////////////////////
// Get data:
  fin = fopen(argv[1],"r"); 
  conc.binin(fin);
  fclose(fin);
  //printf("flag value = %f\n",conc.gridmax() );
  if (conc.gridmax() > 2.0) {
    float flag;
    ijpt loc;
    flag = conc.gridmax();
    //printf("flag value = %f\n",flag);
    for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
      if (conc[loc] == flag) conc[loc] = 0.0;
    }
    }
  }
// Get the distance to land map:
  fin = fopen(argv[2],"r");
  dist.binin(fin);
  fclose(fin);
  #ifdef DDEBUG
    printf("dist stats %.3f %.3f %.3f %.3f\n",dist.gridmax(), dist.gridmin(), 
                   dist.average(), dist.rms() );
    fflush(stdout);
  #endif

  conc_toler = atof(argv[3]);
//////////////////////////////////////////////

  edge_finder(conc, dist, conc_toler, dist_toler);

  return 0;
}
