defmodule Elixir2016.Day13 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
    |> List.first()
    |> String.to_integer()
  end

  def part1(filename) do
    fav_num = parse(filename)
    config = %{fav_num: fav_num, final: {31, 39}}
    {answer, _} = bfs([{1, 1}], 0, MapSet.new(), config)
    answer
  end

  def part2(filename) do
    fav_num = parse(filename)
    config = %{fav_num: fav_num, final: {31, 39}}
    {_, config} = bfs([{1, 1}], 0, MapSet.new(), config)

    config.seen_steps
    |> Enum.filter(fn {{_x, _y}, steps} -> steps <= 50 end)
    |> Enum.count()
  end

  def bfs(open_set, num, seen, config) do
    config = update_seen_steps(config, open_set, num)

    if open_set |> Enum.any?(fn coords -> final_state?(coords, config) end) do
      {num, config}
    else
      next_open_set =
        open_set
        |> Parallel.pmap2(&next_states/2, config)
        |> Enum.concat()
        |> Enum.uniq()
        |> Enum.reject(fn state -> MapSet.member?(seen, state) end)

      if length(next_open_set) == 0 do
        nil
      else
        bfs(next_open_set, num + 1, MapSet.union(seen, MapSet.new(next_open_set)), config)
      end
    end
  end

  def update_seen_steps(%{seen_steps: orig_seen_steps} = config, open_set, steps) do
    seen_steps =
      for(thing <- open_set, into: %{}, do: {thing, steps})
      |> Map.merge(orig_seen_steps)

    config
    |> Map.put(:seen_steps, seen_steps)
  end

  def update_seen_steps(%{} = config, open_set, steps) do
    seen_steps = for thing <- open_set, into: %{}, do: {thing, steps}

    config
    |> Map.put(:seen_steps, seen_steps)
  end

  def next_states({x, y}, config) do
    [{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}]
    |> Enum.filter(fn {x, y} -> not wall?(x, y, config.fav_num) end)
  end

  def final_state?(coords, config), do: coords == config.final

  def wall?(x, y, _fav_num) when x < 0 or y < 0, do: true

  def wall?(x, y, fav_num) do
    (x * x + 3 * x + 2 * x * y + y + y * y + fav_num)
    |> bit_count()
    |> rem(2) == 1
  end

  def bit_count(n) do
    for(<<bit::1 <- :binary.encode_unsigned(n)>>, do: bit) |> Enum.sum()
  end
end
