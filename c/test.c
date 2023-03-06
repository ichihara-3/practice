#include <stdio.h>
#include <stdlib.h>

int main(){
  int n;
  scanf("%d", &n);
  long array[n];
  for (int i = 0; i < n; i++){
    scanf("%ld", &(array[i]));
  }
  printf("%lu\n", sizeof(array) / sizeof(long));
  for (int i = 0; i < sizeof(array)/sizeof(long); i++) {
    printf("%ld\n", array[i]);
  }
}
