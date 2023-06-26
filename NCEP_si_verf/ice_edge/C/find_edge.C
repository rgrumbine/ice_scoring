#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent page
// Robert Grumbine 10 May 2018 

#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
  // metric grid of some kind
  global_12th<float> conc, dist;
  float conc_toler ; // cutoff for finding ice edge.  IMS is about 0.40
  float dist_toler = 25.*1000.; // meters.  require being > this distance away from land to score
  FILE *fin;

//////////////////////////////////////////////
// Get data:
  fin = fopen(argv[1],"r"); 
  conc.binin(fin);
  fclose(fin);
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
