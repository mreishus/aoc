defmodule ElixirDay13.Parse do
  @doc """
  In: filename
  Out: Layer Map
  %{
    0 => %{depth: 3, scanner: 0},
    1 => %{depth: 2, scanner: 0},
    4 => %{depth: 4, scanner: 0},
    6 => %{depth: 4, scanner: 0}
  }
  """
  def parse_file(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse_element/1)
    |> create_layer_map()
  end

  @doc """
  parse_element("4: 6") = %{index: 4, depth: 6}
  """
  def parse_element(string) do
    [left, right] =
      String.split(string, ": ")
      |> Enum.map(&String.to_integer/1)

    %{index: left, depth: right}
  end

  @doc """
  In: List of elements created by parse_element
  Out: Layer map
  %{
    0 => %{depth: 3, scanner: 0},
    1 => %{depth: 2, scanner: 0},
    4 => %{depth: 4, scanner: 0},
    6 => %{depth: 4, scanner: 0}
  }
  """
  def create_layer_map(layers) do
    layers
    |> Enum.reduce(%{}, fn x, acc ->
      layer = %{depth: x.depth, scanner: 0, delta: 1}
      Map.put(acc, x.index, layer)
    end)
  end
end
