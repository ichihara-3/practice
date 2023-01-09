fac :: Integer -> Integer
fac 0 = 1
fac n = n * fac (n - 1)

(***) :: Int -> Int -> Int
m *** 0 = 0
m *** n = m + (m *** (n-1))

product2 :: Num a => [a] -> a
product2 []  = 1
product2 (n:ns) = n * product2 ns

length2 :: [a] -> Int
length2 [] = 0
length2 (_:xs) = 1 + length2 xs

reverse2 :: [a] -> [a]
reverse2 [] = []
reverse2 (x:xs) = reverse2 xs ++ [x]

(+++) :: [a] -> [a] -> [a]
[] +++ ys = ys
(x:xs) +++ ys = x : (xs +++ ys)


insert :: Ord a => a -> [a] -> [a]
insert x [] = [x]
insert x (y:ys) | x <= y    = x : y : ys
                | otherwise = y : insert x ys

isort :: Ord a => [a] -> [a]
isort [] = []
isort (x:xs) = insert x (isort xs)

myzip :: [a] -> [b] -> [(a, b)]
myzip a []          = []
myzip [] b          = []
myzip (x:xs) (y:ys) = (x, y) : myzip xs ys

mydrop :: Int -> [a] -> [a]
mydrop 0 xs = xs
mydrop _ [] = []
mydrop n (x:xs) = mydrop (n-1) xs

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

qsort :: Ord a => [a] -> [a]
qsort [] = []
qsort (x:xs) = qsort smaller ++ [x] ++ larger
               where
                 smaller = [a | a <-xs, a <= x]
                 larger  = [b | b<-xs, b > x]

myeven :: Int -> Bool
myeven 0 = True
myeven n = myodd (n-1)

myodd :: Int -> Bool
myodd 0 = False
myodd n = myeven (n-1)


evens :: [a] -> [a]
evens [] = []
evens (x:xs) = x : odds xs

odds :: [a] -> [a]
odds [] = []
odds (_:xs) = evens xs

-- section 6 practice
-- 1
fac2 :: Integer -> Integer
fac2 0 = 1
fac2 n | n > 0 = n * fac (n - 1)
-- 2
sumdown :: Int -> Int
sumdown 0 = 0
sumdown n | n > 0 = n + sumdown (n - 1)
-- 3
(^^^) :: Int -> Int -> Int
_ ^^^ 0 = 1
n ^^^ m = n * (n ^^^ (m-1))
-- 2 ^ 3
-- = 2 * (2 ^^^ 2)
-- = 2 * (2 * (2 ^^^ 1))
-- = 2 * (2 * (2 * ( 2 ^^^ 0)))
-- = 2 * (2 * (2 * 1))
-- = 2 * 2 * 2 = 8

-- 4
euclid :: Int -> Int -> Int
euclid n m | n < m     = euclid n (m - n)
           | n > m     = euclid (n - m) m
           | otherwise = n

-- 5
-- length [1, 2, 3]
-- = 1 + length [2, 3]
-- = 1 + 1 + length [3]
-- = 1 + 1 + 1 + length []
-- = 1 + 1 + 1 + 0 = 3

-- drop 3 [1,2,3,4,5]
-- = drop 2 [2, 3, 4, 5]
-- = drop 1 [3, 4, 5]
-- = drop 0 [4, 5]
-- = [4, 5]


-- init [1,2,3]
-- = 1 : init [2, 3]
-- = 1 : 2 : init [3]
-- = 1 : 2 : []
-- = [1, 2]

-- 6
and1 :: [Bool] -> Bool
and1 [] = True
and1 [x] = x
and1 (x:xs)| x == True = and1 xs
          | otherwise = False

concat1 :: [[a]] -> [a]
concat1 [] = []
concat1 (x:xs) = x ++ concat1 xs

replicate1 :: Int -> a -> [a]
replicate1 0 _ = []
replicate1 n x = x : replicate1 (n-1) x

(!!!!) :: [a] -> Int -> a
(x:xs) !!!! 0 = x
(_:xs) !!!! n = xs !!!! (n-1)

