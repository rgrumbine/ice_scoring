#include "mvector.h"

// compute the contingency table matchups
// if a11 etc are double, use weighting by cell area
//   else, merely match point for point.
// Note that in the indices, first one refers to the model, second to observations
//   1 means 'has ice', 2 means 'does not have ice' ( > than cutoff level)
//   so a12 means model has ice, but observation does not (false alarm)
//      a21 means model does not have ice, but observation does (false confidence)
// Robert Grumbine

void contingency(mvector<float> &obs, mvector<float> &model,
              double &a11, double &a12, double &a21, double &a22) ;

void contingency(mvector<float> &obs, mvector<float> &model, 
                 mvector<unsigned char> &skip, float &level, 
                 double &a11, double &a12, double &a21, double &a22) ;
void contingency(mvector<float> &obs, mvector<float> &model, 
                 mvector<unsigned char> &skip, mvector<float> &cellareas,
                 float &level, 
                 double &a11, double &a12, double &a21, double &a22) ;


template <class T>
void contingency_derived(T a11, T a12, T a21, T a22, float &pod, 
                 float &far, float &fcr, float &pct, float &ts, float &bias);

// Derived statistics (actually same between pointwise and grid versions)
template <class T>
void contingency_derived(T a11, T a12, T a21, T a22, float &pod, float &far, 
                            float &fcr, float &pct, float &ts, float &bias) {
   pod = (double) a11 / (double) (a11 + a12);
   far = (double) a12 / (double) (a12 + a11);
   fcr = (double) a21 / (double) (a21 + a22);
   //percent correct
   pct = ((double) a11 + (double) a22) / ( (double) (a11+a12+a21+a22)); 
   // threat score, aka csi - critical success index
   ts  = (double) a11 / ( (double) (a11+a12+a21) ); 

   bias = (double) (a11+a12) / ((double)(a11+a21));

  return;
}

 
// use same code for both with and without -- just that if there's no 
//     skip mask, create one that does nothing
void contingency(mvector<float> &obs, mvector<float> &model,
              double &a11, double &a12, double &a21, double &a22) {
  mvector<unsigned char> skip(obs.xpoints() );
  float level = 0;
  skip = 0;
  contingency(obs, model, skip, level, a11, a12, a21, a22);
  return;
}

// Scoring for contingency table:
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
