"""Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a long coiling teal sea serpent with red stripes, a golden armoured dragon head with a swept horn and a red leaf tail fin.
15 blocks. Built by _seadramon.make(x=False).

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _seadramon import make

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a long coiling teal sea serpent with red stripes, a golden armoured dragon head with a swept horn and a red leaf tail fin"
build = make("seadramon", x=False)
