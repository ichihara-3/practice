public class Calculate {
  int a;
  int b;


  public Calculate(int x, int y) {
    this.a = x;
    this.b = y;
  }

  public int add() {
    int res = a + b;
    return res;
  }


  public int subtract () {
    int res = a - b;
    return res;
  }

  public int multiply () {
    int res = a * b;
    return res;
  }

  public int divide () {
    int res = a/b;
    return res;
  }

  public static void main(String[] args) {
    Calculate c1 = new Calculate(45, 4);

    System.out.println("Addition is:" + c1.add());
    System.out.println("Subtraction is:" + c1.subtract());
    System.out.println("Multiplication is:" + c1.multiply());
    System.out.println("Division is:" + c1.divide());
  }
}
