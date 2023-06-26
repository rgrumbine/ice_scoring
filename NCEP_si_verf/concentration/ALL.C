#ifndef ALLC
  #define ALLC

// Collecting everything (?) to do with concentration verification vs. grids:

#include "grid_math.h"
#include "ncepgrids.h"
#include "mvector.h"

// compute the contingency table matchups
// if a11 etc are double, use weighting by cell area
//   else, merely match point for point.
// Note that in the indices, first one refers to the model, second to observations
//   1 means 'has ice', 2 means 'does not have ice' ( > than cutoff level)
//   so a12 means model has ice, but observation does not (false alarm)
//      a21 means model does not have ice, but observation does (false confidence)
// Robert Grumbine
// -----------------------------------------------------------------------------

// Some definitions:

#ifdef cice_file
  #define NX 1500
  #define NY 1099
#elif prototype
  #define NX 1440
  #define NY 1080
#elif rtofs
  #define NX 4500
  #define NY 3297
#else
  #undef NX
  #undef NY
#endif



// -----------------------------------------------------------------------------
// General functions:
template <class T>
void enter(grid2<float> &param, T *x) ;

void contingency_derived(double a11, double a12, double a21, double a22,
                 float &pod, float &far, float &fcr, float &pct, float &ts, float &bias);

// Code:

template <class T>
void enter(grid2<float> &param, T *x) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    if (x[loc.i+ param.xpoints()*loc.j] > 1e20) x[loc.i+ param.xpoints()*loc.j] = 0;
    param[loc] = (float) x[loc.i+ param.xpoints()*loc.j];
  }
  }
  #ifdef DEBUG
    printf("stats: %f %f %f %f\n",param.gridmax(), param.gridmin(), 
            param.average(), param.rms() );
  #endif

  return;
}
void contingency_derived(double a11, double a12, double a21, double a22, float &pod,
                 float &far, float &fcr, float &pct, float &ts, float &bias) {
  pod = (double) a11 / (double) (a11 + a12);
  far = (double) a12 / (double) (a12 + a11);
  fcr = (double) a21 / (double) (a21 + a22);
  pct = ((double) a11 + (double) a22) / ( (double) (a11+a12+a21+a22)); //percent correct
  ts  = (double) a11 / ( (double) (a11+a12+a21) ); // threat score, aka
                                                   // csi - critical success index
  bias = (double) (a11+a12) / ((double)(a11+a21));

  return;
}

// Declaration of gridded functions --------------------------------------------------
// allowing to skip arguments:
void contingency(llgrid<float> &obs, llgrid<float> &model,
              double &a11, double &a12, double &a21, double &a22) ;

void contingency(llgrid<float> &obs, llgrid<float> &model, float &level,
              double &a11, double &a12, double &a21, double &a22) ;

// the full, active, function:
void contingency(llgrid<float> &obs, llgrid<float> &model, 
                 grid2<unsigned char> &skip, float &level, 
                 double &a11, double &a12, double &a21, double &a22) ;

// Source code for gridded functions ------------------------------------------------

// use same code for both with and without skip mask -- just that if there's no 
//     skip mask, create one that does nothing
void contingency(llgrid<float> &obs, llgrid<float> &model,
              double &a11, double &a12, double &a21, double &a22) {
  grid2<unsigned char> skip(obs.xpoints(), obs.ypoints());
  float level = 0;
  skip.set((float) 0);
  contingency(obs, model, skip, level, a11, a12, a21, a22);
  return;
}
void contingency(llgrid<float> &obs, llgrid<float> &model, float &level,
              double &a11, double &a12, double &a21, double &a22) {
  grid2<unsigned char> skip(obs.xpoints(), obs.ypoints());
  skip.set((float) 0);
  contingency(obs, model, skip, level, a11, a12, a21, a22);
  return;
}

