defmodule ElixirDay13.Breakout do
  alias ElixirDay13.{Breakout, Computer}

  defstruct [
    :grid,
    :computer
  ]

  @paddle 3
  @ball 4

  def new(program) do
    %Breakout{
      grid: %{},
      computer: Computer.new(program, [])
    }
  end

  def run(%Breakout{computer: computer} = b) do
    new_computer =
      computer
      |> Computer.set_memory(0, 2)
      |> Computer.execute()

    %Breakout{b | computer: new_computer}
    |> write_outputs_to_grid()
  end

  ## Called by run(), you shouldn't need to call this on its own
  defp write_outputs_to_grid(%Breakout{computer: computer, grid: grid} = b) do
    if Computer.has_output?(computer) do
      {x, computer} = Computer.pop_output(computer)
      {y, computer} = Computer.pop_output(computer)
      {what, computer} = Computer.pop_output(computer)
      grid = Map.put(grid, {x, y}, what)

      %Breakout{b | grid: grid, computer: computer}
      |> write_outputs_to_grid()
    else
      b
    end
  end

  def game_loop(%Breakout{computer: computer, grid: grid} = b) do
    if Computer.halted?(computer) do
      b
    else
      move = get_move(b)
      computer = Computer.add_input(computer, move)

      %{b | computer: computer}
      |> run()
      |> game_loop()
    end
  end

  def get_move(%Breakout{grid: grid}) do
    {{paddle_x, _paddle_y}, _paddle} =
      grid
      |> Enum.filter(fn {k, v} -> v == @paddle end)
      |> List.first()

    {{ball_x, _ball_y}, _ball} =
      grid
      |> Enum.filter(fn {k, v} -> v == @ball end)
      |> List.first()

    cond do
      ball_x > paddle_x -> 1
      ball_x < paddle_x -> -1
      true -> 0
    end
  end

  def part1(program) do
    new(program)
    |> run()
    |> grid_count(2)
  end

  def grid_count(%Breakout{grid: grid}, target) do
    grid
    |> Map.values()
    |> Enum.filter(fn x -> x == target end)
    |> Enum.count()
  end

  def part2(program) do
    new(program)
    |> run()
    |> game_loop()
    |> score()
  end

  def score(%Breakout{grid: grid}) do
    grid |> Map.get({-1, 0})
  end
end
