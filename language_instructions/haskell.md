# Haskell

## Prereqs

```fish
stack install brittany
```

## Basic Setup

```fish
set PROJNAME haskell-day01
stack new $PROJNAME
cd $PROJNAME
nvim package.yaml app/Main.hs src/Lib.hs test/Spec.hs Makefile -p
```

## `package.yaml`

Add *hspec* and *QuickCheck* to the dependencies section.

```yaml
dependencies:
- base >= 4.7 && < 5
- hspec
- QuickCheck
```

## `app/Main.hs`

```haskell
module Main where

import Lib

main :: IO ()
main = do
  putStrLn "Hello from main"
  let xOne = addOne 10
  putStrLn "Expect to see 11"
  putStrLn $ show xOne
```

## `src/Lib.hs`

```haskell
module Lib
    ( addOne
    ) where

addOne :: Int -> Int
addOne x = x + 1
```

## `test/Spec.hs`

```haskell
import Lib (addOne)
import           Test.Hspec
import           Test.QuickCheck

main = do
  hspec $ do
    describe "Best Score" $ do
      it "Example Tests" $ do
        addOne 10 `shouldBe` 11
        addOne 12 `shouldBe` 13
```

## `./Makefile` (requires tabs!)

```make
run:
        stack run
.PHONY: test
test:
        stack test
repl:
        stack ghci
format:
        brittany --write-mode=inplace **/*.hs        
```
