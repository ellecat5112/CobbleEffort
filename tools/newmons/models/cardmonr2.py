"""Cardmon R2 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round blue-and-white floating head ringed by four green cards. Perfect stage.

Front is -z, y is up. 29 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 29
SCALE, HITBOX = sized(25.0, HEIGHT, 1.09)
KIND = "floater"
K = 4
LOOK = "a round blue-and-white floating head ringed by four green cards"

build = make("cardmonr2", "blue", [((0, 11.0, 0), (0, 0, 2), (5.0, 7.0)), ((-8.0, -6.0, 0), (0, 0, 30), (5.0, 7.0)), ((9.0, -4.0, 0), (0, 0, -60), (6.0, 8.0)), ((0, -10.0, -1.0), (0, 0, -4), (5.0, 7.0))], r=5.0)
