defmodule ElixirDay18 do
  alias ElixirDay18.DuetVM

  def main do
    DuetVM.new("../input.txt")
    |> DuetVM.execute_until_recover()
    |> IO.inspect()
  end
end
