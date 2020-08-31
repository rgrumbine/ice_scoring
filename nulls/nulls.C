// construct null forecasters for sea ice cover, giving a baseline for
//   assessing skill of 'real' models
// Robert Grumbine 12 June 2014
// Renewed 20 Augus 2020
//
// level 0 -- forecasters which have no knowledge of anything
// level 1 -- forecaster knows history in general but nothing recent
// level 2 -- forecaster which knows only yesterday
// level 3 -- forecaster which knows yesterday, history, climatology
//

#include "nulls.h"

// level 0 nulls -- completely ignorant nulls
template<class T>
void null(grid2<T> &x, int sort) {
  switch(sort) {
    case GLACIAL :
      x.set((T) 1);
      break;
    case TROPICAL :
      x.set((T) 0);
      break;
    default :
      printf("error message\n");
  }
  return;
}

// level 1 nulls -- knows history in general but nothing recent
template<class T>
void null(grid2<T> &x, int sort, FILE *fin, int jday) {
// the file is a netcdf file, 1 time per day for the previous year
// rely on the file to have the 365 or 366 time levels, as needed
  switch(sort) {
    case LAST_YEAR :
      // extract jday from fin
      break;
    case COND_AVG :
      // extract jday from fin
      break;
    case UNCOND_AVG :
      // extract jday from fin
      break;
    default :
      return;
  }
  return;

} 

// level 2 -- forecaster which knows only yesterday
template<class T>
void null(grid2<T> &x, grid2<T> &observed) {
  x = observed;
  return;
}

// level 3 -- forecaster which knows yesterday, history, climatology
//   a) analog wrt history (full history !?)
//   b) sweep ice cover for N (# years of ice in grid points) and apply
//       same N to each area + adjacent points
//   c) Ice obs N days ago as well
//   d) Cli-Per type
template<class T>
void null(grid2<T> &x, int sort, FILE *fin) {


  return;
}

// Utilities -- 
//   the GFS is (2020) applying a filter in the northern hemisphere that 
//      zeroes ice concentration below 0.40
//   the MRF (1997-20NN) applied a filter such that ice concentrations 
//      below 0.55 were set to 0, and those above were set to 1.0

float gfs(float &x) {
  float y;
  if (x < 0.40) {
    y = 0.00;
  }
  else {
    y = x;
  }
  return y;
}

float mrf(float &x) {
  float y = 0.0;

  if (x > 0.55) {
    y = 1.00;
  }

  return y;
}
