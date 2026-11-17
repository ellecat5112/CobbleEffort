"""Cardmon C2 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round blue-and-white floating head with big black eyes and a blue grid card at its side. Child stage.

Front is -z, y is up. 12 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 12
SCALE, HITBOX = sized(1.0, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a round blue-and-white floating head with big black eyes and a blue grid card at its side"

build = make("cardmonc2", "blue", [((6.6, -1.4000000000000004, 1.0), (0, -20, -8), (4.5, 8.0), 'grid')], r=5.0)
