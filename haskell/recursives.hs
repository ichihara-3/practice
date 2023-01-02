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
