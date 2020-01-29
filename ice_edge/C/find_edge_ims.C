#include "ncepgrids.h"

// Find the sea ice edge defined as over/under tolerance concentrations 
//    at adjacent page
// Robert Grumbine 10 May 2018 

#include "shared.C"
#include "edge_finder.C"

int main(int argc, char *argv[]) {
  // metric grid of some kind
  bedient_north<float> conc(96); // IMS analysis at 1/96th Bedient, ~4 km
  bedient_north<int> land(96);
  float conc_toler = 0.40; // IMS edge about 40%
  FILE *fin;
  ijpt loc;

// Get data:
  fin = fopen(argv[1],"r"); 
  conc.binin(fin);
  fclose(fin);

  land.set(0);
  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
    if (conc[loc] > 1) {
      land[loc] = 1 ;
      conc[loc] = 0.;
    }
  }
  }
  #ifdef DEBUG
    printf("nx ny = %d %d\n",conc.xpoints(), conc.ypoints() );
    printf("max min etc. %f %f %f %f\n",conc.gridmax(), conc.gridmin(), conc.average(), conc.rms() );
    fflush(stdout);
  #endif

// Look for ice edge (write out to stdout)
  edge_finder(conc, land, conc_toler);

  return 0;
}
