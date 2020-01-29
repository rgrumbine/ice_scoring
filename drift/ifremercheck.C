#include <stdio.h>
#include <time.h>

#include "buoy.h"

// Program to check through an IABP buoy file and print out those points 
//   which are near to any skiles point, near 00 UTC, or are a buoy that 
//   _was_ so within some time range (forecast length) of this report.  
// Arguments are space range, time range, forecast length, and 
//   output file name.
// Files forecast.points and dboydata are assumed to exist.

// Robert Grumbine 3 April 2000
// Fixes to span gaps between valid observations which are longer than
//   the forecast interval input.
// Robert Grumbine 11 January 2001
//
// Revised/variant for IFREMER inputs 1 April 2014
//   use bools for FALSE, TRUE


#define SKILES 207
#define MAXBUOYS 45000
#define ndays 16

#include "subs.C"
extern "C" void ssanaly_(float *odist, float *odir, float *dist, float *dir,
                              int &npts, float &ia, float &r2, float &vcc);
extern "C" void fit_(float *odist, float *dist, int &n, float &b0, float &b1,
                     float &correl);
extern "C" float wdir_(float &dx, float &dy, float &fdummy);

class ifremer {
  public:
    float lat1, lat2, lon1, lon2;
    time_t obs_secs;
    int year, month, day;
    float hour;
    float dist, dir;
  private:
    tm obs_time;
    static time_t time_range;
    static float  space_range;
  public:
    ifremer(void);
    ~ifremer() {};
    void read(FILE*) ;

// Resetting default ranges:
    void set_space_range(const float y) { space_range = y; }
    void set_time_range(const time_t y) { time_range = y; }

    // Time functions:
    void   set_time();
    tm     get_time() { return this->obs_time; }
    time_t get_secs() { return this->obs_secs; }
    void   set_secs(const time_t &x) { this->obs_secs = x; }
    bool near(tm &, time_t);

    bool poleward(float cutoff) {
      if (cutoff > 0.) { return ( (this->lat1 >= cutoff) || (this->lat2 >= cutoff)) ; }
      else { return ( (this->lat1 <= cutoff) || (this->lat2 <= cutoff) )  ; }
    }
    bool synoptic(float del) { return (hour <= del || (24. - hour) <= del) ; }
    bool near(ifremer &x, time_t toler) {
      return this->near(x.obs_time, toler);
    }
    bool near(latpt &x, float toler) {
      if (fabs(x.lat - this->lat1)*parameters::km_per_degree > toler) { return false; }
      else {
        return (fabs(arcdis_(x.lon, x.lat, lon1, lat1)) < toler) ;
      }
    }
    bool near(ifremer &x, float toler) {
      if (fabs(x.lat1 - this->lat1)*parameters::km_per_degree > toler) { return false; }
      else {
        return (fabs(arcdis_(x.lon1, x.lat1, this->lon1, this->lat1))
                 < toler) ;
      }
    }
    bool near(ifremer &x, time_t toler, float distance) { return
      (this->near(x.obs_time,toler) && this->near(x, distance) ); }

// Start thinking about QC:
    bool ok(void) {
      return ( ( fabs(lat1) <= 90.0) && (fabs(lat2) <= 90.0) ) ;
    }

};
// defined in buoy.h:
// time_t fn(int yy, int mm, int dd) { tm tmp;
//         tmp.tm_year = yy; tmp.tm_mon  = mm - 1;
//         tmp.tm_mday = dd;  tmp.tm_hour = 0;
//         tmp.tm_min  = 0;    tmp.tm_sec  = 0;
//         return mktime(&tmp);
//         }
time_t ifremer::time_range = (time_t)3600;
float  ifremer::space_range = 50.0;

//////////////////////// Begin support code:
void ifremer::set_time() {
//construct an obs time, given that there are month day year entries already
// in the buoy report.
  obs_time.tm_year = year;
  obs_time.tm_mon     = month - 1;
  obs_time.tm_mday    = day;
  obs_time.tm_hour    = (int) hour;
  obs_time.tm_min     = (int) (60.*(hour - (int)hour) );
  obs_time.tm_sec     = (int) (3600.*(hour - (int)hour) - 60*obs_time.tm_min);
  obs_secs = mktime(&obs_time);
}

ifremer::ifremer(void) {
  obs_time.tm_sec = 0;
  obs_time.tm_min = 0;
  obs_time.tm_hour = 0;
  obs_time.tm_mday = 0;
  obs_time.tm_mon = 0;
  obs_time.tm_year = 0;
  obs_time.tm_wday = 0;
  obs_time.tm_yday = 0;
  obs_time.tm_isdst = 0;
  obs_secs = mktime(&obs_time);
}

bool ifremer::near(tm &x, time_t toler) {
  time_t t1, t2;

  t1 = this->obs_secs;
  t2 = mktime(&x );
  if ( abs(t2-t1) > toler || t1 < 0 || t2 < 0 ) {
    return false;
  }
  else {
    return true;
  }
}
void ifremer::read(FILE *fin) {
  float tlat1, tlat2, tlon1, tlon2, dx, dy, fdummy;
  int tn, td;
  fscanf(fin, "%d %f %f %f %f %d\n",&tn, &tlat1, &tlon1, &tlat2, &tlon2, &td);
  if ( fabs(tlon2 - tlon1) > 180.) {

  }
  this->lat1 = tlat1;
  this->lat2 = tlat2;
  this->lon1 = tlon1;
  this->lon2 = tlon2;

  dist = ARCDIS(tlon1, tlat1, tlon2, tlat2);
  dx = (tlon2-tlon1)*cos((tlat1+tlat2)/2.*parameters::radians_per_degree);
  dy = tlat2-tlat1;
  dir = wdir_(dx, dy, fdummy);
  if (dx == 0. && dy == 0.) dir = 0.;
  //printf("r %8.4f %9.4f %8.4f %9.4f  %6.2f  %7.4f %7.4f %5.1f\n",
  //            tlat1, tlon1, tlat2, tlon2, dist, dx, dy, dir);
} 



    


