#include "ncepgrids.h"

#include "readers.C"

// Global
int ae(llgrid<float> &conc, metricgrid<unsigned char> &land, 
    float &nharea, float &nhextent, float &sharea, float &shextent) ;
int ae(psgrid<float> &conc, metricgrid<unsigned char> &land, 
    float &nharea, float &nhextent, float &sharea, float &shextent) ;

// for cice et al grids -- mask and cellarea in input file
int ae(grid2<float> &conc, grid2<float> &tmask, grid2<float> &tarea, grid2<float> &tlat,
    float &nharea, float &nhextent, float &sharea, float &shextent) ;


// Regional
int ae(llgrid<float> &conc, metricgrid<unsigned char> &land, 
     mvector<double> &area, mvector<double> &extent, mvector<ijpt> &ll, 
     mvector<ijpt> &ur) ;
int ae(psgrid<float> &conc, metricgrid<unsigned char> &land, 
     mvector<double> &area, mvector<double> &extent, mvector<ijpt> &ll, 
     mvector<ijpt> &ur) ;

/////////// Main
int main(int argc, char *argv[]) {
  FILE *fin;

// For use by all
  global_12th<unsigned char> land;
  float minconc = 0.;
// NCEP, IMS analysis
  #ifdef NCEP
    global_12th<float> conc;
  #elif IMS
    bedient_north<float> conc(96);
  #endif
// NSIDC
  #ifdef NSIDC
  nsidcnorth<float> conc_north, lat_n, lon_n;
  nsidcsouth<float> conc_south, lat_s, lon_s;
  #endif
  
// RTOFS 
// CICE6
// GOFS3.1/ACNFS
  #ifdef CICE
  grid2<float> conc, tmask, tarea, tlat;
  #endif
   

  fin = fopen(argv[1],"r");
  reader(land, fin);
  fclose(fin);

  #ifdef NCEP
    fin = fopen(argv[2],"r");
    reader(conc, fin);
    fclose(fin);
  #elif IMS
    fin = fopen(argv[2],"r");
    if (fin == (FILE*) NULL) {
      printf("Failed to open %s, aborting\n",argv[2]);
      return 2;
    }
    reader(conc, fin);
    fclose(fin);
  #elif NSIDC
    fin = fopen(argv[2], "r");
    reader(conc_north, lat_n, lon_n, fin);
    fclose(fin);
    fin = fopen(argv[3], "r");
    reader(conc_south, lat_s, lon_s, fin);
    fclose(fin);
  #elif CICE
     cice_reader(conc, tmask, tarea, tlat, argv[2]);
     if (argc == 4) {
       minconc = atof(argv[3]);
       //debug: printf("min conc = %f\n",minconc);
       for (int i = 0; i < conc.xpoints()*conc.ypoints(); i++) {
         if (conc[i] < minconc) conc[i] = 0.0;
       }
     }
  #endif

  float nharea, nhextent, sharea, shextent;
  #ifdef NSIDC
    float nhatmp, shatmp, nhetmp, shetmp;
    ae(conc_north, land, nhatmp, nhetmp, shatmp, shetmp);
    nharea = nhatmp;
    nhextent = nhetmp;
    ae(conc_south, land, nhatmp, nhetmp, shatmp, shetmp);
    sharea = shatmp;
    shextent = shetmp;
  #elif CICE
    ae(conc, tmask, tarea, tlat, nharea, nhextent, sharea, shextent);
  #else 
    printf("don't know what to do with this data source -- CICE or NSIDC only\n");
    fflush(stdout);
    return 1;
  #endif
  
// will be desirable to have a tag for which model/analysis is used:
  printf("%f NH %6.3f %6.3f SH %6.3f %6.3f Global %6.3f %6.3f \n", minconc, nharea, nhextent,
   sharea, shextent, (nharea + sharea), (nhextent+shextent) );

  return 0;

}
int ae(psgrid<float> &conc, metricgrid<unsigned char> &land, float &nharea, float &nhextent, float &sharea, float &shextent) {
  ijpt loc, land_loc;
  latpt ll;
  double area_sum_nh = 0.0, extent_sum_nh = 0.0;
  double area_sum_sh = 0.0, extent_sum_sh = 0.0;
  //verbose printf("in ae for psgrid \n"); fflush(stdout);
 
  nharea = 0.0;
  sharea = 0.0;
  nhextent = 0.0;
  shextent = 0.0;

  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    //verbose printf("loc.j = %d\n",loc.j); fflush(stdout);
  for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
    ll = conc.locate(loc);
    land_loc = land.locate(ll);
    //very_verbose printf("loc.i = %d\n",loc.i); fflush(stdout);
    if (conc[loc] == 0. || land[land_loc] != 0) continue; // no ice or on land
    if (ll.lat > 0.) {
      area_sum_nh += conc.cellarea(loc)*conc[loc];
      extent_sum_nh += conc.cellarea(loc);
    }
    else {
      area_sum_sh += conc.cellarea(loc)*conc[loc];
      extent_sum_sh += conc.cellarea(loc);
    }
  }
  }
  nharea   = area_sum_nh   / 1.e12; // million km^2
  nhextent = extent_sum_nh / 1.e12;
  sharea   = area_sum_sh   / 1.e12; 
  shextent = extent_sum_sh / 1.e12;

  return 0;
}
int ae(psgrid<float> &conc, metricgrid<unsigned char> &land, mvector<double> &area, mvector<double> &extent, mvector<ijpt> &ll, mvector<ijpt> &ur) {
  ijpt loc;
  int i;

  for (i = 0; i < area.xpoints(); i++) {
    area[i] = 0.0;
    extent[i] = 0.0;
  }
  for (i = 0; i < area.xpoints(); i++) {
    for (loc.j = ll[i].j; loc.j <= ur[i].j; loc.j++) {
    for (loc.i = ll[i].i; loc.i <= ur[i].i; loc.i++) {
      if (conc[loc] == 0. || land[loc] != 0) continue; // no ice or on land
      area[i] += conc.cellarea(loc)*conc[loc];
      extent[i] += conc.cellarea(loc);
    }
    }
  }

  return 0;
}
int ae(llgrid<float> &conc, metricgrid<unsigned char> &land, float &nharea, float &nhextent, float &sharea, float &shextent) {
  ijpt loc;
  latpt ll;
  double area_sum_nh = 0.0, extent_sum_nh = 0.0;
  double area_sum_sh = 0.0, extent_sum_sh = 0.0;
 
  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
    if (conc[loc] == 0. || land[loc] != 0) continue; // no ice or on land
    ll = conc.locate(loc);
    if (ll.lat > 0.) {
      area_sum_nh += conc.cellarea(loc)*conc[loc];
      extent_sum_nh += conc.cellarea(loc);
    }
    else {
      area_sum_sh += conc.cellarea(loc)*conc[loc];
      extent_sum_sh += conc.cellarea(loc);
    }
  }
  }
  nharea = area_sum_nh / 1.e12; // million km^2
  nhextent = extent_sum_nh / 1.e12;
  sharea = area_sum_sh / 1.e12; 
  shextent = extent_sum_sh / 1.e12;

  return 0;
}
int ae(llgrid<float> &conc, metricgrid<unsigned char> &land, mvector<double> &area, mvector<double> &extent, mvector<ijpt> &ll, mvector<ijpt> &ur) {
  ijpt loc;
  int i;

  for (i = 0; i < area.xpoints(); i++) {
    area[i] = 0.0;
    extent[i] = 0.0;
  }
  for (i = 0; i < area.xpoints(); i++) {
    for (loc.j = ll[i].j; loc.j <= ur[i].j; loc.j++) {
    for (loc.i = ll[i].i; loc.i <= ur[i].i; loc.i++) {
      if (conc[loc] == 0. || land[loc] != 0) continue; // no ice or on land
      area[i] += conc.cellarea(loc)*conc[loc];
      extent[i] += conc.cellarea(loc);
    }
    }
  }

  return 0;
}
// for cice et al grids -- mask and cellarea in input file
int ae(grid2<float> &conc, grid2<float> &tmask, grid2<float> &tarea, grid2<float> &tlat,
    float &nharea, float &nhextent, float &sharea, float &shextent) {
  ijpt loc;
  latpt ll;
  double area_sum_nh = 0.0, extent_sum_nh = 0.0;
  double area_sum_sh = 0.0, extent_sum_sh = 0.0;

  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
    if (conc[loc] == 0. || tmask[loc] == 0) continue; // no ice or on land
    if (tlat[loc] > 0.) {
      area_sum_nh += tarea[loc]*conc[loc];
      extent_sum_nh += tarea[loc];
    }
    else {
      area_sum_sh += tarea[loc]*conc[loc];
      extent_sum_sh += tarea[loc];
    }
  }
  }
  nharea   = area_sum_nh   / 1.e12; // million km^2
  nhextent = extent_sum_nh / 1.e12;
  sharea   = area_sum_sh   / 1.e12;
  shextent = extent_sum_sh / 1.e12;

  return 0;
}
