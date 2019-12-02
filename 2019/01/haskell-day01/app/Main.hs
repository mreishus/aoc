module Main where

import           Lib

main :: IO ()
main = do
  input <- readFile "../input.txt"
  let fileLines = (map read) $ lines input
  putStrLn "AOC 2019 Day 1"
  -- mapM_ putStrLn fileLines
  putStrLn "Part 1"
  putStrLn $ show $ part1 fileLines
  putStrLn "Part 2"
  putStrLn $ show $ part2 fileLines
