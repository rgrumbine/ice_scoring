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

#include "grid_math.h"
#include "netcdf.h"

#define GLACIAL 0
#define TROPICAL 1
#define LAST_YEAR 2
#define COND_AVG  3
#define UNCOND_AVG 4
#define PERSISTENCE 5
#define ANALOG 6
#define CLIPER 7

// Utilities -- 
//   the GFS is (~2017-present) applying a filter in the northern hemisphere that 
//      zeroes ice concentration below 0.40
//   the MRF (1997-~2017) applied a filter such that ice concentrations 
//      below 0.55 were set to 0, and those above were set to 1.0
float gfs(float &x);
float mrf(float &x);


// level 0 nulls -- completely ignorant nulls
template<class T>
void null(grid2<T> &x, int sort) ;

// level 1 nulls -- knows history in general but nothing recent
template<class T>
void null(grid2<T> &x, int sort, FILE *fin, int jday) ;
// the file is a netcdf file, 1 time per day for the previous year
// rely on the file to have the 365 or 366 time levels, as needed

// level 2 
template<class T>
void null(grid2<T> &x, grid2<T> &observed) ;

// level 3
template<class T>
void null(grid2<T> &x, int sort, FILE *fin) ;

