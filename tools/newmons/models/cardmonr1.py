"""Cardmon R1 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round yellow-and-white floating head ringed by three green cards. Perfect stage.

Front is -z, y is up. 27 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 27
SCALE, HITBOX = sized(25.0, HEIGHT, 1.01)
KIND = "floater"
K = 4
LOOK = "a round yellow-and-white floating head ringed by three green cards"

build = make("cardmonr1", "yellow", [((-8.0, 5.0, 0), (0, 0, 20), (5.0, 7.0)), ((10.0, 8.0, 0), (0, 0, -35), (7.0, 9.5)), ((0, -9.0, 0), (0, 0, 4), (5.0, 7.0))], r=5.0)
