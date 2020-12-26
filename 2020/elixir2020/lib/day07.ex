defmodule Elixir2020.Day07 do
  ## Returns contained list like:

  ## "List" example. It's parsed yet, but not in a map form,
  ## this gets transformed to "contains" and "contained in" maps
  # [
  # {"drab blue", [{3, "wavy tomato"}]},
  # {"dull teal", [{5, "drab fuchsia"}, {4, "dim black"}]},
  # {"drab aqua", [{3, "dark red"}]},
  # ]
  def parse(filename) do
    list =
      File.stream!(filename)
      |> Enum.map(&String.trim/1)
      |> Enum.map(&parse_line/1)

    %{
      contains: list_to_contains(list),
      contained_in: list_to_contained_in(list)
    }
  end

  ## "Contains" example
  # %{
  #   "bright white" => [{1, "shiny gold"}],
  #   "dark olive" => [{3, "faded blue"}, {4, "dotted black"}],
  #   "dark orange" => [{3, "bright white"}, {4, "muted yellow"}],
  #   "dotted black" => [],
  #   "faded blue" => [],
  #   "light red" => [{1, "bright white"}, {2, "muted yellow"}],
  #   "muted yellow" => [{2, "shiny gold"}, {9, "faded blue"}],
  #   "shiny gold" => [{1, "dark olive"}, {2, "vibrant plum"}],
  #   "vibrant plum" => [{5, "faded blue"}, {6, "dotted black"}]
  # }
  def list_to_contains(list) do
    list
    |> Enum.reduce(
      %{},
      fn {color, contains}, acc ->
        acc
        |> Map.put(color, contains)
      end
    )
  end

  ## "Contained in" example, opposite of contains
  # %{
  #   "bright white" => ["light red", "dark orange"],
  #   "dark olive" => ["shiny gold"],
  #   "dotted black" => ["dark olive", "vibrant plum"],
  #   "faded blue" => ["muted yellow", "dark olive", "vibrant plum"],
  #   "muted yellow" => ["light red", "dark orange"],
  #   "shiny gold" => ["bright white", "muted yellow"],
  #   "vibrant plum" => ["shiny gold"]
  # },
  def list_to_contained_in(list) do
    list
    |> Enum.reduce(
      %{},
      fn {color, contains}, acc ->
        z =
          contains
          |> Enum.reduce(
            %{},
            fn {_qty, color_in}, inner_acc ->
              Map.update(inner_acc, color_in, [color], fn inner_list -> [color | inner_list] end)
            end
          )

        Map.merge(acc, z, fn _k, v1, v2 -> v1 ++ v2 end)
      end
    )
  end

  def parse_line(line) do
    # "shiny violet bags contain 1 faded brown bag, 1 dull red bag."
    [_, color, rest] = Regex.run(~r/^(\w+ \w+) bags contain (.*)$/, line)
    {color, parse_rest(rest)}
  end

  def parse_rest(rest) do
    # 1 faded brown bag, 1 dull red bag."
    Regex.scan(~r'(\d+) (\w+ \w+) bags?[,.]', rest)
    |> Enum.map(fn [_, num, color] ->
      {String.to_integer(num), color}
    end)
  end

  def has_gold(contained_in, current) do
    if Map.has_key?(contained_in, current) do
      outside = Map.get(contained_in, current)

      (Enum.flat_map(outside, fn color ->
         has_gold(contained_in, color)
       end) ++ [outside])
      |> List.flatten()
    else
      []
    end
  end

  def count(contains, color) do
    Map.get(contains, color)
    |> Enum.reduce(0, fn {qty, inner_color}, acc ->
      acc + qty * (count(contains, inner_color) + 1)
    end)
  end

  def part1(filename) do
    parse(filename)
    |> Map.get(:contained_in)
    |> has_gold("shiny gold")
    |> Enum.uniq()
    |> Enum.count()
  end

  def part2(filename) do
    parse(filename)
    |> Map.get(:contains)
    |> count("shiny gold")
  end
end
