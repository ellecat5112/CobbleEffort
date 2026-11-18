"""Leviamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Demon Lord of Envy: a colossal crimson crocodile-leviathan with a long toothy armoured snout, cyan back spines, whip antennae and a long tail, breathing rainbow mist. 35 blocks long. Built by _leviamon.make(x=False).

Front is -z, y is up. 26 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _leviamon import make

HEIGHT = 26
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "quadruped"
K = 3
LOOK = "a colossal crimson crocodile-leviathan with a long toothy armoured snout, cyan back spines, whip antennae and a long tail, breathing rainbow mist"
build = make("leviamon", x=False)
