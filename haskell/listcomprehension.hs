import Data.Char

myconcat :: [[a]] -> [a]
myconcat xss = [x | xs <- xss, x <- xs]

firsts :: [(a, b)] -> [a]
firsts ps = [x | (x, _) <- ps]

mylength :: [a] -> Int
mylength xs = sum [1 | _ <- xs]

evens :: Integral a => [a] -> [a]
evens xs = [x | x <- xs, even x]

factors :: Int -> [Int]
factors n = [x | x <- [1..n], n `mod` x == 0]

prime :: Int -> Bool
prime n = factors n == [1, n]

primes :: Int -> [Int]
primes n = [x | x <- [2..n], prime x]

find :: Eq a => a -> [(a, b)] -> [b]
find k t = [v | (k', v)  <- t , k == k']

pairs :: [a] -> [(a, a)]
pairs xs = zip xs (tail xs)

sorted :: Ord a => [a] -> Bool
sorted xs = and [x <= y |(x, y) <- pairs xs]

positions :: Eq a => a -> [a] -> [Int]
positions x xs = [i| (x', i) <- zip xs [0..], x == x']

lowers :: String -> Int
lowers xs = length [x | x <- xs,  x >= 'a' && x <= 'z']

count :: Char -> String -> Int
count x xs = length [x' | x' <- xs, x == x']

let2int :: Char -> Int
let2int c = ord c - ord 'a'

int2let :: Int -> Char
int2let n = chr (ord 'a' + n)

shift :: Int -> Char -> Char
shift n c | isLower c = int2let ((let2int c + n) `mod` 26)
          | otherwise = c


encode :: Int -> String -> String
encode n xs = [shift n x | x <- xs]

decode :: Int -> String -> String
decode n xs = encode (-n) xs

table :: [Float]
table = [8.1, 1.5, 2.8, 4.2, 12.7, 2.2, 2.0, 6.1, 7.0,
         0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0,
         6.3, 9.0, 2.8, 1.9, 2.4, 0.2, 2.0, 0.1]

percent :: Int -> Int -> Float
percent n m =  (fromIntegral n / fromIntegral m) * 100

freqs :: String -> [Float]
freqs xs = [percent (count x xs) n | x <- ['a'..'z']]
           where n = lowers xs

chisqr :: [Float] -> [Float] -> Float
chisqr os es = sum [((o-e)^2)/e | (o, e) <- zip os es]

rotate :: Int -> [a] -> [a]
rotate n xs = drop n xs ++ take n xs


crack :: String -> String
crack xs = decode factor xs
  where
    factor = head (positions (minimum chitab) chitab)
    chitab = [chisqr (rotate n table') table | n <- [0..25]]
    table' = freqs xs


sqrTo100 = sum [x * x | x <- [1..100]]

grid :: Int -> Int -> [(Int, Int)]
grid m n = [(x, y)| x <- [0..m], y <- [0..n]]

square :: Int -> [(Int, Int)]
square n = [(x, y) | (x, y) <- grid n n, x /= y]

replicate2 :: Int -> a -> [a]
replicate2 n x = [x | _ <- [1..n]]

pyths :: Int -> [(Int, Int, Int)]
pyths n = [(x, y, z)| x <- [1..n], y <- [1..n], z <- [1..n], x^2+y^2==z^2]

perfects :: Int -> [Int]
perfects n = [x | x <- [1..n], perfect x]
  where
    perfect n = n == sum [x | x <- factors n, x /= n]

-- [(x, y)| x <- [1, 2, 3], y<-[4, 5, 6]]

result = concat [[(x, y)| y <- [4, 5, 6]] | x <- [1, 2, 3]]

positions2 :: Eq a => a -> [a] -> [Int]
positions2 x xs = find x [(x', y)| (x', y) <- zip xs [0..]]

scalarproduct :: [Int] -> [Int] -> Int
scalarproduct xs ys = sum [x*y| (x, y) <- zip xs ys]


lowLet2int :: Char -> Int
lowLet2int c = ord c - ord 'a'

lowInt2let :: Int -> Char
lowInt2let n = chr (ord 'a' + n)

upLet2int :: Char -> Int
upLet2int c = ord c - ord 'A'

upInt2let :: Int -> Char
upInt2let n = chr (ord 'A' + n)

shift2 :: Int -> Char -> Char
shift2 n c | isLower c = lowInt2let ((lowLet2int c + n) `mod` 26)
          | isUpper c = upInt2let ((upLet2int c + n) `mod` 26)
          | otherwise = c


encode2 :: Int -> String -> String
encode2 n xs = [shift2 n x | x <- xs]

decode2 :: Int -> String -> String
decode2 n xs = encode2 (-n) xs
