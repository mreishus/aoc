defmodule ElixirDay23.Coordinator do
  use GenServer
  alias ElixirDay23.{ComputerNWServer}

  # start(program, how_many).  Start how_many copies of Computers,
  # all initialized with program, as well as their network address for
  # the first input.
  def start(program, how_many, send_answers_to) when is_list(program) and is_integer(how_many) do
    GenServer.start(__MODULE__, {program, how_many, send_answers_to})
  end

  # send_packet(pid, [address, x, y]): A computer calls this to send
  # a packet to another computer.
  def send_packet(pid, three_packet_list) do
    GenServer.cast(pid, {:send_packet, three_packet_list})
  end

  # get_packet(pid): A computer calls this when it needs input.
  # Either gets a packet looking like [x, y] from its network queue, or
  # returns [ -1 ] if no packet is available.
  # [this_input | new_inputs] = Coordinator.get_packet(coordinator_pid)
  def get_packet(pid) do
    GenServer.call(pid, :get_packet)
  end

  #### Implementation ####

  def init({program, how_many, send_answers_to}) when is_list(program) and is_integer(how_many) do
    "Coordinator starting" |> IO.inspect()
    coordinator_pid = self()

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

    state = %{
      pid_map: pid_map,
      inputs_for_pid: inputs_for_pid,
      nat_value: [nil, nil],
      last_wakeup_sent: nil,
      idle_count: 0,
      p1_answer: nil,
      p2_answer: nil,
      should_stop: false,
      send_answers_to: send_answers_to
    }

    {:ok, state}
  end

  def handle_cast(
        {:send_packet, three_packet_list},
        %{
          pid_map: pid_map,
          inputs_for_pid: inputs_for_pid,
          nat_value: nat_value
        } = state
      ) do
    [address, x, y] = three_packet_list
    pid = Map.get(pid_map, address, nil)

    inputs_for_pid =
      if pid == nil do
        inputs_for_pid
      else
        queue = Map.get(inputs_for_pid, pid, [])
        new_queue = queue ++ [x] ++ [y]
        Map.put(inputs_for_pid, pid, new_queue)
      end

    nat_value =
      if address == 255 do
        [x, y]
      else
        nat_value
      end

    new_state =
      state
      |> Map.put(:inputs_for_pid, inputs_for_pid)
      |> Map.put(:nat_value, nat_value)
      |> check_for_p1_answer()

    # Don't check for p2_answer here, it only triggers when sending a wakeup

    {:noreply, new_state}
  end

  def handle_call(:get_packet, {from_pid, _}, %{inputs_for_pid: inputs_for_pid} = state) do
    # Pull out packet from queue (or -1 if empty)
    queue = Map.get(inputs_for_pid, from_pid, [])
    {reply, new_queue} = get_packet_from_queue(queue)

    # Save new queue, and insert a special message if we detect it's idle
    inputs_for_pid =
      inputs_for_pid
      |> Map.put(from_pid, new_queue)

    # Build new state
    new_state =
      state
      |> Map.put(:inputs_for_pid, inputs_for_pid)
      |> update_idle_count()
      |> send_wakeup_message()

    if Map.get(new_state, :should_stop, false) do
      {:stop, :normal, new_state}
    else
      {:reply, reply, new_state}
    end
  end

  # From an input queue, pull off the oldest packet (two numbers).
  defp get_packet_from_queue([x | [y | rest]]) do
    {[x, y], rest}
  end

  # If an input queue is empty, pull off a -1 when requested an input.
  defp get_packet_from_queue(short_queue) do
    {[-1], short_queue}
  end

  # Check if the network queue is empty and if so, increment the idle count.
  defp update_idle_count(%{inputs_for_pid: inputs_for_pid, idle_count: idle_count} = state) do
    if queue_empty?(inputs_for_pid) do
      %{state | idle_count: idle_count + 1}
    else
      state
    end
  end

  # Given the network input queue, are all entries in it empty?
  defp queue_empty?(inputs_for_pid) do
    l =
      inputs_for_pid
      |> Map.values()
      |> Enum.map(&length/1)
      |> Enum.filter(fn x -> x > 0 end)
      |> length

    l == 0
  end

  # Cannot send wakeup message when no nat_value exists
  defp send_wakeup_message(%{nat_value: [nil, nil]} = state) do
    state
  end

  # If we've been idle for more than 200 ticks, and we have a nat_value,
  # send a special wakeup message to address 0 and reset the idle_count
  defp send_wakeup_message(%{idle_count: idle_count} = state) when idle_count > 200 do
    %{nat_value: nat_value, inputs_for_pid: inputs_for_pid, pid_map: pid_map} = state

    # Write message to console
    # "Idle network detected" |> IO.inspect(label: "label")
    # nat_value |> IO.inspect()

    # Send special message
    pid0 = Map.get(pid_map, 0)
    inputs_for_pid = inputs_for_pid |> Map.put(pid0, nat_value)

    state
    |> check_for_p2_answer(nat_value)
    |> Map.put(:inputs_for_pid, inputs_for_pid)
    |> Map.put(:idle_count, 0)
    |> Map.put(:last_wakeup_sent, nat_value)
    |> check_for_both_answers()
  end

  # If we've been idle less than 200 ticks, don't send any wakeup message
  defp send_wakeup_message(state) do
    state
  end

  # No p1 answer when nat_value is nil
  defp check_for_p1_answer(%{nat_value: [nil, nil]} = state), do: state

  # p1 answer is the first non-nil nat value
  defp check_for_p1_answer(%{p1_answer: nil, nat_value: nat_value} = state) do
    [_x, y] = nat_value

    state
    |> Map.put(:p1_answer, y)
  end

  # p1 answer never changes
  defp check_for_p1_answer(state), do: state

  defp check_for_p2_answer(
         %{p2_answer: nil, last_wakeup_sent: last_wakeup_sent} = state,
         wakeup_sent
       )
       when last_wakeup_sent == wakeup_sent do
    [_x, y] = wakeup_sent

    state
    |> Map.put(:p2_answer, y)
  end

  defp check_for_p2_answer(state, _wakeup_sent), do: state

  defp check_for_both_answers(
         %{p1_answer: p1_answer, p2_answer: p2_answer, send_answers_to: send_answers_to} = state
       )
       when not is_nil(p1_answer) and not is_nil(p2_answer) do
    # p1_answer |> IO.inspect(label: "Part 1")
    # p2_answer |> IO.inspect(label: "Part 2")

    halt_all_computers(state)
    send(send_answers_to, {:answers, p1_answer, p2_answer})

    state
    |> Map.put(:should_stop, true)
  end

  defp check_for_both_answers(state) do
    state
  end

  defp halt_all_computers(state) do
    state.pid_map
    |> Map.values()
    |> Enum.each(fn pid ->
      Process.exit(pid, :kill)
    end)
  end
end
