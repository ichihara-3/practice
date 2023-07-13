#include <stdint.h>
#include <stdio.h>


uint32_t mul125(uint16_t a) {
  uint32_t t = 0;
  *(uint16_t*)((uint8_t*)&t + 1) = a;
  t >>= 1;
  t -= ( a << 1 ) + a;
  return t;
}


int main(void){
  // result: 1250000
  printf( "%d\n", mul125( 10000 ) );
}
