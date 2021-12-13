defmodule Elixir2021.Day12 do
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(fn x -> String.split(x, "-") end)
    |> Enum.reduce(%{}, fn [a, b], acc ->
      acc
      |> Map.update(a, [b], fn list -> [b | list] end)
      |> Map.update(b, [a], fn list -> [a | list] end)
    end)
  end

  def big?(input), do: input == String.upcase(input)

  def search([], count, _config), do: count

  def search(open_set, count, %{routes: routes, get_next: get_next} = config) do
    complete_count =
      Enum.count(open_set, fn path ->
        List.last(path) == "end"
      end)

    Enum.flat_map(open_set, fn state -> get_next.(state, routes) end)
    |> search(count + complete_count, config)
  end

  def next_states1(state, routes) do
    here = List.last(state)

    if here == "end" do
      []
    else
      Map.get(routes, here)
      |> Enum.filter(fn room -> room != "start" end)
      |> Enum.filter(fn room -> big?(room) || !Enum.member?(state, room) end)
      |> Enum.map(fn room -> state ++ [room] end)
    end
  end

  def next_states2(state, routes) do
    here = List.last(state)

    has_double =
      state
      |> Enum.filter(fn r -> !big?(r) end)
      |> Enum.frequencies()
      |> Map.values()
      |> Enum.any?(fn x -> x > 1 end)

    if here == "end" do
      []
    else
      Map.get(routes, here)
      |> Enum.filter(fn room -> room != "start" end)
      |> Enum.filter(fn room -> big?(room) || small_room_allowed(state, room, has_double) end)
      |> Enum.map(fn room -> state ++ [room] end)
    end
  end

  def small_room_allowed(state, room, true) do
    !Enum.member?(state, room)
  end

  def small_room_allowed(state, room, false) do
    Enum.count(state, fn x -> x == room end) < 2
  end

  def part1(filename) do
    routes = parse(filename)
    search([["start"]], 0, %{routes: routes, get_next: &next_states1/2})
  end

  def part2(filename) do
    routes = parse(filename)
    search([["start"]], 0, %{routes: routes, get_next: &next_states2/2})
  end
end
