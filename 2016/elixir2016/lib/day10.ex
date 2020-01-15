defmodule Elixir2016.Day10 do
  alias Elixir2016.Day10.Bot

  def part1_and_2(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Stream.map(&parse/1)
    |> Enum.to_list()
    |> create_bots()
    |> send_values()

    %{tokens: tokens_0} = Bot.output_name(0) |> Bot.state()
    %{tokens: tokens_1} = Bot.output_name(1) |> Bot.state()
    %{tokens: tokens_2} = Bot.output_name(2) |> Bot.state()

    p2_answer =
      (tokens_0 ++ tokens_1 ++ tokens_2)
      |> Enum.reduce(fn x, acc -> x * acc end)

    "Part 1: One of the bots printed to console above.  Part 2: " <> Integer.to_string(p2_answer)
  end

  def create_bots(commands) do
    commands
    |> Enum.filter(fn command -> elem(command, 0) == :bot end)
    |> Enum.each(fn {:bot, num, give_low, give_high} ->
      maybe_create_output(give_low)
      maybe_create_output(give_high)
      Bot.start(Bot.bot_name(num), give_low, give_high)
    end)

    commands
  end

  def send_values(commands) do
    commands
    |> Enum.filter(fn command -> elem(command, 0) == :value end)
    |> Enum.each(fn {:value, val_num, bot_num} ->
      Bot.give_val(Bot.bot_name(bot_num), val_num)
    end)

    commands
  end

  # Starts an "Output" bot if it doesn't exist
  def maybe_create_output({:global, "output_" <> _num} = name) do
    if GenServer.whereis(name) == nil do
      Bot.start(name, nil, nil)
    end
  end

  def maybe_create_output(_), do: nil

  # "value 5 goes to bot 2" -> {:value, 5, 2}
  # "bot 1 gives low to output 1 and high to bot 0" -> {:bot, {:output, 1}, {:bot, 0}}
  def parse(string) do
    find_value = ~r/value (\d+) goes to bot (\d+)/
    find_bot = ~r/bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)/

    cond do
      Regex.match?(find_value, string) ->
        [_ | groups] = Regex.run(find_value, string)
        groups = groups |> Enum.map(&String.to_integer/1)
        {:value, Enum.at(groups, 0), Enum.at(groups, 1)}

      Regex.match?(find_bot, string) ->
        [_, bot_num | groups] = Regex.run(find_bot, string)
        bot_num = String.to_integer(bot_num)

        [low, high] =
          Enum.chunk_every(groups, 2)
          |> Enum.map(&parse_bot_chunk/1)

        {:bot, bot_num, low, high}

      true ->
        raise "Can't parse"
    end
  end

  def parse_bot_chunk(["output", str]), do: Bot.output_name(str)
  def parse_bot_chunk(["bot", str]), do: Bot.bot_name(str)
  def parse_bot_chunk(_), do: raise("Can't parse 2")
end

defmodule Elixir2016.Day10.Bot do
  use GenServer
  alias Elixir2016.Day10.Bot

  def bot_name(num) when is_integer(num), do: {:global, "bot_" <> Integer.to_string(num)}
  def bot_name(num) when is_binary(num), do: {:global, "bot_" <> num}

  def output_name(num) when is_integer(num), do: {:global, "output_" <> Integer.to_string(num)}
  def output_name(num) when is_binary(num), do: {:global, "output_" <> num}

  def start(my_name, give_low, give_high) do
    # my_name |> IO.inspect(label: "bot starting")
    GenServer.start(__MODULE__, {give_low, give_high, my_name}, name: my_name)
  end

  def state(pid) do
    GenServer.call(pid, :state)
  end

  # Bot.give_val(Bot.bot_name(num), val_num)
  def give_val(pid, val) do
    GenServer.call(pid, {:give_val, val})
  end

  #### Implementation ####

  def init({give_low, give_high, my_name}) do
    {:ok, %{give_low: give_low, give_high: give_high, tokens: [], my_name: my_name}}
  end

  def handle_call(:state, _from, state) do
    {:reply, state, state}
  end

  def handle_call({:give_val, val}, _from, state) do
    new_tokens = [val | state.tokens]

    state =
      %{state | tokens: new_tokens}
      |> check_for_two_tokens()

    {:reply, :ok, state}
  end

  def check_for_two_tokens(
        %{tokens: tokens, give_low: give_low, give_high: give_high, my_name: my_name} = state
      )
      when length(tokens) >= 2 and not is_nil(give_low) and not is_nil(give_high) do
    tokens = Enum.sort(tokens)

    if tokens == [17, 61] do
      "Found bot comparing [17,61]" |> IO.inspect()
      my_name |> IO.inspect(label: "Part 1 answer")
    end

    Bot.give_val(give_low, Enum.at(tokens, 0))
    Bot.give_val(give_high, Enum.at(tokens, 1))
    %{state | tokens: []}
  end

  def check_for_two_tokens(state), do: state
end
