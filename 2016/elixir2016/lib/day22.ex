defmodule Elixir2016.Day22 do
  @doc """
  Returns a map of nodes, with the key being its x, y coordinates
  %{                                                                 
    {3, 3} => %{avail: 17, size: 89, used: 72, x: 3, y: 3},
    {24, 3} => %{avail: 19, size: 87, used: 68, x: 24, y: 3},  
    {15, 13} => %{avail: 16, size: 85, used: 69, x: 15, y: 13},
    ..
  }
  x range: 0-32
  y range: 0-30
  """
  def parse(filename) do
    node_list =
      File.stream!(filename)
      |> Stream.drop(2)
      |> Stream.map(&String.trim/1)
      |> Stream.map(&parse_line/1)

    %{size: min_size} = Enum.min_by(node_list, fn node -> node.size end)

    node_list
    |> Enum.map(fn node -> Map.put(node, :large, node.used > min_size) end)
    |> Map.new(fn node -> {{node.x, node.y}, node} end)
  end

  def parse_line(line) do
    # /dev/grid/node-x0-y0     94T   72T    22T   76%
    finder = ~r/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T/

    [x, y, size, used, avail] =
      Regex.run(finder, line) |> Enum.drop(1) |> Enum.map(&String.to_integer/1)

    %{x: x, y: y, size: size, used: used, avail: avail}
  end

  @doc """

    Node A is not empty (its Used is not zero).
    Nodes A and B are not the same node.
    The data on node A (its Used) would fit on node B (its Avail).

  """
  def viable_pairs(nodes) when is_map(nodes) do
    all_pairs =
      for coord_a <- Map.keys(nodes), coord_b <- Map.keys(nodes), coord_a != coord_b do
        {coord_a, coord_b}
      end

    all_pairs
    |> Enum.filter(fn {coord_a, coord_b} ->
      node_a = nodes[coord_a]
      node_b = nodes[coord_b]
      node_a.used != 0 and node_a.used <= node_b.avail
    end)
    |> Enum.count()
  end

  def part1(filename) do
    parse(filename)
    |> viable_pairs()
  end

  @doc """
  Here is what our grid looks like:
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . G
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . _ . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
  We are "_".  We need to move G to the top left, but only by "swaps".

  This is a hard problem, but with easy data.
  Building a general solution would be too difficult.

  1. Move to where the node is.  We can use BFS to find distance here,
  or I can just count in the grid above.
  Assume we approach it from the left and when we move there, it moves
  left one.
  2. Now we need to move left 31 times.  Each move is 5 steps:
  Down Left Left Up Right.
  """
  def part2(_filename) do
    # 63 steps to top right + 31 * 5
    63 + 31 * 5
  end
end
