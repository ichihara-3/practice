#include <stdio.h>
#include <string.h>

int main(void) {
  char* string = "Foo Bar Fizz Bazz";
  char* match1 = "Bar";
  char* p1;

  p1 = strstr(string, match1);
  printf("%s\n", p1);

  char* match2 = "bar";
  char* p2;
  p1 = strstr(string, match2);
  printf("%s\n", p1);
  p2 = strcasestr(string, match2);
  printf("%s\n", p2);
}
