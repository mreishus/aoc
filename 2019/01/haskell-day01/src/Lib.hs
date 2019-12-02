module Lib
  ( fuel
  , totalFuel
  , part1
  , part2
  )
where

addOne :: Int -> Int
addOne x = x + 1

fuel :: Int -> Int
fuel x = (x `div` 3) - 2

totalFuel :: Int -> Int
totalFuel x | y > 0     = y + totalFuel y
            | otherwise = 0
  where y = fuel x

part1 :: [Int] -> Int
part1 xs = sum $ map fuel xs

part2 :: [Int] -> Int
part2 xs = sum $ map totalFuel xs
