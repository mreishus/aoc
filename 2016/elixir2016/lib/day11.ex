defmodule Parallel do
  def pmap(collection, func) do
    collection
    |> Enum.map(&Task.async(fn -> func.(&1) end))
    |> Enum.map(&Task.await/1)
  end
end

defmodule Elixir2016.Day11 do
  def part1() do
    state = input_start()
    bfs([state], 0, MapSet.new())
  end

  def part2() do
    state = input_part2_start()
    bfs([state], 0, MapSet.new())
  end

  def bfs(open_set, num, seen) do
    if open_set |> Enum.any?(&final_state?/1) do
      num
    else
      next_open_set =
        open_set
        # Task.async_stream is slower
        |> Parallel.pmap(&next_states/1)
        |> Enum.concat()
        |> Enum.uniq()
        |> Enum.reject(fn state -> MapSet.member?(seen, state) end)

      if length(next_open_set) == 0 do
        nil
      else
        bfs(next_open_set, num + 1, MapSet.union(seen, MapSet.new(next_open_set)))
      end
    end
  end

  @doc """
  All possible combos of items you can take in the elevator.

  iex(3)> Elixir2016.Day11.item_combos(2)
  [{0, 1}, {0, nil}, {1, nil}]

  iex(1)> Elixir2016.Day11.item_combos(3)
  [{0, 1}, {0, 2}, {1, 2}, {0, nil}, {1, nil}, {2, nil}]
  """
  def item_combos(num_items) do
    pairs = for i <- 0..(num_items - 1), j <- i..(num_items - 1), i != j, do: {i, j}
    singles = for i <- 0..(num_items - 1), do: {i, nil}
    pairs ++ singles
  end

  def floors(floor) do
    [floor - 1, floor + 1]
    |> Enum.filter(fn x -> x >= 1 and x <= 4 end)
  end

  def next_states(state) do
    num_items = length(state[state.elevator])
    this_floor = state.elevator

    item_combos(num_items)
    |> Enum.flat_map(fn {i, j} ->
      floors(this_floor)
      |> Enum.map(fn next_floor ->
        # State with items {i, j}  moved from this_floor to next_floor
        update_state(state, {i, j}, this_floor, next_floor)
      end)
    end)
    |> Enum.map(&canonical_state/1)
    |> Enum.filter(&valid_state?/1)
  end

  # State with items {i, j}  moved from this_floor to next_floor
  # j might be nil
  def update_state(state, {i, j}, this_floor, next_floor) do
    items = state |> Map.get(this_floor)

    acc = {[], items}

    {moved_items, items_left} =
      [i, j]
      |> Enum.filter(fn x -> x != nil end)
      |> Enum.sort()
      |> Enum.reverse()
      |> Enum.reduce(acc, fn i, {moved_items, items_left} ->
        {new_item, items_left} = {Enum.at(items_left, i), List.delete_at(items_left, i)}
        {[new_item | moved_items], items_left}
      end)

    state
    |> Map.put(this_floor, Enum.sort(items_left))
    |> Map.update!(next_floor, fn items -> Enum.sort(Enum.concat(items, moved_items)) end)
    |> Map.put(:elevator, next_floor)
  end

  def valid_state?(state) do
    state
    |> Map.delete(:elevator)
    |> Map.values()
    |> Enum.all?(&valid_floor?/1)
  end

  def valid_floor?(floor) do
    floor
    |> Enum.reduce_while(true, fn item, _acc ->
      case item do
        {:chip, num} ->
          other_gen_exists =
            floor
            |> Enum.any?(fn {thing, a_num} -> thing == :gen and a_num != num end)

          safe =
            if other_gen_exists do
              Enum.member?(floor, {:gen, num})
            else
              true
            end

          if safe, do: {:cont, true}, else: {:halt, false}

        {:gen, _num} ->
          {:cont, true}
      end
    end)
  end

  def final_state?(state) do
    1..3
    |> Enum.all?(fn floor -> length(state[floor]) == 0 end)
  end

  # Moves a state to its "canonical" representation.
  # State A: 1 => [{:chip, 1}, {:gen, 1}], 2 => [{:chip, 4}, {:chip, 3}]
  # State A: 1 => [{:chip, 4}, {:gen, 4}], 2 => [{:chip, 1}, {:chip, 2}]
  # State A and B are really the same state.
  # Unsure about htis, is it too slow/complex?
  def canonical_state(state) do
    elevator = state.elevator

    # num_mapping looks like: %{1 => 1, 2 => 2, 3 => 5, 4 => 3, 5 => 4}
    num_mapping =
      state
      |> Map.delete(:elevator)
      |> Map.keys()
      |> Enum.sort()
      |> Enum.map(fn key -> state[key] end)
      |> Enum.flat_map(fn floor ->
        Enum.map(floor, fn {_thing, num} -> num end)
      end)
      |> Enum.uniq()
      |> Enum.zip(1..99)
      |> Enum.into(%{})

    state
    |> Map.delete(:elevator)
    |> Enum.reduce(%{}, fn {key, floor}, acc ->
      new_floor =
        floor
        |> Enum.map(fn {thing, num} -> {thing, num_mapping[num]} end)

      acc |> Map.put(key, new_floor)
    end)
    |> Map.put(:elevator, elevator)
  end

  def example_start() do
    # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    # The second floor contains a hydrogen generator.
    # The third floor contains a lithium generator.
    # The fourth floor contains nothing relevant.
    # F4 .  .  .  .  .
    # F3 .  .  .  LG .
    # F2 .  HG .  .  .
    # F1 E  .  HM .  LM
    # Hydogren: 1
    # Lithium: 2
    %{
      :elevator => 1,
      1 => Enum.sort([{:chip, 1}, {:chip, 2}]),
      2 => Enum.sort([{:gen, 1}]),
      3 => Enum.sort([{:gen, 2}]),
      4 => []
    }
  end

  def input_start() do
    # The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
    # The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
    # The third floor contains a thulium-compatible microchip.
    # The fourth floor contains nothing relevant.
    # strontium: 1
    # plutonium: 2
    # thulium: 3
    # ruthenium: 4
    # curium: 5
    %{
      :elevator => 1,
      1 => Enum.sort([{:gen, 1}, {:chip, 1}, {:gen, 2}, {:chip, 2}]),
      2 => Enum.sort([{:gen, 3}, {:gen, 4}, {:chip, 4}, {:gen, 5}, {:chip, 5}]),
      3 => Enum.sort([{:chip, 3}]),
      4 => []
    }
  end

  def input_part2_start() do
    # Upon entering the isolated containment area, however, you notice some extra parts on the first floor that weren't listed on the record outside:

    #     (6) An elerium generator.
    #     (6) An elerium-compatible microchip.
    #     (7) A dilithium generator.
    #     (7) A dilithium-compatible microchip.
    %{
      :elevator => 1,
      1 =>
        Enum.sort([
          {:gen, 1},
          {:chip, 1},
          {:gen, 2},
          {:chip, 2},
          {:gen, 6},
          {:chip, 6},
          {:gen, 7},
          {:chip, 7}
        ]),
      2 => Enum.sort([{:gen, 3}, {:gen, 4}, {:chip, 4}, {:gen, 5}, {:chip, 5}]),
      3 => Enum.sort([{:chip, 3}]),
      4 => []
    }
  end
end
