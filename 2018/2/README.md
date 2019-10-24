# Advent Of Code 2018, Day 2

https://adventofcode.com/2018/day/2

I happened to be awake when the problem was released, so I wanted to try for a quick solution to get a high rank.  I developed a fast solution in Javascript, then redid the problem in Elixir as more practice in the language.

I solved the first part in 10 minutes, earning me rank #839, and the second part in 16 minutes, earning me rank #512.  

46,180 people solved Day 2, putting rank 512 as a respectable performance in the 98.89th percentile.  However, leader board points were only given for the top 100 ranks.

I realized I probably don't have what it takes to be a competitive programmer, especially since I wasn't using preparation. From here out I would relax and not treat the programs as so much of a race.

**Languages Solved In:** Elixir, Javascript (ES6)

## Part 1

**Problem:** Given a list of strings, find how many have 1.) a character repeated exactly 2 times, and 2.) a character repeated exactly 3 times.  Multiply these together for the final answer.

**Approach:** Reduce each string to a "seen map", which has characters as keys and counts as values, then filter and count for values of 2/3, and multiply.

## Part 2

**Problem:** Given a list of strings, find two that are only one character off.  Then print what's in common between those.

**Approach, Javascript:** For each pair of strings, I did a simple index scan to count the differences.  I simply incremented `i`, checked if `string1[i] != string2[i]`, and stopped checking if there was more than one difference.

**Approach, Elixir**:  Here I was able to use pattern matching and recursion to do a solution that fit more in line with functional programming.

```elixir
  # Given two strings, are they off by only one character?
  # input: "hello", "hallo"
  # output: true
  def are_strings_one_char_off(x, y) do
    is_one_char_off(x |> String.graphemes, y |> String.graphemes)
  end

  defp is_one_char_off([x | xs], [y | ys]) do
    case x == y do
      true -> is_one_char_off(xs, ys)
      false -> xs == ys
    end
  end
  defp is_one_char_off([], _), do: false
  defp is_one_char_off(_, []), do: false
```

**Drawbacks**:  Both approaches require each pair of strings to be checked, so it's not the most efficient runtime.
Perhaps a hashing based solution would be better?  Given the size of the input, it didn't matter much.
