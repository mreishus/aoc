defmodule Elixir2021.Day04.BingoBoard do
  alias Elixir2021.Day04.BingoBoard

  defstruct [
    :grid,
    :marks,
    :lookup,
    :max_x,
    :max_y
  ]

  def build_marks(max_x, max_y) do
    0..max_x
    |> Enum.reduce(%{}, fn x, acc ->
      0..max_y
      |> Enum.reduce(acc, fn y, acc2 ->
        Map.put(acc2, {x, y}, false)
      end)
    end)
  end

  def build_lookups(grid, max_x, max_y) do
    0..max_x
    |> Enum.reduce(%{}, fn x, acc ->
      0..max_y
      |> Enum.reduce(acc, fn y, acc2 ->
        num = grid[{x, y}]
        Map.put(acc2, num, {x, y})
      end)
    end)
  end

  def new(grid) when is_map(grid) do
    {max_x, _} = grid |> Map.keys() |> Enum.max_by(fn {x, _y} -> x end)
    {_, max_y} = grid |> Map.keys() |> Enum.max_by(fn {_x, y} -> y end)

    %BingoBoard{
      grid: grid,
      marks: build_marks(max_x, max_y),
      lookup: build_lookups(grid, max_x, max_y),
      max_x: max_x,
      max_y: max_y
    }
  end
end

defmodule Elixir2021.Day04 do
  alias Elixir2021.Day04.BingoBoard

  def parse(filename) do
    [numbers | boards] =
      File.read!(filename)
      |> String.trim()
      |> String.split("\n\n")

    numbers =
      numbers
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)

    boards =
      boards
      |> Enum.map(fn x -> parse_board(x) end)

    %{
      numbers: numbers,
      boards: boards
    }
  end

  @doc """

  input (string):
  "14 21 17 24  4
  10 16 15  9 19
  18  8 23 26 20
  22 11 13  6  5
   2  0 12  3  7"

  output:
    %Elixir2021.Day04.BingoBoard{
      grid: %{
        {0, 0} => 14,
        {0, 1} => 10,
        {0, 2} => 18,
        {0, 3} => 22,
        {0, 4} => 2,
        {1, 0} => 21,
        {1, 1} => 16,
        {1, 2} => 8,
        {1, 3} => 11,
        {1, 4} => 0,
        {2, 0} => 17,
        {2, 1} => 15,
        {2, 2} => 23,
        {2, 3} => 13,
        {2, 4} => 12,
        {3, 0} => 24,
        {3, 1} => 9,
        {3, 2} => 26,
        {3, 3} => 6,
        {3, 4} => 3,
        {4, 0} => 4,
        {4, 1} => 19,
        {4, 2} => 20,
        {4, 3} => 5,
        {4, 4} => 7
      },
      marks: %{
        {0, 0} => false,
        {0, 1} => false,
        {0, 2} => false,
        {0, 3} => false,
        {0, 4} => false,
        {1, 0} => false,
        {1, 1} => false,
        {1, 2} => false,
        {1, 3} => false,
        {1, 4} => false,
        {2, 0} => false,
        {2, 1} => false,
        {2, 2} => false,
        {2, 3} => false,
        {2, 4} => false,
        {3, 0} => false,
        {3, 1} => false,
        {3, 2} => false,
        {3, 3} => false,
        {3, 4} => false,
        {4, 0} => false,
        {4, 1} => false,
        {4, 2} => false,
        {4, 3} => false,
        {4, 4} => false
      },
      lookup: %{
        0 => {1, 4},
        2 => {0, 4},
        3 => {3, 4},
        4 => {4, 0},
        5 => {4, 3},
        6 => {3, 3},
        7 => {4, 4},
        8 => {1, 2},
        9 => {3, 1},
        10 => {0, 1},
        11 => {1, 3},
        12 => {2, 4},
        13 => {2, 3},
        14 => {0, 0},
        15 => {2, 1},
        16 => {1, 1},
        17 => {2, 0},
        18 => {0, 2},
        19 => {4, 1},
        20 => {4, 2},
        21 => {1, 0},
        22 => {0, 3},
        23 => {2, 2},
        24 => {3, 0},
        26 => {3, 2}
      },
      max_x: 4,
      max_y: 4
    }
  """
  def parse_board(input) do
    input
    |> String.split("\n")
    |> Enum.zip(0..9999)
    |> Enum.flat_map(&parse_board_line/1)
    |> Map.new()
    |> BingoBoard.new()
  end

  @doc """
  input:
  {"18  8 23 26 20", 2}
  output:
  [{{0, 2}, 18}, {{1, 2}, 8}, {{2, 2}, 23}, {{3, 2}, 26}, {{4, 2}, 20}]
  """
  def parse_board_line({input_string, row}) do
    input_string
    |> String.split()
    |> Enum.map(&String.to_integer/1)
    |> Enum.zip(0..9999)
    |> Enum.map(fn {num, col} ->
      {{col, row}, num}
    end)
  end

  # Input: Board and a number
  # Output: Board with that number marked off
  def mark_number(board, num) do
    if Map.has_key?(board.lookup, num) do
      coord = board.lookup[num]
      new_marks = board.marks |> Map.put(coord, true)
      %{board | marks: new_marks}
    else
      board
    end
  end

  def is_board_winner(board) do
    0..board.max_x
    |> Enum.any?(fn x ->
      Enum.all?(0..board.max_y, fn y ->
        Map.get(board.marks, {x, y})
      end)
    end) ||
      0..board.max_y
      |> Enum.any?(fn y ->
        Enum.all?(0..board.max_x, fn x ->
          Map.get(board.marks, {x, y})
        end)
      end)
  end

  def score_board(board, last_num) do
    # Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. 
    # Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

    score =
      0..board.max_x
      |> Enum.reduce(0, fn x, acc ->
        0..board.max_y
        |> Enum.reduce(acc, fn y, acc2 ->
          if Map.get(board.marks, {x, y}) do
            acc2
          else
            acc2 + board.grid[{x, y}]
          end
        end)
      end)

    score * last_num
  end

  def part1(filename) do
    %{numbers: numbers, boards: boards} = parse(filename)

    ## Figure out which bingo board wins first, then
    ## Compute the score of that board

    [last_num, boards] =
      numbers
      |> Enum.reduce_while([-1, boards], fn num, [_last_num, acc_boards] ->
        acc_boards =
          acc_boards
          |> Enum.map(fn this_board ->
            mark_number(this_board, num)
          end)

        if Enum.any?(Enum.map(acc_boards, &is_board_winner/1)) do
          {:halt, [num, acc_boards]}
        else
          {:cont, [num, acc_boards]}
        end
      end)

    boards
    |> Enum.find(&is_board_winner/1)
    |> score_board(last_num)
  end

  def part2(filename) do
    %{numbers: numbers, boards: boards} = parse(filename)

    ## Figure out which bingo board wins last, then
    ## Compute the score of that board
    [last_num, last_board] =
      numbers
      |> Enum.reduce_while([-1, boards], fn num, [_last_num, acc_boards] ->
        acc_boards =
          acc_boards
          |> Enum.map(fn this_board ->
            mark_number(this_board, num)
          end)

        losing_boards = acc_boards |> Enum.reject(&is_board_winner/1)

        if length(losing_boards) == 0 do
          {:halt, [num, Enum.at(acc_boards, 0)]}
        else
          {:cont, [num, losing_boards]}
        end
      end)

    score_board(last_board, last_num)
  end
end
