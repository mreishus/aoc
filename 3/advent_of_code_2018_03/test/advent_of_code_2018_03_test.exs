defmodule AdventOfCode201803Test do
  use ExUnit.Case
  doctest AdventOfCode201803

  test "End To End Part 1" do
    filename = "input.txt"
    grid_size = 1000
    {overlap, _} = AdventOfCode201803.solve(filename, grid_size)
    assert overlap == 121163
  end

  test "End To End Part 2" do
    filename = "input.txt"
    grid_size = 1000
    {_, uncontested} = AdventOfCode201803.solve(filename, grid_size)
    assert uncontested == [%Claim{height: 11, id: 943, width: 16, x: 235, y: 134}]
  end
  #test "greets the world" do
  #  assert AdventOfCode201803.hello() == :world
  #end
end
