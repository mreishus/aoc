defmodule AdventOfCode201807 do
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.trim()
      |> String.split("\n", trim: true)
  end

  def add_empty_array_under_key_if_missing(map, key) do
      case map[key] == nil do
        true  -> put_in(map[key], [])
        false -> map
      end
  end

  def parse_lines(lines) do
    lines
        |> Enum.map(&parse_line/1)
        |> Enum.reduce(%{}, fn [do_first, do_next], acc -> 
          acc = acc
            |> add_empty_array_under_key_if_missing(do_next)
            |> add_empty_array_under_key_if_missing(do_first)
          {_, acc} = get_and_update_in(acc, [do_next], fn x -> {x, [do_first | x]} end)
          acc
        end)
  end

  def parse_line(line) do
    regex = ~r/Step (\w+) must be finished before step (\w+) can begin./
    [_do_first, _do_next] = Regex.run(regex, line) |> List.delete_at(0)
  end

  @doc """
  iex> AdventOfCode201807.parse_file("input_small.txt")
  %{
      "A" => ["C"],
      "B" => ["A"],
      "C" => [],
      "D" => ["A"],
      "E" => ["F", "D", "B"],
      "F" => ["C"]
  }
  """
  def parse_file(filename) do
    read_file(filename)
      |> parse_lines()
  end

  @doc """
  iex> AdventOfCode201807.go()
  true
  """
  def go do
    deps = parse_file("input.txt")
    IO.inspect deps
    a = part1(deps)
    IO.inspect a
    IO.puts "go"
    true
  end

  def part1(deps) do
    task_order([], deps) |> Enum.join
  end

  @doc """
  iex> AdventOfCode201807.task_order([], %{ "A" => ["C"], "B" => ["A"], "C" => [], "D" => ["A"], "E" => ["F", "D", "B"], "F" => ["C"] })
  ["C", "A", "B", "D", "F", "E"]
  """
  def task_order(result, deps) do
    next_step = do_next(deps)
    result = [ next_step | result ]

    new_deps = Map.delete(deps, next_step)
    new_deps = Map.keys(new_deps)
    |> Enum.reduce(new_deps, fn x, acc ->
      vals = acc[x] |> Enum.filter(fn y -> y != next_step end)
      Map.put(acc, x, vals)
    end)

    case length(Map.keys(new_deps)) do
      0 -> result |> Enum.reverse()
      _ -> task_order(result, new_deps)
    end
  end

  @doc """
  iex> AdventOfCode201807.do_next(%{ "A" => ["C"], "B" => ["A"], "C" => [], "D" => ["A"], "E" => ["F", "D", "B"], "F" => ["C"] })
  "C"
  iex> AdventOfCode201807.do_next(%{ "A" => ["C"], "B" => ["A"], "C" => [], "AAA" => [], "D" => ["A"], "E" => ["F", "D", "B"], "F" => ["C"] })
  "AAA"
  iex> AdventOfCode201807.do_next(%{ "A" => ["C"], "B" => ["A"], "D" => ["A"], "E" => ["F", "D", "B"], "F" => ["C"] })
  nil
  """
  def do_next(deps) do
    deps 
      |> Map.to_list() 
      |> Enum.filter(fn {_task, deps} -> length(deps) == 0 end) 
      |> Enum.map(fn x -> elem(x, 0) end) 
      |> Enum.sort()
      |> List.first()
  end
end
