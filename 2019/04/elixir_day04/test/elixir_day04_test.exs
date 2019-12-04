defmodule ElixirDay04Test do
  use ExUnit.Case
  doctest ElixirDay04

  test "password?" do
    assert ElixirDay04.password?(1) == false
    assert ElixirDay04.password?(11_111_111) == false
    assert ElixirDay04.password?(111_111) == true
    assert ElixirDay04.password?(223_450) == false
    assert ElixirDay04.password?(123_789) == false
    assert ElixirDay04.password?(123_444) == true
  end

  test "password2?" do
    assert ElixirDay04.password2?(1) == false
    assert ElixirDay04.password2?(11_111_111) == false
    assert ElixirDay04.password2?(111_111) == false
    assert ElixirDay04.password2?(223_450) == false
    assert ElixirDay04.password2?(123_789) == false
    assert ElixirDay04.password2?(123_444) == false
    assert ElixirDay04.password2?(112_233) == true
    assert ElixirDay04.password2?(111_122) == true
    assert ElixirDay04.password2?(111_123) == false
  end

  test "solve" do
    want = 771
    got = ElixirDay04.solve(200_000, 300_000)
    assert want == got
  end

  test "solve2" do
    want = 546
    got = ElixirDay04.solve2(200_000, 300_000)
    assert want == got
  end
end
