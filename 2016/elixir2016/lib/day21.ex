defmodule Elixir2016.Day21 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_line/1)
    |> Enum.to_list()
  end

  def parse_line(line) do
    move = ~r/move position (\d+) to position (\d+)/
    reverse = ~r/reverse positions (\d+) through (\d+)/
    swap_letter = ~r/swap letter (\w+) with letter (\w+)/
    swap_pos = ~r/swap position (\d+) with position (\d+)/
    rotate = ~r/rotate (left|right) (\d+) step/
    rotate_pos = ~r/rotate based on position of letter (\w+)/

    cond do
      Regex.match?(move, line) ->
        [arg1, arg2] = Regex.run(move, line) |> Enum.drop(1) |> Enum.map(&String.to_integer/1)
        {:move, arg1, arg2}

      Regex.match?(reverse, line) ->
        [arg1, arg2] = Regex.run(reverse, line) |> Enum.drop(1) |> Enum.map(&String.to_integer/1)
        {:reverse, arg1, arg2}

      Regex.match?(rotate_pos, line) ->
        [_, arg1] = Regex.run(rotate_pos, line)
        {:rotate_pos, arg1}

      Regex.match?(rotate, line) ->
        [_, arg1, arg2] = Regex.run(rotate, line)
        {:rotate, arg1, String.to_integer(arg2)}

      Regex.match?(swap_letter, line) ->
        [_, arg1, arg2] = Regex.run(swap_letter, line)
        {:swap_letter, arg1, arg2}

      Regex.match?(swap_pos, line) ->
        [arg1, arg2] = Regex.run(swap_pos, line) |> Enum.drop(1) |> Enum.map(&String.to_integer/1)
        {:swap_pos, arg1, arg2}

      true ->
        line
    end
  end

  def part1(filename) do
    parse(filename)
    |> run_commands("abcdefgh")
  end

  def part2(filename) do
    commands = parse(filename)

    "abcdefgh"
    |> String.graphemes()
    |> permutations()
    |> Enum.map(&Enum.join/1)
    |> Stream.filter(fn passwd ->
      run_commands(commands, passwd) == "fbgdceah"
    end)
    |> Enum.take(1)
  end

  def run_commands(commands, initial_string) do
    commands
    |> Enum.reduce(initial_string, fn command, acc ->
      run_command(command, acc)
    end)
  end

  def run_command({:swap_pos, pos1, pos2}, string) do
    char1 = String.at(string, pos1)
    char2 = String.at(string, pos2)

    string
    |> string_update(pos1, char2)
    |> string_update(pos2, char1)
  end

  def run_command({:swap_letter, let1, let2}, string) do
    string
    |> String.graphemes()
    |> Enum.map(fn this_letter ->
      case this_letter do
        ^let1 -> let2
        ^let2 -> let1
        _ -> this_letter
      end
    end)
    |> Enum.join()
  end

  def run_command({:reverse, pos1, pos2}, string) when pos2 > pos1 do
    # "abcdef": Reverse {2, 4}
    # 0-1  "ab"   left
    # 2-4  "cde"  mid
    # 5    "f"    right
    {left_mid, right} = String.split_at(string, pos2 + 1)
    {left, mid} = String.split_at(left_mid, pos1)
    left <> String.reverse(mid) <> right
  end

  def run_command({:rotate, "left", n}, string) do
    string
    |> String.graphemes()
    |> rotate_left(n)
    |> Enum.join()
  end

  def run_command({:rotate, "right", n}, string) do
    string
    |> String.graphemes()
    |> rotate_right(n)
    |> Enum.join()
  end

  def run_command({:move, pos1, pos2}, string) do
    list = string |> String.graphemes()
    char1 = list |> Enum.at(pos1)

    list
    |> List.delete_at(pos1)
    |> List.insert_at(pos2, char1)
    |> Enum.join()
  end

  # "rotate based on position of letter b" finds the index of letter b (1), then
  # rotates the string right once plus a number of times equal to that index (2):
  # ecabd.
  # Once the index is determined, rotate the string to the right one time, plus a
  # number of times equal to that index, plus one additional time if the index was
  # at least 4.
  def run_command({:rotate_pos, char1}, string) do
    [left, _] = String.split(string, char1, parts: 2)
    pos1 = String.length(left)

    rotate_amount =
      cond do
        pos1 >= 4 -> pos1 + 2
        true -> pos1 + 1
      end

    run_command({:rotate, "right", rotate_amount}, string)
  end

  def run_command(_command, string), do: string

  ### Helpers ###

  @doc """
  iex(3)> Day21.string_update("abcdef", 3, "Z")
  "abcZef"
  """
  def string_update(string, position, char) do
    # iex(4)> "abcdef" |> String.at(3)
    # "d"
    {left, right} = String.split_at(string, position)

    if String.length(right) == 1 do
      left <> char
    else
      {_replaced, trunc_right} = String.split_at(right, 1)
      left <> char <> trunc_right
    end
  end

  @doc """
  iex(2)> Day21.rotate_left([5, 6, 7, 8, 9], 2)
  [7, 8, 9, 5, 6]
  """
  def rotate_left(list, 0), do: list

  def rotate_left([h | t], n) when n > 0 do
    (t ++ [h])
    |> rotate_left(n - 1)
  end

  @doc """
  iex(8)> Day21.rotate_right([5, 6, 7, 8, 9], 2)
  [8, 9, 5, 6, 7]
  """
  def rotate_right(list, 0), do: list

  def rotate_right(list, n) when n > 0 do
    list
    |> Enum.reverse()
    |> rotate_left(n)
    |> Enum.reverse()
  end

  def permutations([]), do: [[]]

  def permutations(list),
    do: for(elem <- list, rest <- permutations(list -- [elem]), do: [elem | rest])
end
