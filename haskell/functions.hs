myeven :: Integral a => a -> Bool
myeven n = n `mod` 2 == 0

mysplitAt :: Int -> [a] -> ([a], [a])
mysplitAt n xs = (take n xs, drop n xs)

myrecip :: Fractional a => a -> a
myrecip n = 1/n

myabs :: Int -> Int
myabs n = if n >= 0 then n else -n

mysignum :: Int -> Int
mysignum n = if n < 0 then -1 else
                if n == 0 then 0 else 1

myabs2 n | n >= 0    = n
         | otherwise = -n

mysignum2 n | n < 0  = -1
            | n == 0 = 0
            | n > 0  = 1

mynot :: Bool -> Bool
mynot False = True
mynot True = False

(&&&) :: Bool -> Bool -> Bool
True &&& True = True
_ &&& _ = False

(+++) :: Integral a => a -> a
(+++) n = n + 2


myfst :: (a, b) -> a
myfst (x, _) = x

mysnd :: (a, b) -> b
mysnd (_, y) = y

test :: [Char] -> Bool
test ['a', _, _] = True
test _           = False

test2 :: [Char] -> Bool
test2 ('a':_) = True
test2 _       = False

myhead :: [a] -> a
myhead (x:_) = x

mytail :: [a] -> [a]
mytail (_:xs) = xs

myconst :: a-> (b -> a)
myconst x = \_ -> x

odds :: Int -> [Int]
odds n = map f [0..n-1]
         where f x = x * 2 + 1

odds2 :: Int -> [Int]
odds2 n = map (\x -> x*2 + 1) [0..n-1]

halve :: [a] -> ([a], [a])
halve xs = (take (length xs `div` 2) xs, drop (length xs `div` 2) xs)

halve2 :: [a] -> ([a], [a])
halve2 xs = (take x xs, drop x xs)
            where x = length xs `div` 2


third1 :: [a] -> a
third1 xs = head (tail (tail xs))

third2 :: [a] -> a
third2 xs = xs!!2

third3 :: [a] -> a
third3 (_:_:a:_) = a

