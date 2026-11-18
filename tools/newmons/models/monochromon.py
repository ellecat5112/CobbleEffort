"""Monochromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a stocky four-legged horned dinosaur with grey-and-black patched hide, a white underside, one great black snout horn, red-tipped back spikes and heavy clawed feet. 15 blocks long.

Front is -z, y is up. 34 units tall; Adult stage. Built by _monochromon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _monochromon import make

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a stocky four-legged horned dinosaur with grey-and-black patched hide, a white underside, one great black snout horn, red-tipped back spikes and heavy clawed feet"
build = make("monochromon", x=False)
