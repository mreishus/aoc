defmodule Elixir2016.Day02 do
  def part1(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.reduce(%{position: {1, 1}, digits: []}, fn steps_str, acc ->
      # Apply all of the steps in "steps_str" to our current position
      new_pos =
        String.graphemes(steps_str)
        |> Enum.reduce(acc.position, fn step, new_pos ->
          move(new_pos, step)
        end)

      new_digit = keypad() |> Map.get(new_pos)
      %{position: new_pos, digits: acc.digits ++ [new_digit]}
    end)
    |> Map.get(:digits)
    |> Enum.join("")
  end

  def part2(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.reduce(%{position: {0, 2}, digits: []}, fn steps_str, acc ->
      # Apply all of the steps in "steps_str" to our current position
      new_pos =
        String.graphemes(steps_str)
        |> Enum.reduce(acc.position, fn step, new_pos ->
          move2(new_pos, step)
        end)

      new_digit = keypad2() |> Map.get(new_pos)
      %{position: new_pos, digits: acc.digits ++ [new_digit]}
    end)
    |> Map.get(:digits)
    |> Enum.join("")
  end

  ## Part 1 Keypad / Move Logic

  def keypad() do
    %{
      {0, 0} => 1,
      {1, 0} => 2,
      {2, 0} => 3,
      {0, 1} => 4,
      {1, 1} => 5,
      {2, 1} => 6,
      {0, 2} => 7,
      {1, 2} => 8,
      {2, 2} => 9
    }
  end

  # Edge Cases
  def move({0, y}, "L"), do: {0, y}
  def move({2, y}, "R"), do: {2, y}
  def move({x, 0}, "U"), do: {x, 0}
  def move({x, 2}, "D"), do: {x, 2}

  # Normal movement
  def move({x, y}, "L"), do: {x - 1, y}
  def move({x, y}, "R"), do: {x + 1, y}
  def move({x, y}, "U"), do: {x, y - 1}
  def move({x, y}, "D"), do: {x, y + 1}

  ## Part 2 Keypad / Move Logic
  @doc """
        1
      2 3 4
    5 6 7 8 9
      A B C
        D
  """
  def keypad2() do
    %{
      {2, 0} => 1,
      {1, 1} => 2,
      {2, 1} => 3,
      {3, 1} => 4,
      {0, 2} => 5,
      {1, 2} => 6,
      {2, 2} => 7,
      {3, 2} => 8,
      {4, 2} => 9,
      {1, 3} => "A",
      {2, 3} => "B",
      {3, 3} => "C",
      {2, 4} => "D"
    }
  end

  # Edge Cases - Left
  def move2({2, 0} = orig, "L"), do: orig
  def move2({1, 1} = orig, "L"), do: orig
  def move2({0, 2} = orig, "L"), do: orig
  def move2({1, 3} = orig, "L"), do: orig
  def move2({2, 4} = orig, "L"), do: orig

  # Edge Cases - Right
  def move2({2, 0} = orig, "R"), do: orig
  def move2({3, 1} = orig, "R"), do: orig
  def move2({4, 2} = orig, "R"), do: orig
  def move2({3, 3} = orig, "R"), do: orig
  def move2({2, 4} = orig, "R"), do: orig

  @doc """
        1
      2 3 4
    5 6 7 8 9
      A B C
        D
  """
  # Edge Cases - Up
  def move2({_x, 0} = orig, "U"), do: orig
  def move2({1, 1} = orig, "U"), do: orig
  def move2({3, 1} = orig, "U"), do: orig
  def move2({0, 2} = orig, "U"), do: orig
  def move2({4, 2} = orig, "U"), do: orig

  # Edge Cases - Down
  def move2({_x, 4} = orig, "D"), do: orig
  def move2({1, 3} = orig, "D"), do: orig
  def move2({3, 3} = orig, "D"), do: orig
  def move2({0, 2} = orig, "D"), do: orig
  def move2({4, 2} = orig, "D"), do: orig

  # Normal movement
  def move2({x, y}, "L"), do: {x - 1, y}
  def move2({x, y}, "R"), do: {x + 1, y}
  def move2({x, y}, "U"), do: {x, y - 1}
  def move2({x, y}, "D"), do: {x, y + 1}
end