void contingency(llgrid<float> &obs, llgrid<float> &model, 
              grid2<unsigned char> &skip, float &level, 
              double &a11, double &a12, double &a21, double &a22) {
  double area = 0;
  ijpt loc;

  a11 = 0;
  a12 = 0;
  a21 = 0;
  a22 = 0;
  for (loc.j = 0; loc.j < obs.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < obs.xpoints(); loc.i++) {
    // only score if point is water of interest
    if ( skip[loc] == 0 ) {

      area += obs.cellarea(loc);

     // contingency table:
     if (model[loc] > level ) {
       if (obs[loc] > level ) {
         a11 += obs.cellarea(loc);
       }
       else {
         a12 += obs.cellarea(loc);
       }
     }
     else {
       if (obs[loc] > level ) {
         a21 += obs.cellarea(loc);
       }
       else {
         a22 += obs.cellarea(loc);
       }
     }
    }

  }
  }

  a11 /= area;
  a12 /= area;
  a21 /= area;
  a22 /= area;

  return;
}

// ----------------------------------
//     Scoring on matchup vectors

void contingency(mvector<float> &obs, mvector<float> &model,
              double &a11, double &a12, double &a21, double &a22) ;

void contingency(mvector<float> &obs, mvector<float> &model, 
                 mvector<unsigned char> &skip, float &level, 
                 double &a11, double &a12, double &a21, double &a22) ;
void contingency(mvector<float> &obs, mvector<float> &model, 
                 mvector<unsigned char> &skip, mvector<float> &cellareas,
                 float &level, 
                 double &a11, double &a12, double &a21, double &a22) ;

// Pointwise/mvector scoring for contingency table:
void contingency(mvector<float> &obs, mvector<float> &model, mvector<unsigned char> &skip, 
              float &level, double &a11, double &a12, double &a21, double &a22) {
  double area = 0;
  int count = 0;
  int loc;

  a11 = 0;
  a12 = 0;
  a21 = 0;
  a22 = 0;
  for (loc = 0; loc < obs.xpoints(); loc++) {
    // only score if point is water of interest
    if ( skip[loc] == 0 ) {
    
    count += 1;
    
    // contingency table:
    if (model[loc] > level ) {
      if (obs[loc] > level ) {
        a11 += 1;
       }
       else {
         a12 += 1;
       }
     }
     else {
       if (obs[loc] > level ) {
         a21 += 1;
       }
       else {
         a22 += 1;
       }
     }
    }

  }

  area = (double) count;
  a11 /= area;
  a12 /= area;
  a21 /= area;
  a22 /= area;

  return;
}
//
// Scoring for contingency table:
void contingency(mvector<float> &obs, mvector<float> &model, mvector<unsigned char> &skip, 
              mvector<float> &cellarea,
              float &level, double &a11, double &a12, double &a21, double &a22) {
  double area = 0;
  int count = 0;
  int loc;

  a11 = 0;
  a12 = 0;
  a21 = 0;
  a22 = 0;
  for (loc = 0; loc < obs.xpoints(); loc++) {
    // only score if point is water of interest
    if ( skip[loc] == 0 ) {
    
    count += 1;
    area  += cellarea[loc];
    
    // contingency table:
    if (model[loc] > level ) {
      if (obs[loc] > level ) {
        a11 += cellarea[loc];
       }
       else {
         a12 += cellarea[loc];
       }
     }
     else {
       if (obs[loc] > level ) {
         a21 += cellarea[loc];
       }
       else {
         a22 += cellarea[loc];
       }
     }
    }

  }

  //area = (double) count;
  a11 /= area;
  a12 /= area;
  a21 /= area;
  a22 /= area;

  return;
}
//////////////////////////////////////////////////////////////////

void  scoring(FILE *fout, grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, global_12th<float> &obs) ;
void  scoring(FILE *fout, grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, global_12th<float> &obs, global_12th<unsigned char> &skip, float level) ;

