import           Lib                            ( part1
                                                , part2
                                                )
import           Test.Hspec
import           Test.QuickCheck

main = do
  hspec $ do
    describe "Best Score" $ do
      it "Test Part1" $ do
        part1 "1122" `shouldBe` 3
        part1 "1111" `shouldBe` 4
        part1 "1234" `shouldBe` 0
        part1 "91212129" `shouldBe` 9
      it "Test Part2" $ do
        part2 "1212" `shouldBe` 6
        part2 "1221" `shouldBe` 0
        part2 "123425" `shouldBe` 4
        part2 "123123" `shouldBe` 12
        part2 "12131415" `shouldBe` 4
