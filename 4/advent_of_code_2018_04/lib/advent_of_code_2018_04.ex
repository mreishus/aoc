defmodule AdventOfCode201804 do
  def read_file() do
    file_name = Path.expand("./", __DIR__) |> Path.join("input.txt")
    {:ok, contents} = File.read(file_name)
    contents
      |> String.split("\n", trim: true)
  end

  # input: list of unparsed strings
  # output: list of tuples, 0th element is guard number, 1st element is string. "
  # "begin shift" lines are removed
  # example..
  #[
  #    {10, "[1518-11-01 00:05] falls asleep"},
  #    {10, "[1518-11-01 00:25] wakes up"},
  #
  def add_guard([line | lines], guard_num) do
    case Regex.match?(~r/begins shift/, line) do
      true -> add_guard(lines, get_guard(line))
      false -> [ {guard_num, line} | add_guard(lines, guard_num) ]
    end
  end

  def add_guard([], _guard_num) do
    []
  end

  def guard_lines_to_ranges(lines) do
    chunked_lines = lines |> Enum.chunk_every(2)
    chunked_lines
      |> Enum.map(fn [{sleep_guard, sleep_text}, {wake_guard, wake_text}] ->
        sleep_valid = Regex.match?(~r/falls asleep/, sleep_text)
        wake_valid = Regex.match?(~r/wakes up/, wake_text)
        if !sleep_valid || !wake_valid || (sleep_guard != wake_guard) do
          raise "Invalid data"
        end
        range = parse_range(sleep_text, wake_text)
        Map.put(range, :guard_id, sleep_guard)
      end)
  end

  def parse_range(sleep_text, wake_text) do
    sleep_date = parse_date(sleep_text)
    wake_date = parse_date(wake_text)
    asleep_mins_count = wake_date.composite_min - sleep_date.composite_min
    asleep_mins_list = sleep_date.composite_min..(wake_date.composite_min-1) |> Enum.to_list
    %{asleep_mins_count: asleep_mins_count,
      asleep_mins_list: asleep_mins_list,
      sleep_date: sleep_date,
      wake_date: wake_date}
  end

  def parse_date(line) do
    [_year, _month, day, hour, min] = Regex.run(~r/\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]/, line)
                              |> List.delete_at(0)
                              |> Enum.map(fn x -> String.to_integer(x) end)
    #%{year: year, month: month, day: day, hour: hour, min: min, composite_min: 60 * hour + min}
    %{day: day, hour: hour, min: min, composite_min: 60 * hour + min}
  end

  # line containing guard number -> guard number
  def get_guard(line) do
    [_, guard_num] = Regex.run(~r/#(\d+)/, line)
    guard_num |> String.to_integer
  end
  # Make this a test
  #line = "[1518-11-01 00:00] Guard #10 begins shift"
  #g = get_guard(line)
  #IO.inspect g

  def ranges_to_sleep_time_by_guard(ranges) do
    ranges
    |> Enum.reduce(%{}, fn range, acc ->
      Map.put(acc, range.guard_id, (acc[range.guard_id] || 0) + range.asleep_mins_count)
    end)
  end

  def get_most_slept_minute_for_guard(guard_id, ranges) do
    ranges
      |> Enum.filter(fn x -> x.guard_id == guard_id end)
      |> Enum.map(fn x -> x.asleep_mins_list end)
      |> List.flatten()
      |> Enum.group_by(fn(x) -> x end)
      |> Enum.reduce(%{}, fn({k, v}, acc) -> Map.put(acc, k, Enum.count(v)) end)
      |> Map.to_list()
      |> Enum.max_by(fn {_sleep_minute, occurances} -> occurances end)
  end

  def go do
    lines = read_file()
      |> Enum.sort()
      |> add_guard(-1)

    ranges = lines
      |> guard_lines_to_ranges()

    most_sleepy_guard = ranges
      |> ranges_to_sleep_time_by_guard()
      |> Map.to_list()
      |> Enum.max_by(fn {_guard_id, sleep_time} -> sleep_time end)
      |> elem(0)

    most_sleepy_guard_most_often_slept_minute = 
      get_most_slept_minute_for_guard(most_sleepy_guard, ranges)
      |> elem(0)

    IO.puts ""
    IO.puts "[Part 1, most sleepy guard and most slept minute]:"
    IO.puts "Most sleepy guard: "
    IO.puts most_sleepy_guard
    IO.puts "Minute most often slept for that guard: "
    IO.puts most_sleepy_guard_most_often_slept_minute

    IO.puts ""
    IO.puts "[Part 2]"
    IO.puts "Which guard was most frequently asleep on the same minute?"
    guard_ids = ranges
      |> Enum.map(fn x -> x.guard_id end)
      |> Enum.uniq

    most_often_slept_minutes_by_guard = guard_ids 
      |> Enum.reduce([], fn guard_id, acc ->
        {sleep_minute, occurances} = get_most_slept_minute_for_guard(guard_id, ranges)
        r = %{sleep_minute: sleep_minute, occurances: occurances, guard_id: guard_id}
        [r | acc]
      end)
    pt2_answer = most_often_slept_minutes_by_guard
      |> Enum.max_by(fn %{guard_id: guard_id, occurances: occurances, sleep_minute: sleep_minute} -> occurances end )
    IO.inspect pt2_answer
  end
end
