module Lib
  ( rotate
  , part1
  , part2
  , captcha
  )
where

rotate :: [a] -> Int -> [a]
rotate xs n = take (length xs) $ drop n $ cycle xs

part1 :: [Char] -> Int
part1 xs = captcha xs 1

part2 :: [Char] -> Int
part2 xs = captcha xs n where n = length xs `div` 2

captcha xs n = sum $ map (read . pure :: Char -> Int) $ map fst $ filter
  (\(x, y) -> x == y)
  zipped
 where
  xs'    = rotate xs n
  zipped = zip xs xs'

