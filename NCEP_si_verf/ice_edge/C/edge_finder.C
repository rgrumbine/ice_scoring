#include "metric.h"

void edge_finder(metricgrid<float> &conc, grid2<int> &land, float conc_toler ) ;
void edge_finder(metricgrid<float> &conc, grid2<float> &dist, float conc_toler, float dist_toler) ;

void edge_finder(grid2<float> &conc, mvector<float> &lat, mvector<float> &lon, float conc_toler) ;
void edge_finder(grid2<float> &conc,   grid2<float> &lat,   grid2<float> &lon, float conc_toler ) ;
/////////////////////////////////////////////////////////////////////////////////
void midpoint(ijpt &x, ijpt &y, fijpt &z);
void midpoint(ijpt &x, ijpt &y, fijpt &z) {
  z.i = (float)x.i + (float)y.i;
  z.j = (float)x.j + (float)y.j;
  z /= 2.0;
  return;
}

/////////////////////////////////////////////////////////////////////////////////
void edge_finder(grid2<float> &conc, grid2<float> &lat, grid2<float> &lon, float conc_toler ) {
  latpt ll;
  fijpt z;
  ijpt loc, im, ip, jm, jp;
  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    jp.j = min(loc.j+1, conc.ypoints()-1);
    jm.j = max(loc.j-1, 0);
    ip.j = loc.j;
    im.j = loc.j;
    for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
      jp.i = loc.i;
      jm.i = loc.i;
      ip.i = min(loc.i + 1, conc.xpoints()-1);
      im.i = max(loc.i - 1, 0);
      if (conc[loc] >= conc_toler && conc[im] < conc_toler) {
        midpoint(loc, im, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[ip] < conc_toler) {
        midpoint(loc, ip, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jm] < conc_toler) {
        midpoint(loc, jm, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jp] < conc_toler) {
        midpoint(loc, jp, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
    }
  }
  return;
}

void edge_finder(metricgrid<float> &conc, grid2<int> &land, float conc_toler ) {
  latpt ll;
  fijpt z;
  ijpt loc, im, ip, jm, jp;

  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    jp.j = min(loc.j+1, conc.ypoints()-1);
    jm.j = max(loc.j-1, 0);
    ip.j = loc.j;
    im.j = loc.j;
    for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
      if (land[loc] != 0) continue;
      jp.i = loc.i;
      jm.i = loc.i;
      ip.i = min(loc.i + 1, conc.xpoints()-1);
      im.i = max(loc.i - 1, 0);
      if (conc[loc] >= conc_toler && conc[im] < conc_toler && land[im] == 0) {
        midpoint(loc, im, z); ll = conc.locate(z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[ip] < conc_toler && land[ip] == 0) {
        midpoint(loc, ip, z); ll = conc.locate(z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jm] < conc_toler && land[jm] == 0) {
        midpoint(loc, jm, z); ll = conc.locate(z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jp] < conc_toler && land[jp] == 0) {
        midpoint(loc, jp, z); ll = conc.locate(z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
    }
  }
  return;
}

void edge_finder(metricgrid<float> &conc, grid2<float> &dist, float conc_toler, float dist_toler) { 
  latpt ll;
  fijpt z;
  ijpt loc, im, ip, jm, jp;

  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    jp.j = min(loc.j+1, conc.ypoints()-1);
    jm.j = max(loc.j-1, 0);
    ip.j = loc.j;
    im.j = loc.j;
    for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
      jp.i = loc.i; 
      jm.i = loc.i;
      ip.i = min(loc.i + 1, conc.xpoints()-1);
      im.i = max(loc.i - 1, 0);
      if (conc[loc] >= conc_toler && conc[im] < conc_toler && dist[loc] > dist_toler) {
        midpoint(loc, im, z); ll = conc.locate(z);
        if (ll.lon > 180.) ll.lon -= 360.;
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[ip] < conc_toler && dist[loc] > dist_toler) {
        midpoint(loc, ip, z); ll = conc.locate(z);
        if (ll.lon > 180.) ll.lon -= 360.;
        printf("%f %f\n",ll.lon, ll.lat);
      } 
      if (conc[loc] >= conc_toler && conc[jm] < conc_toler && dist[loc] > dist_toler) {
        midpoint(loc, jm, z); ll = conc.locate(z);
        if (ll.lon > 180.) ll.lon -= 360.;
        printf("%f %f\n",ll.lon, ll.lat);
      } 
      if (conc[loc] >= conc_toler && conc[jp] < conc_toler && dist[loc] > dist_toler) {
        midpoint(loc, jp, z); ll = conc.locate(z);
        if (ll.lon > 180.) ll.lon -= 360.;
        printf("%f %f\n",ll.lon, ll.lat);
      } 
    }   
  }  

  return;
}
void edge_finder(grid2<float> &conc, mvector<float> &lat, mvector<float> &lon, float conc_toler) { 
// Look for ice edge, defined by a concentration tolerance / critical value
  latpt ll;
  fijpt z;
  ijpt loc, im, ip, jm, jp;

  for (loc.j = 0; loc.j < conc.ypoints(); loc.j++) {
    jp.j = min(loc.j+1, conc.ypoints()-1);
    jm.j = max(loc.j-1, 0);
    ip.j = loc.j;
    im.j = loc.j;
    for (loc.i = 0; loc.i < conc.xpoints(); loc.i++) {
      jp.i = loc.i;
      jm.i = loc.i;
      ip.i = min(loc.i + 1, conc.xpoints()-1);
      im.i = max(loc.i - 1, 0);
      if (conc[loc] >= conc_toler && conc[im] < conc_toler) {
        midpoint(loc, im, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[ip] < conc_toler) {
        midpoint(loc, ip, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jm] < conc_toler) {
        midpoint(loc, jm, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
      if (conc[loc] >= conc_toler && conc[jp] < conc_toler) {
        midpoint(loc, jp, z); ll = locate(lat, lon, z);
        printf("%f %f\n",ll.lon, ll.lat);
      }
    }
  }

  return;
}
