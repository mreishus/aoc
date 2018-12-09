defmodule AdventOfCode201807 do
  @extra_time 60
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
    b = part2(deps)
    IO.inspect b
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

    new_deps = remove_from_deps(deps, next_step)

    case length(Map.keys(new_deps)) do
      0 -> result |> Enum.reverse()
      _ -> task_order(result, new_deps)
    end
  end

  def remove_from_deps(deps, next_step) do
    new_deps = Map.delete(deps, next_step)
    Map.keys(new_deps)
      |> Enum.reduce(new_deps, fn x, acc ->
        vals = acc[x] |> Enum.filter(fn y -> y != next_step end)
        Map.put(acc, x, vals)
      end)
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

  def do_next_multiple(deps) do
    deps 
      |> Map.to_list() 
      |> Enum.filter(fn {_task, deps} -> length(deps) == 0 end) 
      |> Enum.map(fn x -> elem(x, 0) end) 
      |> Enum.sort()
  end

  @doc """
  iex> AdventOfCode201807.part2(%{ "A" => ["C"], "B" => ["A"], "C" => [], "D" => ["A"], "E" => ["F", "D", "B"], "F" => ["C"] })
  "asdf"
  """
  def part2(deps) do
    workers = make_workers(5)
    timer = 0
    tasks_finished = []

    [timer, _workers, _deps, _tasks_finished] = run_simulation(timer, workers, deps, tasks_finished)

    timer - 1
  end

  def run_simulation(timer, workers, deps, tasks_finished) do
    [timer, workers, deps, tasks_finished] = tick(timer, workers, deps, tasks_finished)
    case length(Map.keys(deps)) do
      0 -> [timer, workers, deps, tasks_finished]
      _ -> run_simulation(timer, workers, deps, tasks_finished)
    end
  end

  def tick(timer, workers, deps, tasks_finished) do
    ## Did anything just finish?
    just_finished = workers 
      |> Enum.filter(fn x -> x.done_on_second == timer end)
      |> Enum.map(fn x -> x.working_on end)
    tasks_finished = tasks_finished ++ just_finished

    ## Remove finished things from deps
    deps = just_finished
      |> Enum.reduce(deps, fn finished_step, acc ->
        remove_from_deps(acc, finished_step)
      end )

    ## Unassign workers on finished tasks
    workers = just_finished
      |> Enum.reduce(workers, fn finished_step, acc ->
        unassign_task(acc, finished_step)
      end )

    # Is there anything that can be done next?
    next_steps = do_next_multiple(deps)

    # Find out what's currently being worked on and filter that from next_steps
    working_on = workers |> Enum.map(fn x -> x.working_on end)
    next_steps = next_steps
                 |> Enum.filter(fn step -> !Enum.member?(working_on, step) end)

    # Assign the work
    workers = next_steps
              |> Enum.reduce(workers, fn next_step, acc_workers ->
                assign_work(next_step, acc_workers, timer)
              end)

    [timer+1, workers, deps, tasks_finished]
  end

  def unassign_task(workers, finished_step) do
    workers
      |> Enum.map(fn x -> 
        case x.working_on == finished_step do
          true -> %{done_on_second: nil, working_on: nil}
          false -> x
        end
      end)
  end

  def assign_work(next_step, [worker | workers], timer) do
    case worker.working_on do
      nil -> [ assign_to_worker(worker, next_step, timer) | workers ]
      _ -> [worker | assign_work(next_step, workers, timer)]
    end
  end

  def assign_work(_next_step, [], _timer) do
    []
  end

  def assign_to_worker(worker, next_step, timer) do
    %{worker | working_on: next_step, done_on_second: timer + time_to_do(next_step)}
  end

  def time_to_do(next_step) do
    (next_step |> String.to_charlist |> hd) - 64 + @extra_time
  end

  def replicate(n, x), do: for _ <- 1..n, do: x

  def make_workers(num) do
    replicate(num, %{working_on: nil, done_on_second: nil})
  end
end