void  scoring(FILE *fout, grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, global_12th<float> &obs, global_12th<unsigned char> &skip, float level) {
  latpt ll;
  fijpt floc;
  ijpt loc;
  double sum = 0, sumsq = 0;
  int count = 0;
  int a11 = 0, a12 = 0, a21 = 0, a22 = 0;

// aice, lat, lon, obs, fout
  for (loc.j = 0; loc.j < aice.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < aice.xpoints(); loc.i++) {
    ll.lat = lat[loc];
    while (lon[loc] > 360.) lon[loc] -= 360.;
    ll.lon = lon[loc] ;

    floc = obs.locate(ll);
    #ifdef DEBUG
      if (floc.i <= -0.5 || floc.j <= -0.5) {
        fprintf(fout, "floc %f %f\n", floc.i, floc.j);
      }
      if (floc.i > obs.xpoints()-0.5 || floc.j > obs.ypoints()-0.5) {
        fprintf(fout, "floc %f %f\n", floc.i, floc.j);
      }
    #endif

    // only score if point is water of interest, and at least one of observed or fcst is >= level
    if ( (skip[floc] == 0) ) {
  
      sum += obs[floc] - aice[loc];
      sumsq += (obs[floc] - aice[loc])*(obs[floc] - aice[loc]);
      count += 1;

     // contingency table:
     if (aice[loc] > level ) {
       if (obs[floc] > level ) {
         a11 += 1;
       }
       else {
         a12 += 1;
       }
     }
     else {
       if (obs[floc] > level ) {
         a21 += 1;
       }
       else {
         a22 += 1;
       }
     }
    }

  }
  }
  //printf("count = %d %d\n",count, a11+a12+a21+a22);

  fprintf(fout, "skip mean, rms = %6.3f %6.3f level = %5.2f\n",sum/count, sqrt(sumsq/count), level );
  fprintf(fout, "skip contingency %6.3f %6.3f %6.3f %6.3f  %5.2f\n",(float)a11/(float)count, (float)a12/(float)count,
        (float)a21/(float)count, (float)a22/(float)count, level);
  double pod, far, fcr, pct, ts, bias;
  pod = (double) a11 / (double) (a11 + a12);
  far = (double) a12 / (double) (a12 + a11);
  fcr = (double) a21 / (double) (a21 + a22);
  pct = ((double) a11 + (double) a22) / ( (double) a11+a12+a21+a22); //percent correct
  ts  = (double) a11 / ( (double) a11+a12+a21); // threat score, aka csi - critical success index
  bias = (double) (a11+a12) / ((double)(a11+a21));
  fprintf(fout, "skip pod etc %6.3f %6.3f %6.3f %6.3f %6.3f %f   %5.2f\n",pod, far, fcr, pct, ts, bias, level);


  return;
}
void  scoring(FILE *fout, grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, global_12th<float> &obs) {
  latpt ll;
  fijpt floc;
  ijpt loc;
  double sum = 0, sumsq = 0;

// aice, lat, lon, obs, fout
  for (loc.j = 0; loc.j < aice.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < aice.xpoints(); loc.i++) {
    ll.lat = lat[loc];
    while (lon[loc] > 360.) lon[loc] -= 360.;
    ll.lon = lon[loc] ;

    floc = obs.locate(ll);
    if (floc.i <= -0.5 || floc.j <= -0.5) {
      fprintf(fout, "floc %f %f\n", floc.i, floc.j);
    }
    if (floc.i > obs.xpoints()-0.5 || floc.j > obs.ypoints()-0.5) {
      fprintf(fout, "floc %f %f\n", floc.i, floc.j);
    }

    sum   += (obs[floc] - aice[loc]);
    sumsq += (obs[floc] - aice[loc])*(obs[floc] - aice[loc]);

  }
    fflush(fout);
  }
  fprintf(fout, "global mean, rms = %e %e\n",sum/aice.xpoints()/aice.ypoints(), sqrt(sumsq/aice.xpoints()/aice.ypoints()) );

  return;
}

#endif

