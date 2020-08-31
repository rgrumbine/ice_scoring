#include "ncepgrids.h"

#include "nulls.C"

int main(void) {
  global_12th<float> conc, null_conc;

  conc.set((float)0.5);
  printf("conc: %f %f %f %f\n",conc.gridmax(), conc.gridmin(), 
     conc.average(), conc.rms() );

  null(null_conc, GLACIAL);
  printf("null: %f %f %f %f\n",null_conc.gridmax(), null_conc.gridmin(), 
     null_conc.average(), null_conc.rms() );
  
  null(null_conc, TROPICAL);
  printf("null: %f %f %f %f\n",null_conc.gridmax(), null_conc.gridmin(), 
     null_conc.average(), null_conc.rms() );
  
  return 0;
}
