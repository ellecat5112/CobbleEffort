"""Tylomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Armor Digimon of reliability: a sleek sea-reptile like a shark, with a navy-and-white
armoured snout, swept blade fins, a pale-blue scaled body and a long curling neck-tail. 15 blocks.

Front is -z, y is up. Adult stage (Armor). Built by _tylomon.make.
"""
from __future__ import annotations

from _digi import sized
from _tylomon import make

HEIGHT = 26
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a sleek navy-and-white shark-like sea reptile with swept blade fins and a long curling neck-tail"
build = make("tylomon", False)
