import Data.Char

caesar_encode :: Int -> String -> String
caesar_encode n xs = [shift n c | c <- xs]
  where
    shift n c | isLower c = chr ((ord c + n - ord 'a') `mod` 26 + ord 'a')
              | isUpper c = chr ((ord c + n - ord 'A') `mod` 26 + ord 'A')
              | otherwise = c

caesar_decode :: Int -> String -> String
caesar_decode n xs = caesar_encode (-n) xs

chisqr :: [Float] -> [Float] -> Float
chisqr os es = sum [(o-e)^2 / e | (o, e) <- zip os es]

rotate :: Int -> [a] -> [a]
rotate n xs = drop n xs ++ take n xs

count :: Eq a => a -> [a] -> Int
count x xs = length [x | x' <- xs, x == x']

freq :: String -> [Float]
freq xs = [fromIntegral (count c xs') | c <- ['a'..'z']]
  where
    xs' = [toLower x | x <- xs]

indexOf :: Eq a => a -> [a] -> Int
indexOf x xs = [i | (x', i) <- zip xs [0..], x == x'] !! 0

crack :: String -> String
crack xs = caesar_decode factor xs
  where
    factor = indexOf (minimum chitab) chitab
    freqs = freq xs
    chitab = [chisqr (rotate n freqs) frequency | n <- [0..25]]

frequency :: [Float]
frequency = [8.1, 1.5, 2.8, 4.2, 12.7, 2.2, 2.0, 6.1, 7.0,
         0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0,
         6.3, 9.0, 2.8, 1.9, 2.4, 0.2, 2.0, 0.1]
