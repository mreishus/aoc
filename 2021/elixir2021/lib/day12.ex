defmodule Elixir2021.Day12.State do
  alias Elixir2021.Day12
  alias Elixir2021.Day12.State

  defstruct path: [],
            doubled_small?: false

  def new(path, doubled_small?) do
    %State{path: path, doubled_small?: doubled_small?}
  end

  def add_room(state = %State{}, room) do
    if state.doubled_small? do
      %State{path: [room | state.path], doubled_small?: true}
    else
      has_double = not Day12.big?(room) and Enum.member?(state.path, room)
      %State{path: [room | state.path], doubled_small?: has_double}
    end
  end
end

defmodule Elixir2021.Day12 do
  alias Elixir2021.Day12.State

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

  def search(open_set, count, routes) do
    complete_count =
      Enum.count(open_set, fn state ->
        List.first(state.path) == "end"
      end)

    Enum.flat_map(open_set, fn state -> next_states(state, routes) end)
    |> search(count + complete_count, routes)
  end

  def next_states(state, routes) do
    here = List.first(state.path)

    if here == "end" do
      []
    else
      Map.get(routes, here)
      |> Enum.filter(fn room -> room != "start" end)
      |> Enum.filter(fn room -> big?(room) || small_room_allowed(state, room) end)
      |> Enum.map(fn room -> State.add_room(state, room) end)
    end
  end

  def small_room_allowed(state = %State{}, room) do
    if state.doubled_small? do
      !Enum.member?(state.path, room)
    else
      Enum.count(state.path, fn x -> x == room end) < 2
    end
  end

  def part1(filename) do
    routes = parse(filename)
    open_set = [State.new(["start"], true)]
    search(open_set, 0, routes)
  end

  def part2(filename) do
    routes = parse(filename)
    open_set = [State.new(["start"], false)]
    search(open_set, 0, routes)
  end
end
