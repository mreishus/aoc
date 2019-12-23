defmodule ElixirDay23.Coordinator do
  use GenServer
  alias ElixirDay23.{ComputerNWServer}

  def start(program, how_many) when is_list(program) and is_integer(how_many) do
    GenServer.start(__MODULE__, {program, how_many})
  end

  # Coordinator.send_packet(coordinator_pid, three_packet_list)
  def send_packet(pid, three_packet_list) do
    GenServer.cast(pid, {:send_packet, three_packet_list})
  end

  def put(pid, key, value) do
    GenServer.cast(pid, {:put, key, value})
  end

  def get(pid, key) do
    GenServer.call(pid, {:get, key})
  end

  #### Implementation ####

  def init({program, how_many}) when is_list(program) and is_integer(how_many) do
    "Coordinator starting" |> IO.inspect()

    coordinator_pid = self()
    pid_map = %{}

    pid_map =
      0..(how_many - 1)
      |> Enum.reduce(%{}, fn n, acc ->
        {:ok, pid} = ComputerNWServer.start(program, [n], coordinator_pid)
        Map.put(acc, n, pid)
      end)

    pid_map |> IO.inspect(label: "pid_map")

    {:ok, pid_map}
  end

  def handle_cast({:send_packet, three_packet_list}, state) do
    [address, x, y] = three_packet_list
    pid = Map.get(state, address, nil)

    if pid == nil do
      "Trying to send packet to invalid address"
      |> IO.inspect()

      three_packet_list |> IO.inspect()
    else
      ComputerNWServer.add_two_input(pid, x, y)
      # "Sent packet" |> IO.inspect()
    end

    {:noreply, state}
  end

  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end
end
