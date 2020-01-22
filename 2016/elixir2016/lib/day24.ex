defmodule Elixir2016.Day24 do
  @doc """
  Turns a filename into a map representing a maze,
  that looks like this:
  %{
    {3, 3} => %{key: nil, wall: false},
    {4, 0} => %{key: nil, wall: true},
    {2, 1} => %{key: nil, wall: false},
    {2, 2} => %{key: nil, wall: true},
    {6, 4} => %{key: nil, wall: true},
    {0, 0} => %{key: nil, wall: true},
    {2, 0} => %{key: nil, wall: true},
    {3, 1} => %{key: "1", wall: false},
    ...
  }
  """
  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
    |> parse_lines()
  end

  def parse_lines(lines) when is_list(lines) do
    lines
    |> Enum.zip(0..9999)
    |> Enum.flat_map(&parse_line/1)
    |> Map.new()
  end

  def parse_line({maze_string, row}) when is_binary(maze_string) and is_integer(row) do
    maze_string
    |> String.graphemes()
    |> Enum.zip(0..9999)
    |> Enum.map(fn {char, col} ->
      {{col, row}, parse_char(char)}
    end)
  end

  def parse_char("#"), do: %{wall: true, key: nil}
  def parse_char("."), do: %{wall: false, key: nil}
  def parse_char(num), do: %{wall: false, key: num}

  @doc """
  input: maze map from parse()
  output: %{num_keys: 5, start: {1, 1}}
  You always start with key 0.  So we will need to collect keys 1-4 for a total of 5 keys.
  """
  def maze_info(maze) do
    inverse_maze = for {k, v} <- maze, into: %{}, do: {v, k}
    start = inverse_maze |> Map.get(%{key: "0", wall: false})

    num_keys =
      Map.keys(inverse_maze) |> Enum.filter(fn %{key: key} -> key != nil end) |> Enum.count()

    %{start: start, num_keys: num_keys}
  end

  def part1(filename) do
    parse(filename)
    |> bfs(false)
  end

  def part2(filename) do
    parse(filename)
    |> bfs(true)
  end

  def bfs(maze, return_to_0) do
    maze_info = maze_info(maze)
    seen = MapSet.new()
    # first_state example: { {1, 1}, "0" } to represent standing at 1,1 holding "0" key
    first_state = {maze_info.start, MapSet.new(["0"])}

    config = %{
      maze: maze,
      maze_info: maze_info,
      return_to_0: return_to_0
    }

    config.maze_info.num_keys
    bfs([first_state], 0, seen, config)
  end

  @doc """
  open_set: List of states.  Example state: { {1, 1}, MapSet.new(["0"]) }.  Standing at 1,1 holding only the "0" key.
  num: Integer of steps taken.
  seen: MapSet of previously seen states.
  config: Map holding the following.
    :maze The maze, a map.
    :maze_info Maze info, example: %{num_keys: 5, start: {1, 1}}
  """
  def bfs(open_set, num, seen, config)
      when is_list(open_set) and is_integer(num) and is_map(config) do
    if contains_final?(open_set, config) do
      num
    else
      new_set =
        open_set
        |> Enum.flat_map(fn state -> next_states(state, config.maze) end)
        |> Enum.uniq()
        |> Enum.reject(fn state -> MapSet.member?(seen, state) end)

      seen = seen |> MapSet.union(MapSet.new(open_set))
      bfs(new_set, num + 1, seen, config)
    end
  end

  def contains_final?(open_set, config) when is_list(open_set) and is_map(config) do
    goal_keys = config.maze_info.num_keys

    if config.return_to_0 do
      open_set
      |> Enum.any?(fn {coord, keys} ->
        MapSet.size(keys) == goal_keys and coord == config.maze_info.start
      end)
    else
      open_set
      |> Enum.any?(fn {_coord, keys} ->
        MapSet.size(keys) == goal_keys
      end)
    end
  end

  def next_states({{x, y}, keys}, maze) do
    [
      {x + 1, y},
      {x - 1, y},
      {x, y + 1},
      {x, y - 1}
    ]
    |> Enum.filter(fn coord ->
      maze[coord].wall != true
    end)
    |> Enum.map(fn coord ->
      if maze[coord].key == nil do
        {coord, keys}
      else
        keys = MapSet.put(keys, maze[coord].key)
        {coord, keys}
      end
    end)
  end
end
