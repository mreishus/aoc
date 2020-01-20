# 4x4 Grid
# Start: Top left: 0, 0
# Vault: Bottom right: 3, 3
#########
# S| | | #
# -#-#-#-#
# | | | #
# -#-#-#-#
# | | | #
# -#-#-#-#
# | | |
####### V

defmodule Elixir2016.Day17 do
  def parse(filename) do
    File.read!(filename)
    |> String.trim()
  end

  def part1(filename) do
    parse(filename)
    |> bfs_part1()
  end

  def part2(filename) do
    parse(filename)
    |> bfs_part2()
  end

  def bfs_part1(passcode) when is_binary(passcode) do
    bfs([{0, 0, ""}], 0, MapSet.new(), %{passcode: passcode})
  end

  # open_set: List of {x, y, path}.  Search Frontier.  x = int, y = int, path = string like "UDDDLR" current path.
  # num: Number of steps taken, int.
  # seen: MapSet: Search states seen before. {x, y, path}.
  # config: map with %{passcode: passcode} (passcode is a string)
  def bfs(open_set, num, seen, config) do
    if contains_dest?(open_set) do
      answer(open_set)
    else
      next_open_set = Enum.flat_map(open_set, fn state -> next_states(state, config) end)
      bfs(next_open_set, num + 1, seen, config)
    end
  end

  def bfs_part2(passcode) when is_binary(passcode) do
    bfs_longest([{0, 0, ""}], 0, MapSet.new(), %{passcode: passcode})
    |> String.length()
  end

  def bfs_longest([], _, _, _), do: nil

  def bfs_longest(open_set, num, seen, config) do
    if contains_dest?(open_set) do
      this_answer = answer(open_set)

      next_open_set = Enum.flat_map(open_set, fn state -> next_states(state, config) end)
      bfs_answer = bfs_longest(next_open_set, num + 1, seen, config)

      if bfs_answer == nil do
        this_answer
      else
        bfs_answer
      end
    else
      next_open_set = Enum.flat_map(open_set, fn state -> next_states(state, config) end)
      bfs_longest(next_open_set, num + 1, seen, config)
    end
  end

  def contains_dest?(open_set) do
    open_set
    |> Enum.any?(fn {x, y, _path} -> x == 3 and y == 3 end)
  end

  def answer(open_set) do
    {_x, _y, path} =
      open_set
      |> Enum.filter(fn {x, y, _path} -> x == 3 and y == 3 end)
      |> List.first()

    path
  end

  # Any state at the destination has no more steps
  def next_states({3, 3, _path}, _config), do: []

  def next_states({_x, _y, path} = state, config) do
    # (example) next_dirs = [:r, :d]
    next_dirs =
      room_dirs(config.passcode, path)
      |> Enum.filter(fn {_dir, possible} -> possible end)
      |> Enum.map(fn {dir, _possible} -> dir end)

    next_dirs
    |> Enum.map(fn dir -> walk(state, dir) end)
    |> Enum.filter(&valid_state?/1)
  end

  def walk({x, y, path}, :r), do: {x + 1, y, path <> "R"}
  def walk({x, y, path}, :l), do: {x - 1, y, path <> "L"}
  def walk({x, y, path}, :u), do: {x, y - 1, path <> "U"}
  def walk({x, y, path}, :d), do: {x, y + 1, path <> "D"}

  def valid_state?({x, y, path}) when is_integer(x) and is_integer(y) and is_binary(path) do
    x >= 0 and x <= 3 and y >= 0 and y <= 3
  end

  def valid_state?(_), do: false

  @doc """
  iex(2)> Day17.room_dirs("hijkl", "")
  %{d: true, l: true, r: false, u: true}

  iex(3)> Day17.room_dirs("hijkl", "DR")
  %{d: false, l: false, r: false, u: false}

  iex(4)> Day17.room_dirs("hijkl", "DU")
  %{d: false, l: false, r: true, u: false}
  """
  def room_dirs(passcode, path_string) do
    open_letters = ["b", "c", "d", "e", "f"]

    [u, d, l, r] =
      room_hash(passcode, path_string)
      |> String.graphemes()
      |> Enum.map(fn letter ->
        Enum.member?(open_letters, letter)
      end)

    %{u: u, d: d, l: l, r: r}
  end

  # passcode: "hijkl" or whatever is in input file
  # path_string: "UDLLL" (path taken so far)
  def room_hash(passcode, path_string) do
    (passcode <> path_string)
    |> md5
    |> String.slice(0, 4)
  end

  ## MD5 Helper (String -> String)
  def md5(input) do
    :crypto.hash(:md5, input) |> Base.encode16(case: :lower)
  end
end
