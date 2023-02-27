// mmablib supports:

#include "points.h"
#include "mvector.h"
#include "grid_base.h"

latpt locate(grid2<float> &lat, grid2<float> &lon, fijpt &z) ;
latpt locate(mvector<float> &lat, mvector<float> &lon, fijpt &z) ;

latpt locate(grid2<float> &lat, grid2<float> &lon, fijpt &z) {
  ijpt loc1, loc2;
  latpt ll1, ll2;

  loc1.i = floor(z.i);
  loc1.j = floor(z.j);
  loc2.i = ceil(z.i);
  loc2.j = ceil(z.j);

  ll1.lat = lat[loc1];
  ll2.lat = lat[loc2];
  ll1.lon = lon[loc1];
  ll2.lon = lon[loc2];

  if (ll1.lon < -180.) ll1.lon += 360.;
  if (ll2.lon < -180.) ll2.lon += 360.;
  if (ll1.lon >  180.) ll1.lon -= 360.;
  if (ll2.lon >  180.) ll2.lon -= 360.;

  ll1.lat = (ll1.lat + ll2.lat)/2.0;
  ll1.lon = (ll1.lon + ll2.lon)/2.0;

  return ll1;
}
latpt locate(mvector<float> &lat, mvector<float> &lon, fijpt &z) {
  ijpt loc1, loc2;
  latpt ll1, ll2;

  loc1.i = floor(z.i);
  loc1.j = floor(z.j);
  loc2.i = ceil(z.i);
  loc2.j = ceil(z.j);

  ll1.lat = lat[loc1.j];
  ll2.lat = lat[loc2.j];
  ll1.lon = lon[loc1.i];
  ll2.lon = lon[loc2.i];

  if (ll1.lon < -180.) ll1.lon += 360.;
  if (ll2.lon < -180.) ll2.lon += 360.;
  if (ll1.lon >  180.) ll1.lon -= 360.;
  if (ll2.lon >  180.) ll2.lon -= 360.;

  ll1.lat = (ll1.lat + ll2.lat)/2.0;
  ll1.lon = (ll1.lon + ll2.lon)/2.0;

  return ll1;
}
