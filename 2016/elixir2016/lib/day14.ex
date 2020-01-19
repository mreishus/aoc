defmodule Elixir2016.Day14 do
  alias Elixir2016.Day14.{Hash, HashServer}

  def parse(filename) do
    File.stream!(filename)
    |> Stream.map(&String.trim/1)
    |> Enum.to_list()
    |> List.first()
  end

  def part1(filename) do
    salt = parse(filename)
    {:ok, pid} = HashServer.start(salt, false)
    find_64th_pad(pid)
  end

  def part2(filename) do
    salt = parse(filename)
    {:ok, pid} = HashServer.start(salt, true)
    find_64th_pad(pid)
  end

  def find_64th_pad(pid) do
    Stream.iterate(1, fn x -> x + 1 end)
    |> Stream.map(fn num -> HashServer.get(pid, num) end)
    |> Stream.filter(fn info -> info.triple end)
    |> Stream.filter(fn info ->
      num = info.num

      # Can't parallelize this - The Genserver can only process one request at a time
      (num + 1)..(num + 1000)
      |> Stream.map(fn inner_num -> HashServer.get(pid, inner_num) end)
      |> Enum.any?(fn inner_info ->
        inner_info.quint and Enum.member?(inner_info.quint_chars, info.triple_char)
      end)
    end)
    |> Enum.take(64)
    |> Stream.map(fn info -> info.num end)
    |> Enum.to_list()
    |> List.last()
  end
end

defmodule Elixir2016.Day14.Hash do
  ## MD5 Helper (String -> String)
  def md5(input) do
    :crypto.hash(:md5, input) |> Base.encode16(case: :lower)
  end

  def md5_salt_n(salt, n) when is_binary(salt) and is_integer(n) do
    md5(salt <> Integer.to_string(n))
  end

  def stretch_md5_salt_n(salt, n) when is_binary(salt) and is_integer(n) do
    input = salt <> Integer.to_string(n)

    1..2017
    |> Enum.reduce(input, fn _x, acc ->
      md5(acc)
    end)
  end

  def triple?(input_str) do
    Regex.match?(~r/(.)\1\1/, input_str)
  end

  # Example return value: "d" if the first triple is "ddd"
  def triple_char(input_str) do
    Regex.run(~r/(.)\1\1/, input_str) |> List.last()
  end

  def quint?(input_str) do
    Regex.match?(~r/(.)\1\1\1\1/, input_str)
  end

  # Example return value: ["c", "d", "k"] (multiple quints) or ["c"] (one quint)
  def quint_chars(input_str) do
    Regex.scan(~r/(.)\1\1\1\1/, input_str) |> Enum.map(&List.last/1)
  end

  def info(salt, num) do
    md5_salt_n(salt, num)
    |> info_from_md5(num)
  end

  def stretch_info(salt, num) do
    stretch_md5_salt_n(salt, num)
    |> info_from_md5(num)
  end

  defp info_from_md5(md5, num) do
    triple = triple?(md5)
    quint = quint?(md5)

    %{
      num: num,
      md5: md5,
      triple: triple,
      triple_char: if(triple, do: triple_char(md5), else: nil),
      quint: quint,
      quint_chars: if(quint, do: quint_chars(md5), else: nil)
    }
  end
end

defmodule Elixir2016.Day14.HashServer do
  @doc """
  Example usage

  alias Elixir2016.Day14.HashServer

  iex(6)> {:ok, pid} = HashServer.start("abc")
  {:ok, #PID<0.208.0>}
  iex(7)> HashServer.get(pid, 18)
  "computing"
  %{md5: "0034E0923CC38887A57BD7B1D4F953DF", num: 18, quint: false, triple: true}
  iex(8)> HashServer.get(pid, 18)
  %{md5: "0034E0923CC38887A57BD7B1D4F953DF", num: 18, quint: false, triple: true}
  iex(9)> HashServer.get(pid, 19)
  "computing"
  %{md5: "6EF56B8D791C660573DEA373BF88155F", num: 19, quint: false, triple: false}
  iex(10)> HashServer.get(pid, 19)
  %{md5: "6EF56B8D791C660573DEA373BF88155F", num: 19, quint: false, triple: false}
  iex(11)>
  """
  use GenServer
  alias Elixir2016.Day14.Hash

  def start(salt, is_stretch) do
    GenServer.start(__MODULE__, {salt, is_stretch})
  end

  def get(pid, num) do
    GenServer.call(pid, {:get, num})
  end

  #### Implementation ####

  def init({salt, is_stretch}) do
    {:ok, %{salt: salt, is_stretch: is_stretch}}
  end

  def handle_call({:get, num}, _from, state) do
    state = get_num(state, num)
    {:reply, Map.get(state, num), state}
  end

  def get_num(state, num) do
    if Map.has_key?(state, num) do
      state
    else
      add_num(state, num)
    end
  end

  def add_num(state, num) do
    info =
      if state.is_stretch do
        Hash.stretch_info(state.salt, num)
      else
        Hash.info(state.salt, num)
      end

    state
    |> Map.put(num, info)
  end
end
