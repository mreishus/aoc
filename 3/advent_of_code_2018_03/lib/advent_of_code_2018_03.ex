defmodule Claim do
  defstruct [
    id: 0,
    x: 0,
    y: 0,
    width: 0,
    height: 0
  ]
end

defmodule AdventOfCode201803 do
  # void -> List of text
  def read_file(filename) do
    file_name = Path.expand("./", __DIR__) |> Path.join(filename)
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  # List of text -> List of claims
  def parse_file(data) do
    data
      |> Enum.map(&replace_non_digits_with_space/1)
      |> Enum.map(&file_line_to_claim/1)
  end

  # Text with punctuation removed -> Claim
  def file_line_to_claim(line) do
    [id, x, y, width, height] = String.split(line, " ", trim: true) 
                                |> Enum.map(&String.to_integer/1)
    %Claim{
      id: id,
      x: x,
      y: y,
      width: width,
      height: height
    }
  end

  # text -> text with punctuation turned to space
  def replace_non_digits_with_space(line), do: Regex.replace(~r/\D+/, line, " ")

  # grid size -> empty grid (map with tuple(x,y) as key and empty list [] as value)
  def init_grid(size) do
    1..size |> Enum.reduce(%{}, fn x, acc ->
      1..size |> Enum.reduce(acc, fn y, acc ->
        Map.put(acc, {x, y}, [])
      end)
    end)
  end

  # grid, claim -> grid with claim applied
  def apply_claim(grid, claim) do
    claim.x..(claim.x + claim.width - 1) |> Enum.reduce(grid, fn x, acc ->
      claim.y..(claim.y + claim.height - 1) |> Enum.reduce(acc, fn y, acc ->
        new_value = acc[{x, y}] ++ [claim.id]
        Map.put(acc, {x, y}, new_value)
      end)
    end)
  end

  # grid (with claims applied), size -> How many squares have more than 1 claim?
  def overlapping_squares(grid, size) do
    1..size |> Enum.reduce(0, fn x, acc ->
      1..size |> Enum.reduce(acc, fn y, acc ->
        case (length(grid[{x, y}]) > 1) do
          true -> acc + 1
          false -> acc
        end
      end)
    end)
  end

  def uncontested_claims(grid, claims, size) do
    1..size |> Enum.reduce(claims, fn x, acc ->
      1..size |> Enum.reduce(acc, fn y, acc ->
        this_square_claim_ids = grid[{x, y}]
        case (length(this_square_claim_ids) > 1) do
          true -> acc
            |> Enum.filter(fn x -> !Enum.member?(this_square_claim_ids, x.id) end)
          false -> acc
        end
      end)
    end)
  end

  def solve(filename, grid_size) do
    claims = read_file(filename)
      |> parse_file()

    grid = claims
      |> Enum.reduce(init_grid(grid_size), fn claim, acc ->
        apply_claim(acc, claim)
      end)

    # pt 1
    overlap = overlapping_squares(grid, grid_size)
    # pt 2
    uncontested = uncontested_claims(grid, claims, grid_size)
    {overlap, uncontested}
  end

  def go do
    filename = "input.txt"
    grid_size = 1000

    {overlap, uncontested} = solve(filename, grid_size)

    IO.puts "[Part 1]: overlapping squares:"
    IO.puts overlap
    IO.puts "[Part 2]: claims that don't overlap:"
    IO.inspect uncontested |> Enum.map(fn x -> x.id end)
  end
end
