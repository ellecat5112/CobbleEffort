"""Cardmon U2 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round blue-and-white floating head with two green cards beside it. Adult stage.

Front is -z, y is up. 15 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 15
SCALE, HITBOX = sized(15.0, HEIGHT, 0.56)
KIND = "floater"
K = 4
LOOK = "a round blue-and-white floating head with two green cards beside it"

build = make("cardmonu2", "blue", [((-8.0, -5.0, 0), (0, 0, -25), (5.0, 7.0)), ((10.0, -4.0, 0), (0, 0, 30), (7.0, 9.5))], r=5.0)
