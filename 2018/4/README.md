# Advent Of Code 2018, Day 4

https://adventofcode.com/2018/day/4

This was a **time range** based problem.  Any experienced programmer knows that dealing with dates and times can be deceptively complex.  Thankfully, the problem was constructed in a way to avoid this complexity - even hours didn't matter.

**Languages Solved In:** Elixir

## Part 1

**Problem:** You're given a list of events with timestamps across several days:  Guard change events, guard falls asleep events, guard awakens events.  Find which guard slept the most minutes.  Which minute of the day was he most often asleep on?

**Approach, Elixir:** I first parsed the file by removing all guard change events and transforming the remaining lines into a tuple containing the active guard at that time and the event text.

Then, I transformed the event logs into an array of "Sleep Ranges", which were hashes including `sleep_date`, `wake_date`, `asleep_mins_count`, and `asleep_mins_list`.  The sleep ranges were collected into a Map with guard ids as keys and sleep ranges as values.

Using the list of sleep ranges, I found the guard who slept the most, by reducing the list of sleep ranges to a sum of minutes of slept and maxing by that:
```elixir
  def ranges_to_sleep_time_by_guard(ranges) do
    ranges
    |> Enum.reduce(%{}, fn range, acc ->
      Map.put(acc, range.guard_id, (acc[range.guard_id] || 0) + range.asleep_mins_count)
    end)
  end

    most_sleepy_guard = ranges
      |> ranges_to_sleep_time_by_guard()
      |> Map.to_list()
      |> Enum.max_by(fn {_guard_id, sleep_time} -> sleep_time end)
      |> elem(0)
```

Then, I found which was the most slept minute for that guard.  I used the `asleep_mins_list` I had built for each range, combined with`Enum.group_by` and `Enum.reduce` to find out how often each minute of the day was slept on.

```elixir
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
```

## Part 2

**Problem:** Of all guards, which guard is most frequently asleep on the same minute?

**Approach, Elixir**:  In part 1, I already built up the list of sleep ranges per guard in a map and a `get_most_slept_minute_for_guard` function. 

I modified the function to not only return the most slept minute, but the # of sleeps (`occurances`).  Then I could  compute it for each guard and find the maximum.

```elixir
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
```

