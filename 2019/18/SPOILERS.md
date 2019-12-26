# Day 18: Many-Worlds Interpretation

## Key Insights

- The path between keys never changes. Even though doors are opening and
  closing, these only completely block a path or not. So the path between all
  keys can be precomputed and saved. We just need to record any "blockers"
  (doors) on that path, so we know when it is available or not.
- After collecting keys in the following order: `A,B,C,D`, `A,C,B,D`,
  `B,A,C,D`, `B,C,A,D`, `C,A,B,D`, `C,B,A,D`, we are in the same node of the
  search space. We're standing at key `D`, holding keys `A,B,C,D`. The order
  of the last key matters because it determines where we are standing, but the
  order of the previously searched keys does not. These 6 nodes of the search
  space must absolutely be collapsed to 1, or your program will not finish (as
  this happens many times over).

## Approach

- Use _BFS_ to compute the distances between all keys.
- Walk each path between the keys and note which doors are along that path,
  recording them as blockers.
- Now, step "back" or "up" a level and run a _dijkstra's search_, with our nodes
  consisting of (Player Location, Set of keys held (order does not matter)).
  The edges are weighted by the number of steps between each key. For
  example, to move from `(Location of D, {A,B,C,D keys held})` to `(Location of G, {A,B,C,D,G keys held})`, the weight of the edge is the length of the path
  between keys D and G, which we precomputed. If the edge is available or
  not depends on if that path has any blockers that we don't have keys for (we
  also precomputed all of these lists.)
- An efficient priority queue data structure for dijkstra's to run quickly is
  absolutely needed.
- Python's `frozenset` is a hashable collection of objects where order does
  not matter, perfect for storing and comparing sets of keys collected.

## Approach P2

We generalize our solution a bit to hold multiple locations in state, and account
for some paths not existing. It was not that difficult after implementing
part 1.
