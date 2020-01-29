#include "metric.h"
//Robert Grumbine
//Jan 15  2013

template<class T>
class rtofsg : public metricgrid<T> {
// grid-specific parameters:
// fundamental or derived parameters:

  public :
    rtofsg(void);
    rtofsg(rtofsg<T> &);
    
    inline fijpt& locate(const latpt &); // translate lat-lon to grid ij
    inline latpt locate(const ijpt &);  // translate integer ij to lat-lon
    inline latpt locate(const fijpt &); // translate float ij to lat-lon

  // now start unique:
    void reada(FILE *, int);
    void readb(FILE *);
};

template <class T>
rtofsg<T>::rtofsg(void) {
  this->nx = 4500;
  this->ny = 3298;
  this->grid = new T [this->nx * this->ny];
}
template <class T>
rtofsg<T>::rtofsg(rtofsg<T> &x) {
  this->nx = x.nx;
  this->ny = x.ny;

  if (this->grid != (T *) NULL) {
    delete this->grid;
  }
  this->grid = new T[this->nx*this->ny];
  for (int i = 0; i < this->ny*this->nx; i++) {
    this->grid[i] = x[i];
  }
}

template <class T>
fijpt& rtofsg<T>::locate(const latpt &x) {
// future -- fix locates
  global_fijpt.i = -1;
  global_fijpt.j = -1;
  return global_fijpt;
}
template <class T>
latpt rtofsg<T>::locate(const ijpt &x) {
  latpt ll;
  ll.lat = -99.0;
  ll.lon = 0.0;
  return ll;
}
template <class T>
latpt rtofsg<T>::locate(const fijpt &x) {
  latpt ll;
  ll.lat = -99.0;
  ll.lon = 0.0;
  return ll;
}
template<class T>
void rtofsg<T>::reada(FILE *ina, int nfield) {
  int i;
  rewind(ina);
  for (i = 0; i < nfield; i++) {
    this->binin(ina);
  }
  return;
}

template<class T>
void rtofsg<T>::readb(FILE *inb) {
  char delim = '=';
  int nparms = 17;
  size_t nline = 900;
  char **gline;
  int idm, jdm;
  char parm[900][900];
  char* tparm;
  int i;

  *gline = new char [ 900 ];

  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  getline(gline, &nline, inb);
  printf("%d %s",nline, gline[0]); fflush(stdout);

  getline(gline, &nline, inb);
  sscanf(gline[0], "%d", &idm);
  getline(gline, &nline, inb);
  sscanf(gline[0], "%d", &jdm);
  printf("grid %d %d versus %d %d\n",this->nx, this->ny, idm, jdm); fflush(stdout);

  getline(gline, &nline, inb);
  printf("%s",gline[0]); fflush(stdout);

//  for (i = 0; i < nparms; i++) {
//    parm[i] = new char [ 900 ];
//  }
//  printf("done allocating space for parm\n"); fflush(stdout);

  printf("starting loop\n"); fflush(stdout);
  i = 0; printf("i = %d\n",i); fflush(stdout);
    getline(gline, &nline, inb);
    printf("parm i = %d, line = %s",i,gline[0]); fflush(stdout);
    tparm = strtok(gline[0], &delim);
    strncpy(parm[i], tparm, 90);

//  for (i = 1; i < nparms; i++) {
//    getline(gline, &nline, inb);
//    printf("parm i = %d, line = %s",i,gline[0]); fflush(stdout);
//
//    &parm[i] = strtok(gline[0], &delim);
//    printf("parm %d = %s\n",i,parm[i]);
//  }

  return;
}
//---------------------------------------------------------------------

int main(int argc, char *argv[]) {
  FILE *inb, *ina;
  rtofsg<float> x;

//  inb = fopen(argv[1], "r");
//  x.readb(inb);
//  fclose(inb);

  ina = fopen(argv[1], "r");
  x.reada(ina, 5);
  fclose(ina);
  printf("%f %f %f\n",x.gridmax(), x.gridmin(), x.average() );

  return 0;
}
