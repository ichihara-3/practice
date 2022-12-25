double x = x + x
quadruple x = double (double x)
factorial n = product [1..n]
average ns = sum ns `div` length ns

a = b + c
  where
    b = 5
    c = 10

d = a * 2

z = double a

n = a `div` length xs
  where
    a = 10
    xs = [1,2,3,4,5]

mylast xs = head (reverse xs)
mylast2 xs = xs !! ((length xs)-1)
mylast3 xs = head (drop ((length xs) -1) xs)

myinit xs = reverse(drop 1 (reverse xs))
myinit2 xs = take ((length xs) - 1) xs
myinit3 xs = reverse (tail (reverse xs))

myeven n = n `mod` 2 == 0
myodd n = not (myeven n)

add :: (Int, Int) -> Int
add (x, y) = x + y

zeroto :: Int -> [Int]
zeroto n = [0..n]

add' :: Int -> (Int -> Int)
add' x y = x + y

mult :: Int -> (Int -> (Int -> Int))
mult x y z = x*y*z
