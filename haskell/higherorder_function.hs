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