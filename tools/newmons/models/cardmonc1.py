"""Cardmon C1 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round yellow-and-white floating head with big black eyes and one green card hovering above it. Child stage.

Front is -z, y is up. 22 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 0.82)
KIND = "floater"
K = 4
LOOK = "a round yellow-and-white floating head with big black eyes and one green card hovering above it"

build = make("cardmonc1", "yellow", [((0, 12.0, 0), (0, 0, 4), (5.0, 7.0))], r=5.0)
