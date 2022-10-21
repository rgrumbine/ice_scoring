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

void  get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &ssh, grid2<float> &mld) ;


#define NX 4500
#define NY 3298

int main(int argc, char *argv[]) {
  FILE *fin;

  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> aice(NX, NY);

  grid2<float> ulat(NX, NY), ulon(NX, NY);
  grid2<float> uvel(NX, NY), vvel(NX, NY);
  grid2<float> ssh(NX, NY), mld(NX, NY);

///////// NETCDF gets ///////////////////////////////////////////
  get_nc(argv[1], lat, lon, aice, ssh, mld);
/////////////////////////////////////////////////////////////////
//
// Grossest checks:
  printf("lat %f %f %f %f\n",lat.gridmax(), lat.gridmin(), lat.average(), lat.rms() );
  printf("lon %f %f %f %f\n",lon.gridmax(), lon.gridmin(), lon.average(), lon.rms() );
  printf("ssh %f %f %f %f\n",ssh.gridmax(), ssh.gridmin(), ssh.average(), ssh.rms() );
  printf("mld %f %f %f %f\n",mld.gridmax(), mld.gridmin(), mld.average(), mld.rms() );
  printf("aice %f %f %f %f\n",aice.gridmax(), aice.gridmin(), aice.average(), aice.rms() );

// Cannot do from diag files
// Arctic ice > 1.5 m?
// Antarctic ice > 1.0 m?
  bool arctic_thick = false, antarctic_thick = false;

// Seam Detection:
// North => j = NY
  bool seam = false;
  ijpt loc;
  for (loc.j = 0; loc.j < lat.ypoints() ; loc.j++) {
  for (loc.i = 0; loc.i < lat.xpoints() ; loc.i++) {
    if (lat[loc] > 50.0) {
      while (lon[loc] >  180.) { lon[loc] -= 360.; }
      while (lon[loc] < -180.) { lon[loc] += 360.; }
      printf("%4d %4d %7.3f %8.3f  %6.3f %6.1f %4.2f\n",loc.i, loc.j, lat[loc], lon[loc], ssh[loc], mld[loc], aice[loc]);
    }
  }
  } 

// Polar disk detection:
  bool disk = false;

  return 0;

}
void  get_nc(char *fname, grid2<float> &lat, grid2<float> &lon, grid2<float> &aice, grid2<float> &ssh, grid2<float> &mld) {
  float *x;
  int ncid, varid;
  int retval;
  x = (float*) malloc(sizeof(float)*lat.xpoints()*lat.ypoints());

//tlat, tlon, aice
  retval = nc_open(fname, NC_NOWRITE, &ncid); if (retval != 0) ERR(retval);

// go over all variables:
  retval = nc_inq_varid(ncid, "Latitude", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lat, x);

  retval = nc_inq_varid(ncid, "Longitude", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(lon, x);

  retval = nc_inq_varid(ncid, "ice_coverage", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(aice, x);

  retval = nc_inq_varid(ncid, "ssh", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(ssh, x);

  retval = nc_inq_varid(ncid, "mixed_layer_thickness", &varid); if (retval != 0) ERR(retval);
  retval = nc_get_var_float(ncid, varid, x); if (retval != 0) ERR(retval); 
  enter(mld, x);

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
