import Data.Char
import Data.List

twice :: (a -> a) -> a -> a
twice f x = f (f x)

quadruple = twice (*2)

mymap :: (a -> b) -> [a] -> [b]
mymap f xs = [f x | x <- xs]

add1Inner = map (map (+1))

mymap2 :: (a -> b) -> [a] -> [b]
mymap2 _ [] = []
mymap2 f (x:xs) = f x : mymap2 f xs

myfilter :: (a -> Bool) -> [a] -> [a]
myfilter p xs = [x | x <- xs, p x]

sumsqreven :: [Int] -> Int
sumsqreven xs = sum (map (^2) (filter even xs))


-- f [] = v
-- f (x:xs) = x # f xs
-- sum [] = 0
-- sum (x:xs) = x + sum xs
-- -> sum = foldr (+) 0

-- product [] = 1
-- product (x:xs) = x * product xs
-- -> product = foldr (*) 1

-- or [] = False
-- or (x:xs) = x || or xs
-- -> or = foldr (||) False

-- and [] = True
-- and (x:xs) = x && and xs
-- -> and = foldr (&&) True

mylength :: [a] -> Int
mylength = foldr (\_ n -> 1+n) 0

myreverse :: [a] -> [a]
myreverse = foldr (\x ys -> ys ++ [x]) []

mysum :: Num a => [a] -> a
mysum = sum' 0
  where
    sum' v [] = v
    sum' v (x:xs) = sum' (v+x) xs

mysum2 :: Integral a => [a] -> a
mysum2 = foldl (+) 0

myproduct :: Integral a => [a] -> a
myproduct = foldl (*) 1

myor :: [Bool] -> Bool
myor = foldl (||) False

myand :: [Bool] -> Bool
myand = foldl (&&) True

mylength2 :: [a] -> Int
mylength2 = foldl (\n _ -> n + 1) 0

myreverse2 :: [a] -> [a]
myreverse2 = foldl (\xs y -> y : xs) []

--------
myodd = not . even
twice2 f = f . f

compose :: [a -> a] -> (a -> a)
compose = foldr (.) id

---------
-- binary converter


type Bit = Int

bin2int :: [Bit] -> Int
bin2int bits = sum [w * b | (w, b) <- zip weights bits]
               where weights = iterate (*2) 1

int2bin :: Int -> [Bit]
int2bin 0 = []
int2bin n = n `mod` 2 : int2bin (n `div` 2)

make8 :: [Bit] -> [Bit]
make8 bits = take 8 (bits ++ repeat 0)

encode :: String -> [Bit]
encode = concat . map (make8 . int2bin . ord)

chop8 :: [Bit] -> [[Bit]]
chop8 [] = []
chop8 bits = take 8 bits : chop8 (drop 8 bits)

decode :: [Bit] -> String
decode = map (chr . bin2int) . chop8

transmit :: String -> String
transmit = decode . channel . encode

channel = id

--------
-- vote algorithms

votes :: [String]
votes = ["Red", "Blue", "Green", "Blue", "Blue", "Red"]

count :: Eq a => a -> [a] -> Int
count x = length . filter (== x)


rmdups :: Eq a => [a] -> [a]
rmdups [] = []
rmdups (x:xs) = x: rmdups (filter (/= x) xs)

result :: Ord a => [a] -> [(Int, a)]
result xs = sort [(count v xs, v) | v <- rmdups xs]

winner :: Ord a => [a] -> a
winner = snd . last . result


--
ballots :: [[String]]
ballots = [["Red", "Green"],
           ["Blue"],
           ["Green", "Red", "Blue"],
           ["Blue", "Green", "Red"],
           ["Green"]]

rmempty :: Eq a => [[a]] -> [[a]]
rmempty = filter (/= [])

elim :: Eq a => a -> [[a]] -> [[a]]
elim x = map (filter (/= x))


rank :: Ord a => [[a]] -> [a]
rank = map snd . result . map head


winner' :: Ord a => [[a]] -> a
winner' bs = case rank (rmempty bs) of
             [c]    -> c
             (c:cs) -> winner' (elim c bs)
