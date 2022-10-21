#include <stdio.h>
#include <stdlib.h>
//Robert Grumbine
//8 June 2018

#include "netcdf.h"
/* Handle errors by printing an error message and exiting with a
 * non-zero status. */
#define ERRCODE 2
#define ERR(e) {printf("Error: %s\n", nc_strerror(e)); exit(ERRCODE);}

#include "ncepgrids.h"
void enter(grid2<float> &param, float *x) ;
void get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &hi, grid2<float> &sst);

bool seamer(grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, float epsilon) ;

#define NX 4500
#define NY 3297

int main(int argc, char *argv[]) {
  FILE *fin;

  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> aice(NX, NY), hi(NX, NY);
  grid2<float> sst(NX, NY);

  grid2<float> ulat(NX, NY), ulon(NX, NY);
  grid2<float> uvel(NX, NY), vvel(NX, NY);

  global_12th<float> obs;
  global_12th<unsigned char> skip;

// Get observations:
  fin = fopen(argv[1], "r");
  obs.binin(fin);
  fclose(fin);

  // get skip mask
  fin = fopen(argv[2], "r");
  skip.binin(fin);
  fclose(fin);

///////// NETCDF gets ///////////////////////////////////////////
  get_nc(argv[3], lat, lon, aice, hi, sst);
/////////////////////////////////////////////////////////////////

// Polar disk detection:

// Seam Detection:
//   last argument is an 'epsilon', ignore points where loc1, 2,3 are all < epsilon
  printf("calling seamer with aice\n");
  seamer(aice, lat, lon, 0.001);
  printf("calling seamer with hi\n");
  seamer(hi, lat, lon, 0.01);
  printf("calling seamer with sst\n");
  seamer(sst, lat, lon, -3.);
//sss, Tair, 



// Arctic ice > 1.5 m?
// Antarctic ice > 1.0 m?
  bool arctic_thick = false, antarctic_thick = false;

  return 0;
}
void  get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &hi, grid2<float> &sst) {
  float *x;
  int ncid, varid;
  int retval;
  x = (float*) malloc(sizeof(float)*lat.xpoints()*lat.ypoints());

//tlat, tlon, aice, hi
  retval = nc_open(fname, NC_NOWRITE, &ncid); if (retval != 0) ERR(retval);

// go over all variables:
  retval = nc_inq_varid(ncid, "TLAT", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lat, x);

  retval = nc_inq_varid(ncid, "TLON", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lon, x);

  retval = nc_inq_varid(ncid, "aice", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(aice, x);

  retval = nc_inq_varid(ncid, "hi", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(hi, x);

  retval = nc_inq_varid(ncid, "sst", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(sst, x);

// close when done:
  retval = nc_close(ncid); if (retval != 0) ERR(retval);

  return;
}
void enter(grid2<float> &param, float *x) {
  ijpt loc;
  for (loc.j = 0; loc.j < param.ypoints(); loc.j++) {
  for (loc.i = 0; loc.i < param.xpoints(); loc.i++) {
    if (x[loc.i+ NX*loc.j] > 1e30) x[loc.i+ NX*loc.j] = 0;
    param[loc] = x[loc.i+ NX*loc.j];
  }
  }

  return;
}
bool seamer(grid2<float> &aice, grid2<float> &lat, grid2<float> &lon, float epsilon) {
  bool seam = false;
  ijpt loc1, loc2, loc1p,loc2p, loc3, loc3p;
  double rms1 = 0.0, rms2 = 0.0, rms3 = 0.0;
  int count = 0;

  loc1.j = 3295; // j for seam check
  loc2.j = 3294; // gradients should be comparable at adjacent lines
  loc3.j = 3293;
  loc1p.j = 3296; // j+1 for seam check
  loc2p.j = 3295; // 
  loc3p.j = 3294; // 
  for (loc1.i = 0; loc1.i < lat.xpoints() ; loc1.i++) {
    loc2.i  = loc1.i;
    loc3.i  = loc1.i;
    loc1p.i = loc1.i;
    loc2p.i = loc1.i;
    loc3p.i = loc1.i;
    if (lat[loc1] > 76.0 
        && (fabs(aice[loc1]) > epsilon && 
            fabs(aice[loc2]) > epsilon && 
            fabs(aice[loc3]) > epsilon) ) {
      //#ifdef DEBUG
          printf("seamcheck %4d %4d %7.3f %8.3f  %4.2f %4.2f %4.2f  %5.2f %5.2f %5.2f\n",
                         loc1.i, loc1.j, lat[loc1], lon[loc1],
                 aice[loc1], aice[loc2], aice[loc3], aice[loc1p]-aice[loc1], aice[loc2p]-aice[loc2],
                 aice[loc3p] - aice[loc3] );
      //#endif
      rms1 += (aice[loc1p]-aice[loc1])*(aice[loc1p]-aice[loc1]);
      rms2 += (aice[loc2p]-aice[loc2])*(aice[loc2p]-aice[loc2]);
      rms3 += (aice[loc3p]-aice[loc3])*(aice[loc3p]-aice[loc3]);
      count += 1;
      }
    }
                                                                                             printf("seam rmses %f %f %f\n",sqrt(rms1/count), sqrt(rms2/count), sqrt(rms3/count) );
  if (sqrt(rms1/count) > 0.10 && sqrt(rms1/count) > 2.*sqrt(rms2/count)) seam = true;      
  return seam;
}
