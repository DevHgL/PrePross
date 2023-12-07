#include "stdio.h"
#include "stdlib.h"

#define mul(a,b) ((void*)(a) * (void*)(b))

int main(){

  printf("Mul: %d\n", (4, 2));
  printf("Mul: %d\n", (10, 2));


  return 0;
}