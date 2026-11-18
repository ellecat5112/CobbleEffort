"""Mega Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the great sea serpent coiled in an S, white body chevroned in blue with rows of red fin-blades, a golden helm with a lightning-bolt horn. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage. Built by _megaseadramon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _megaseadramon import make

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "the great sea serpent coiled in an S, white body chevroned in blue with rows of red fin-blades, a golden helm with a lightning-bolt horn"
build = make("megaseadramon", look="base")
