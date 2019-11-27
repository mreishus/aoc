defmodule ElixirDay04Test do
  use ExUnit.Case
  doctest ElixirDay04

  test "greets the world" do
    assert ElixirDay04.hello() == :world
  end

  test "valid_passphrase?" do
    assert ElixirDay04.valid_passphrase?("aa bb cc dd ee")
    assert ElixirDay04.valid_passphrase?("aa bb cc dd aaa")
    refute ElixirDay04.valid_passphrase?("aa bb cc dd aa")
  end

  test "valid_passphrase_p2?" do
    # Valie
    assert ElixirDay04.valid_passphrase_p2?("abcde fghij")
    assert ElixirDay04.valid_passphrase_p2?("a ab abc abd abf abj")
    assert ElixirDay04.valid_passphrase_p2?("iiii oiii ooii oooi oooo")

    # Not
    refute ElixirDay04.valid_passphrase_p2?("abcde xyz ecdab")
    refute ElixirDay04.valid_passphrase_p2?("oiii ioii iioi iiio")
  end
end
