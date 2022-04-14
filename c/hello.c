#include <stdio.h>
#include <string.h>

typedef struct {
  int a;
  int b;
} var;

int dump(void *myStruct, long size) {
  unsigned int i;
  const unsigned char *const px = (unsigned char *)myStruct;
  for (i = 0; i < size; ++i) {
    // line number
    if (i % (sizeof(int) * 8) == 0) {
      printf("\n%08lX: ", i / sizeof(int) / 8);
    } else if (i % 4 == 0) {
      printf(" ");
    }
    printf("%02X", px[i]);
  }

  printf("\n\n");
  return 0;
}

int main() {
  char line[100];
  char *fmt = "Hello, %s\n";
  char *name = "World";
  snprintf(line, strlen(fmt) - 2 + strlen(name), fmt, name);
  puts(line);

  var x;
  x.a = 1;
  x.b = 2;
  var *p = &x;

  printf("x.a=%d, p->b=%d\n", x.a, p->b);

  struct hoge {
    int a;
    char b;
  } a = {1, 'a'}, b = {2, 'b'};

  __builtin_dump_struct(&a, &printf);
  __builtin_dump_struct(&b, &printf);

  struct hoge c = {2, 'c'};
  __builtin_dump_struct(&c, &printf);

  dump(&a, sizeof(a));
  dump(&b, sizeof(b));
  dump(&c, sizeof(c));

  struct fuga {
    int a;
    int b;
    int c;
    int d;
    int e;
    int f;
    int g;
    int h;
    int i;
    int j;
  } z = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
  dump(&z, sizeof(z));
}
