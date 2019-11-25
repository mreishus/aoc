module Main where

import           Lib

import           Data.Char                      ( isSpace )
rstrip = reverse . dropWhile isSpace . reverse


main :: IO ()
main = do
  s_raw <- readFile "../input.txt"
  let s = rstrip s_raw
  putStrLn "Part1"
  putStrLn $ show $ part1 s
  putStrLn "Part2"
  putStrLn $ show $ part2 s
