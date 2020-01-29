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
void gradient(grid2<float> &lat, grid2<float> &lon, grid2<float> &x, float &dellimit, llgrid<float> &dist_land);


#define NX 4500
#define NY 3298

int main(int argc, char *argv[]) {
  grid2<float> lat(NX, NY), lon(NX, NY);
  grid2<float> aice(NX, NY);
  grid2<float> ssh(NX, NY), mld(NX, NY);
  global_12th<float> dist_land;

  FILE *fin;
  fin = fopen(argv[2],"r");
  dist_land.binin(fin);
  fclose(fin);
///////// NETCDF gets ///////////////////////////////////////////
  get_nc(argv[1], lat, lon, aice, ssh, mld);
/////////////////////////////////////////////////////////////////
//
// Grossest checks:
  enum var {LAT, LON, SSH, MLD, AICE };
  float lower_bound[5] = {-80., -400., -2.1,   0.0, 0.0};
  float upper_bound[5] = { 90., 2000.,  2.1, 2100., 1.0}; 
  float dellimit[5]    = { 0.1,    1.,  0.75, 100., 0.08}; // gradient limit, ij space 

  printf("lat %f %f %f %f\n",lat.gridmax(), lat.gridmin(), lat.average(), lat.rms() );
  printf("lon %f %f %f %f\n",lon.gridmax(), lon.gridmin(), lon.average(), lon.rms() );
  printf("ssh %f %f %f %f\n",ssh.gridmax(), ssh.gridmin(), ssh.average(), ssh.rms() );
  printf("mld %f %f %f %f\n",mld.gridmax(), mld.gridmin(), mld.average(), mld.rms() );
  printf("aice %f %f %f %f\n",aice.gridmax(), aice.gridmin(), aice.average(), aice.rms() );
  if (lat.gridmax() > 90.0) {
    printf("latitude off the planet! max = %f\n",lat.gridmax() );
    return 1;
  }

  ijpt loc;
  bool sshok = true, mldok = true, aiceok = true;
  int sshcount = 0, mldcount = 0, aicecount = 0;
  for (loc.j = 0; loc.j < lat.ypoints() ; loc.j++) {
  for (loc.i = 0; loc.i < lat.xpoints() ; loc.i++) {
    if (ssh[loc] < lower_bound[SSH] || ssh[loc] > upper_bound[SSH]) {
      sshok=false; sshcount++;
      printf("ssh out of range %f to %f at %f %f, val = %f\n",lower_bound[SSH], upper_bound[SSH],
         lat[loc], lon[loc], ssh[loc]);
    }
    if (mld[loc] < lower_bound[MLD] || mld[loc] > upper_bound[MLD]) {
      mldok=false; mldcount++;
      printf("mld out of range %f to %f at %f %f, val = %f\n",lower_bound[MLD], upper_bound[MLD],
         lat[loc], lon[loc], mld[loc]);
    }
    if (aice[loc] < lower_bound[AICE] || aice[loc] > upper_bound[AICE]) {
      aiceok=false; aicecount++;
      printf("aice out of range %f to %f at %f %f, val = %f\n",lower_bound[AICE], upper_bound[AICE],
         lat[loc], lon[loc], aice[loc]);
    }
  }
  }
  if (! (aiceok && mldok && sshok)) {
    printf("aice mld ssh error counts: %d %d %d\n",aicecount, mldcount, sshcount);
  }

// Cannot do from diag files
// Arctic ice > 1.5 m?
// Antarctic ice > 1.0 m?
  bool arctic_thick = false, antarctic_thick = false;

// Seam Detection:
// North => j = NY
  bool seam = false;
  ijpt loc1, loc2, loc1p,loc2p, loc3, loc3p;
  double rms1 = 0.0, rms2 = 0.0, rms3 = 0.0;
  int count = 0;
  loc1.j = 3296; // j for seam check
  loc2.j = 3295; // gradients should be comparable at adjacent lines
  loc3.j = 3294;
  loc1p.j = 3297; // j+1 for seam check
  loc2p.j = 3296; // 
  loc3p.j = 3295; // 
  for (loc1.i = 0; loc1.i < lat.xpoints() ; loc1.i++) {
    loc2.i  = loc1.i; 
    loc3.i  = loc1.i; 
    loc1p.i = loc1.i; 
    loc2p.i = loc1.i; 
    loc3p.i = loc1.i; 
    if (lat[loc1] > 76.0 && (aice[loc1] != 0 && aice[loc2] != 0 && aice[loc3] != 0) ) {
      #ifdef DEBUG
      printf("seamcheck %4d %4d %7.3f %8.3f  %4.2f %4.2f %4.2f  %5.2f %5.2f %5.2f\n",
               loc1.i, loc1.j, lat[loc1], lon[loc1], 
               aice[loc1], aice[loc2], aice[loc3], aice[loc1p]-aice[loc1], aice[loc2p]-aice[loc2],
               aice[loc3p] - aice[loc3] );
      #endif
      rms1 += (aice[loc1p]-aice[loc1])*(aice[loc1p]-aice[loc1]);
      rms2 += (aice[loc2p]-aice[loc2])*(aice[loc2p]-aice[loc2]);
      rms3 += (aice[loc3p]-aice[loc3])*(aice[loc3p]-aice[loc3]);
      count += 1;
    }
  }
  printf("seam rmses %f %f %f\n",sqrt(rms1/count), sqrt(rms2/count), sqrt(rms3/count) );

//  printf("Lat: "); gradient(lat, lon, lat, dellimit[LAT], dist_land);
//  printf("Lon: "); gradient(lat, lon, lon, dellimit[LON], dist_land);
  printf("SSH: ");  gradient(lat, lon, ssh, dellimit[SSH], dist_land);
  printf("MLD: ");  gradient(lat, lon, mld, dellimit[MLD], dist_land);
  printf("Aice: "); gradient(lat, lon, aice, dellimit[AICE], dist_land);


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
void gradient(grid2<float> &lat, grid2<float> &lon, grid2<float> &x, float &dellimit, llgrid<float> &dist_land) {
//void gradient(grid2<float> &lat, grid2<float> &lon, grid2<float> &x, 
//                                 grid2<float> &dx, grid2<float> &dy) {

//Gradient in ij space for now
  ijpt loc, locip, locjp;
  latpt ll;
  fijpt floc, flocip, flocjp;
  grid2<float> dx(lat.xpoints(), lat.ypoints());
  grid2<float> dy(lat.xpoints(), lat.ypoints());
  float xrms, yrms, flag = 999.;
  bool more_flag = true;
  float land_min = 20.*1000.; // meters you must be away from land

  dx.set((float) 0.);
  dy.set((float) 0.);

  for (loc.j = 0; loc.j < x.ypoints()-1; loc.j++) {
    locip.j = loc.j ;
    locjp.j = loc.j + 1;
  for (loc.i = 0; loc.i < x.xpoints()-1; loc.i++) {
    locip.i = loc.i + 1;
    locjp.i = loc.i;

    ll.lat = lat[loc]; ll.lon = lon[loc];
    floc = dist_land.locate(ll);
    ll.lat = lat[locip]; ll.lon = lon[locip];
    flocip = dist_land.locate(ll);
    ll.lat = lat[locjp]; ll.lon = lon[locjp];
    flocjp = dist_land.locate(ll);

    if (dist_land[floc] > land_min && dist_land[flocip] > land_min && dist_land[flocjp] > land_min) {
      dx[loc] = x[locip] - x[loc];
      dy[loc] = x[locjp] - x[loc];
    }
  }
  }
  printf("dx gradient stats %f %f %f %f \n",dx.gridmax(), dx.gridmin(), dx.average(), dx.rms() );
  printf("    dy gradient stats %f %f %f %f \n",dy.gridmax(), dy.gridmin(), dy.average(), dy.rms() );
  fflush(stdout);

    more_flag = false;
    xrms = dx.rms(flag);
    yrms = dy.rms(flag);

    for (loc.j = 0; loc.j < x.ypoints()-1; loc.j++) {
      locip.j = loc.j ;
      locjp.j = loc.j + 1;
    for (loc.i = 0; loc.i < x.xpoints()-1; loc.i++) {
      locip.i = loc.i + 1;
      locjp.i = loc.i;

      if (( fabs(dx[loc]) > dellimit || fabs(dy[loc]) > dellimit) && 
                (dx[loc] != flag && dy[loc] != flag ) ) {
        printf("overrms %d %d  %7.3f %8.3f  %f %f  %f %f  %f %f %f\n",loc.i, loc.j, lat[loc], lon[loc],
                        dx[loc], xrms, dy[loc], yrms, x[loc], x[locip], x[locjp]);
        fflush(stdout);
        dx[loc] = flag;
        dy[loc] = flag;
        more_flag = true;
      }
    }
    }
    printf("    new dx gradient stats %f %f %f %f \n",
                dx.gridmax(flag), dx.gridmin(flag), dx.average(flag), dx.rms(flag) );
    printf("    new dy gradient stats %f %f %f %f \n",
                dy.gridmax(flag), dy.gridmin(flag), dy.average(flag), dy.rms(flag) );

  return;
}
