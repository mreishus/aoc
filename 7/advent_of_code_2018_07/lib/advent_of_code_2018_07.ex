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
    deps = lines
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
    [do_first, do_next] = Regex.run(regex, line) |> List.delete_at(0)
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
    read_file("input_small.txt")
      |> parse_lines()
  end

  @doc """
  iex> AdventOfCode201807.go()
  true
  """
  def go do
    deps = parse_file("input_small.txt")
    IO.inspect deps
    IO.puts "go"
    true
  end
end
