#!/usr/bin/env python
"""
Advent Of Code 2015 Day 22
https://adventofcode.com/2015/day/22
"""

from collections import namedtuple, defaultdict
from dataclasses import dataclass
from typing import List
import copy
from aoc.heapdict import heapdict

# Magic Missile costs 53 mana. It instantly does 4 damage.
#
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit
# points.
#
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it
# is active, your armor is increased by 7.
#
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the
# start of each turn while it is active, it deals the boss 3 damage.
#
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the
# start of each turn while it is active, it gives you 101 new mana.

Spell = namedtuple("Spell", ("name", "cost", "damage", "heal", "effect_time"))
SPELLS = [
    Spell("Magic Missile", 53, 4, 0, 0),
    Spell("Drain", 73, 2, 2, 0),
    Spell("Shield", 113, 0, 0, 6),
    Spell("Poison", 173, 0, 0, 6),
    Spell("Recharge", 229, 0, 0, 5),
]


@dataclass
class GameState:
    player_hp: int
    player_mana: int
    boss_hp: int
    boss_dmg: int
    effects: dict
    hard_mode: bool = False
    player_won: bool = False
    boss_won: bool = False
    player_armor: int = 0


@dataclass(eq=True, frozen=True)
class HashableGameState:
    player_hp: int
    player_mana: int
    boss_hp: int
    boss_dmg: int
    effects: frozenset
    hard_mode: bool
    player_won: bool
    boss_won: bool
    player_armor: int


def hashable(s1: GameState) -> HashableGameState:
    return HashableGameState(
        s1.player_hp,
        s1.player_mana,
        s1.boss_hp,
        s1.boss_dmg,
        frozenset(s1.effects.items()),
        s1.hard_mode,
        s1.player_won,
        s1.boss_won,
        s1.player_armor,
    )


def unhashable(s1: HashableGameState) -> GameState:
    return GameState(
        s1.player_hp,
        s1.player_mana,
        s1.boss_hp,
        s1.boss_dmg,
        dict(s1.effects),
        s1.hard_mode,
        s1.player_won,
        s1.boss_won,
        s1.player_armor,
    )


def available_actions(state: GameState) -> List[Spell]:
    if state.player_won or state.boss_won:
        return []

    actions = []
    for spell in SPELLS:
        if spell.cost > state.player_mana:
            continue
        if spell.name in state.effects and state.effects[spell.name] > 0:
            continue
        actions.append(spell)
    return actions


def advance_state(state: GameState, spell: Spell) -> GameState:
    state = copy.deepcopy(state)

    # Player casts spell
    state.player_mana -= spell.cost
    state.boss_hp -= spell.damage
    state.player_hp += spell.heal
    if spell.effect_time > 0:
        if spell.name in state.effects and state.effects[spell.name] > 0:
            raise ValueError("Can't cast an effect that's already happening")
        state.effects[spell.name] = spell.effect_time

    # Check win
    state = check_win(state)
    if state.player_won or state.boss_won:
        return state

    # Switch to boss turn
    state = apply_effects(state)
    dealt = max(1, state.boss_dmg - state.player_armor)
    state.player_hp -= dealt

    # Check win
    state = check_win(state)
    if state.player_won or state.boss_won:
        return state

    # Switch to player turn: Apply effects and let the state rest before the
    # player casts a spell
    if state.hard_mode:
        state.player_hp -= 1
        state = check_win(state)
        if state.player_won or state.boss_won:
            return state

    state = apply_effects(state)
    state = check_win(state)
    return state


def check_win(state: GameState) -> GameState:
    state = copy.deepcopy(state)
    if state.boss_hp <= 0:
        state.player_won = True
        return state
    if state.player_hp <= 0:
        state.boss_won = True
    return state


def apply_effects(state: GameState) -> GameState:
    state = copy.deepcopy(state)
    state.player_armor = 0
    for (spell_name, turns) in state.effects.items():
        if turns <= 0:
            continue
        state.effects[spell_name] -= 1
        if spell_name == "Shield":
            state.player_armor = 7
        elif spell_name == "Poison":
            state.boss_hp -= 3
        elif spell_name == "Recharge":
            state.player_mana += 101
    return state


def solve(init_state: GameState):
    """ Use Dijkstra's to find the minimum mana needed to kill the boss. """
    dist_to = defaultdict(lambda: 999_999)
    edge_to = {}
    open_set = heapdict()

    dist_to[hashable(init_state)] = 0
    open_set[hashable(init_state)] = 0
    while len(open_set) > 0:
        (state, length) = open_set.popitem()

        if state.player_won:
            # Uncomment to see what spells it used:
            # spells = []
            # while state in edge_to:
            #     state, spell = edge_to[state]
            #     spells.append(spell)
            # for spell in reversed(spells):
            #     print(spell.name)
            return length

        state = unhashable(state)
        spells = available_actions(state)

        for spell in spells:
            new_state = hashable(advance_state(state, spell))
            if dist_to[new_state] > dist_to[hashable(state)] + spell.cost:
                dist_to[new_state] = dist_to[hashable(state)] + spell.cost
                edge_to[new_state] = (hashable(state), spell)
                open_set[new_state] = dist_to[new_state]
    return None


class Day22:
    """ AoC 2015 Day 22 """

    @staticmethod
    def part1(_filename: str) -> int:
        """ Given a filename, solve 2015 day 22 part 1 """
        state = GameState(50, 500, 71, 10, {})
        return solve(state)

    @staticmethod
    def part2(_filename: str) -> int:
        """ Given a filename, solve 2015 day 22 part 2 """
        state = GameState(50 - 1, 500, 71, 10, {}, True)
        return solve(state)
