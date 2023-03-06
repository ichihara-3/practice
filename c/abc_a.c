#include <stdio.h>


int main(){
  char buf[5];
  char res[5];
  scanf("%s", buf);
  res[0] = '0';
  for (int i=1; i<4; i++) {
    res[i] = buf[i-1];
  }
  printf("%s\n", res);
}
