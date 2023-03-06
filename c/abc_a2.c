#include <stdio.h>
int main(int a, char **v) {
  gets((char *)&a);
  a = a << 8 | 48;
  puts((char *)&a);
}
