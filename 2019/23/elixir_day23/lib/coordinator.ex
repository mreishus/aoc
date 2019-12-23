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

  # [this_input | new_inputs] = Coordinator.get_packet(coordinator_pid)
  def get_packet(pid) do
    GenServer.call(pid, :get_packet)
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
    # pid_map = %{}
    # input_for_pid = %{}

    pid_map =
      0..(how_many - 1)
      |> Enum.reduce(%{}, fn n, acc ->
        {:ok, pid} = ComputerNWServer.start(program, [n], coordinator_pid)
        Map.put(acc, n, pid)
      end)

    inputs_for_pid =
      Map.values(pid_map)
      |> Enum.reduce(%{}, fn pid, acc ->
        Map.put(acc, pid, [])
      end)

    # pid_map |> IO.inspect(label: "pid_map")
    # inputs_for_pid |> IO.inspect(label: "inputs_for_pid")

    {:ok, %{pid_map: pid_map, inputs_for_pid: inputs_for_pid}}
  end

  def handle_cast({:send_packet, three_packet_list}, %{
        pid_map: pid_map,
        inputs_for_pid: inputs_for_pid
      }) do
    [address, x, y] = three_packet_list
    pid = Map.get(pid_map, address, nil)

    new_inputs_for_pid =
      if pid == nil do
        "Trying to send packet to invalid address"
        |> IO.inspect()

        three_packet_list |> IO.inspect()
        inputs_for_pid
      else
        queue = Map.get(inputs_for_pid, pid, [])
        new_queue = queue ++ [x] ++ [y]
        Map.put(inputs_for_pid, pid, new_queue)
      end

    new_state = %{pid_map: pid_map, inputs_for_pid: new_inputs_for_pid}
    {:noreply, new_state}
  end

  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  def handle_call(:get_packet, {from_pid, _}, %{pid_map: pid_map, inputs_for_pid: inputs_for_pid}) do
    queue = Map.get(inputs_for_pid, from_pid, [])
    {reply, new_queue} = get_packet_from_queue(queue)
    new_inputs_for_pid = Map.put(inputs_for_pid, from_pid, new_queue)

    new_state = %{pid_map: pid_map, inputs_for_pid: new_inputs_for_pid}
    {:reply, reply, new_state}
  end

  defp get_packet_from_queue([x | [y | rest]]) do
    {[x, y], rest}
  end

  defp get_packet_from_queue(short_queue) do
    {[-1], short_queue}
  end
end
