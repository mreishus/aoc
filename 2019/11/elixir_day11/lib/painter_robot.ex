defmodule ElixirDay11.PainterRobot do
  alias ElixirDay11.{PainterRobot, ComputerServer}

  defstruct [
    :program,
    :location,
    :direction,
    :grid,
    :computer_pid
  ]

  def new(program, initial_square_color) do
    {:ok, pid} = ComputerServer.start(program, [])

    %PainterRobot{
      program: program,
      location: {0, 0},
      direction: :up,
      grid: new_grid(initial_square_color),
      computer_pid: pid
    }
  end

  def new_grid(initial_square_color) do
    %{
      {0, 0} => initial_square_color
    }
  end

  def execute(%PainterRobot{} = robot) do
    Stream.iterate(0, fn x -> x end)
    |> Enum.reduce_while(robot, fn _, robot ->
      robot = send_input(robot)

      if halted?(robot) do
        {:halt, robot}
      else
        robot = half_step(robot)
        {:cont, robot}
      end
    end)
  end

  def halted?(%PainterRobot{computer_pid: computer_pid}) do
    ComputerServer.halted?(computer_pid)
  end

  def send_input(
        %PainterRobot{grid: grid, location: location, computer_pid: computer_pid} = robot
      ) do
    current_square = Map.get(grid, location, 0)
    ComputerServer.add_input(computer_pid, current_square)
    robot
  end

  # A full step is: send_input(), check for halt, half_step()
  def half_step(
        %PainterRobot{
          grid: grid,
          location: location,
          direction: direction,
          computer_pid: computer_pid
        } = robot
      ) do
    if ComputerServer.halted?(computer_pid) do
      robot
    else
      paint_color = ComputerServer.pop_output(computer_pid)
      turn_dir = ComputerServer.pop_output(computer_pid)

      new_grid = Map.put(grid, location, paint_color)
      new_direction = turn(direction, turn_dir)
      new_location = advance(location, new_direction)
      %PainterRobot{robot | grid: new_grid, direction: new_direction, location: new_location}
    end
  end

  def count_painted_squares(%PainterRobot{grid: grid}) do
    grid
    |> Map.keys()
    |> Enum.count()
  end

  def display(%PainterRobot{grid: grid}) do
    {min_x, max_x} = grid |> Map.keys() |> Enum.map(fn {x, _y} -> x end) |> Enum.min_max()
    {min_y, max_y} = grid |> Map.keys() |> Enum.map(fn {_x, y} -> y end) |> Enum.min_max()

    min_y..max_y
    |> Enum.map(fn y -> display_row(grid, y, min_x, max_x) end)
    |> Enum.intersperse("\n")
  end

  def display_row(grid, y, min_x, max_x) do
    min_x..max_x
    |> Enum.map(fn x -> Map.get(grid, {x, y}, 0) end)
    |> Enum.map(fn char -> display_char(char) end)
  end

  def display_char(1), do: "#"
  def display_char(_), do: " "

  def advance({x, y}, :left), do: {x - 1, y}
  def advance({x, y}, :right), do: {x + 1, y}
  def advance({x, y}, :up), do: {x, y - 1}
  def advance({x, y}, :down), do: {x, y + 1}

  def turn(direction, 0), do: do_turn(direction, :left)
  def turn(direction, 1), do: do_turn(direction, :right)

  def do_turn(:up, :left), do: :left
  def do_turn(:left, :left), do: :down
  def do_turn(:down, :left), do: :right
  def do_turn(:right, :left), do: :up

  def do_turn(:up, :right), do: :right
  def do_turn(:right, :right), do: :down
  def do_turn(:down, :right), do: :left
  def do_turn(:left, :right), do: :up
end
