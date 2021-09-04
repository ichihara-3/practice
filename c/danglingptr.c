#include <stdio.h>

typedef struct Point {
  int x;
  int y;
} point_t;

point_t *get_point(void) {
  point_t p = {10, 10};
  return &p;
}

int main(void) {
  point_t *p = get_point();
  printf("%d, %d\n", p->x, p->y);
}
