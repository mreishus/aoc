import           Lib                            ( fuel
                                                , totalFuel
                                                )
import           Test.Hspec
import           Test.QuickCheck

main = do
  hspec $ do
    describe "Fuel" $ do
      it "works" $ do
        fuel 12 `shouldBe` 2
        fuel 14 `shouldBe` 2
        fuel 1969 `shouldBe` 654
        fuel 100756 `shouldBe` 33583
    describe "Total Fuel" $ do
      it "works" $ do
        totalFuel 12 `shouldBe` 2
        totalFuel 14 `shouldBe` 2
        totalFuel 1969 `shouldBe` 966
        totalFuel 100756 `shouldBe` 50346
