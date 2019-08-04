This is a Lisp(Scheme) Interpreter written by Python3.

The original ideas and the source codes are by Peter Norvig.
[(How to Write a (Lisp) Interpreter (in Python))](http://norvig.com/lispy.html)


実際には、日本語の翻訳記事[((Pythonで) 書く (Lisp) インタプリタ)](http://www.aoky.net/articles/peter_norvig/lispy.htm)を参考にした。

As written in the original article, this interpreter NOT implements all of Scheme's specifications.


example:

- fibonacci 

```Scheme
$ python3 lis.py
lis.py>  (define fibo (lambda (n) (if (>= n 2) (+ (fibo (- n 1)) (fibo (- n 2))) 1)))
None
lis.py> (fibo 10)
89
lis.py> (fibo 20)
10946
lis.py> (fibo 30)
1346269
```
