import Data.Char

crack :: String -> String
crack xs = xs


frequency :: [Float]
frequency = [8.1, 1.5, 2.8, 4.2, 12.7, 2.2, 2.0, 6.1, 7.0,
         0.2, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0,
         6.3, 9.0, 2.8, 1.9, 2.4, 0.2, 2.0, 0.1]


caesar_encode :: Int -> String -> String
caesar_encode n xs = [shift n c | c <- xs]
  where
    shift n c | isLower c = chr ((ord c + n - ord 'a') `mod` 26 + ord 'a')
              | isUpper c   = chr ((ord c + n - ord 'A') `mod` 26 + ord 'A')
              | otherwise = c

caesar_decode :: Int -> String -> String
caesar_decode n xs = caesar_encode (-n) xs