int main(int argc, char *argv[]) {
  FILE *fin1, *fin2, *fout, *fcstin;
  latpt loc[SKILES];
  ifremer buoy, near_buoys[MAXBUOYS];
  int i, nnear = 0, skileno, fcst_length;
  float lat, lon, space, time;

  time_t deltat;

  float dir[ndays][SKILES], dist[ndays][SKILES];
  int retcode, date;
  float odir[MAXBUOYS], odist[MAXBUOYS], fdir[MAXBUOYS], fdist[MAXBUOYS];



/////////////////////////////////////////////////////////
// Set up arguments/control values.
  space = atof(argv[1]);
  time  = atof(argv[2]);
  deltat = (time_t) (3600 * time);
  fcst_length = atoi(argv[3]);
  //printf("Space limit = %f\n",space);
  //printf("deltat = %d\n",(int) deltat);
  //printf("forecast lead %d\n",fcst_length);
  //printf("Size of a buoy report %d\n",(int) sizeof(ifremer) );
  fflush(stdout);
  fout = fopen(argv[4],"w+");
  if (fout == (FILE*) NULL) {
    printf("Failed to open %s for reading and writing \n",argv[4]);
    return 1;
  }
  fcstin = fopen(argv[5], "r");
  if (fcstin == (FILE*) NULL) {
    printf("Failed to open forecast file %s for reading \n",argv[5]);
    return 1;
  }

/////////////////////////////////////////////////////////
//Read in all skiles points
  fin1=fopen("forecast.points","r");
  if (fin1 == (FILE *) NULL) {
    printf("Failed to open the forecast.points file, exiting\n");
    return 1;
  }  
  i = 0;
  while (!feof(fin1) ) {
    fscanf(fin1, "%d %f %f\n",&skileno, &lat, &lon);
    i += 1;
    loc[skileno-1].lat = lat;
    loc[skileno-1].lon = lon;
  }
  fclose(fin1);
  //printf("i at end of while loop skiles pt. read %d\n",i);
  fflush(stdout);

// Read in the forecast -- retcode is number of days found:
  getfcst(date, fcstin, &dir[0][0], &dist[0][0], retcode);
  //printf("retcode = %d\n",retcode); fflush(stdout);


/////////////////////////////////////////////////////////
// Now read through buoy file and see what matchups we find
  fin2 = fopen("dboydata","r");
  if (fin2 == (FILE *) NULL) {
    printf("Failed to find the required input file 'dboydata'\n");
    return 1;
  }
  rewind(fin2);
  nnear = 0;

  while (!feof(fin2)) {
    buoy.read(fin2);

//If we're near to a skiles point write out the data report
//  Note that the feature tracking is limited in precision and slow motions are
//    not reliable.  Minimum quantization is about 5 km, so require this 
//    and ignore zeroes, which may be either no motion or below observation threshold.
    for (skileno = 0; (skileno < SKILES) ; skileno++) {
      if (buoy.near(loc[skileno], space) && buoy.dist > 5.0 ) {
        near_buoys[nnear] = buoy;
        fprintf(fout,"%3d %5.2f %6.2f   %6.2f %6.2f  %6.2f %6.2f\n",skileno+1, 
                  buoy.lat1, buoy.lon1, buoy.dir, buoy.dist,
                  dir[fcst_length-1][skileno], 
                  dist[fcst_length-1][skileno]*parameters::nmtokm);
        fflush(fout);
        // copy over to observed and forecast values
        odir[nnear]  = buoy.dir;
        odist[nnear] = buoy.dist;
        fdir[nnear]  = dir[fcst_length-1][skileno];
        fdist[nnear] = dist[fcst_length-1][skileno]*parameters::nmtokm;
        nnear += 1;
      }
    }

  } //end while
  //printf("Total near obs: %d\n",nnear);
  fclose(fin2);


// Can now begin scoring:
  float ia, correl, vcc;
  float b0, b1;
  float meandist, meandir, rmsdist, rmsdir, errad, erradrms;

// bulk scoring:
  ssanaly_(odist, odir, fdist, fdir, nnear, ia, correl, vcc);
  printf("%5.1f %5d %2d %6.3f %6.3f %6.3f",space, nnear, (int) fcst_length, ia, correl, vcc);
  fit_(fdist, odist, nnear, b0, b1, correl);
  printf("  %6.2f %6.3f", b0, b1);
  rms(odist, odir, fdist, fdir, nnear, meandist, meandir, rmsdist,
                       rmsdir, errad, erradrms);
  printf("  %6.2f %6.1f  %5.1f %5.1f %5.1f %5.1f\n",meandist, meandir, rmsdist,
                       rmsdir, errad, erradrms);



  return 0;
}
