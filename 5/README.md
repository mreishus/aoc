# Advent Of Code 2018, Day 5

https://adventofcode.com/2018/day/5

This was the first problem where **algorithmic complexity** mattered.  We're given strings like 
`dabAcCaCBAcCcaDA`, which may `react`.  

Any pairs of adjacent letters that differ only in case, like `aA`, react and are removed from the string.  This may cause other reactions to occur.  For example: `zAbBaY`.  The `bB` in the middle would react, leaving `zAaY`.  Then the `Aa` would react, leaving `zY`.

**Languages Solved In:** Ruby, Elixir

## Part 1

**Problem:** Given a large string, fully react it and return the length of the fully reacted string.

**Naive Approach, not implemented:**  Scan over the string, left to right, looking for a reaction.  When one is found, react the string, then repeat the scan until nothing is found.

This is horribly slow because we are doing a scan of the string for each reaction accomplished.  Worse yet, as we exhaust all of the reactions on the left half of the string, we are scanning it over and over again, wasting time.

**Approach, Ruby (Better, but not best):** I do a single scan of the string, noting all reaction points.  Then I process all of those reactions.  Repeat the process until no reactions were found. 

Note: When processing the reaction points, I process them in reverse order.  This way I don't need to update the reaction points as the string gets shorter.  If a 100-long string had reaction points [10, 20, 30], and I processed the reaction at 10, the other reaction points would now be at 18 and 28 instead of at 20 and 30.  But if I process at 30, it's safe to process at 20 and then 10 next.

This isn't the fastest possible solution, but it was easy to code quickly and was significantly more performant than the naive solution.  I ranked 1010 out of 26318, placing me in the 96.1th percentile.

**Approach, Elixir (Best):** Reading some solutions on Reddit, I was able to see a stack based approach.  I took the idea and implemented it in Elixir.  This way, we're able to process all reactions with only one scan of the string!

We process the input string, one at a time, putting it on result stack.  Whenever there's a reaction, we simply pop off the reacting character from the stack.   This is done in one reduce call.

```elixir
  def react(polymer) do
    polymer
    |> Enum.reduce([], fn new_letter, acc ->
      case are_letters_reactive(List.first(acc), new_letter) do
        false -> [new_letter | acc]
        true -> tl(acc)
      end
    end)
    |> Enum.reverse
  end
```

How it works.  Begin with:
```
 [] <- "dabAac"
```
 Most of the time, it moves a letter from the string into the array:  (to the front because it's faster, will reverse later)

```
 ["d"] <- "abAac"
 ["a", "d"] <- "bAac"
 ["b", "a", "d"] <- "Aac"
 ["A", "b", "a", "d"] <- "ac"
```
 However, if the front of the result array reacts with
 the front of the string, we drop the first element from the result array and throw away that letter from the string:

```
["b", "a", "d"] <- "c"
```

Back to normal:

```
["c", "b", "a", "d"]
```

 Now we're done, no need for multiple passes, only need to reverse when done.

## Part 2

**Problem:** React the long string 26 times, once after removing each letter in the alphabet from it.  Removing which letter helps the string become the shortest?

**Approaches:** Same as above.  This was mostly a way for them to make sure that you were not using the naive solution, since now you must react a very long string 26 times.

