"""Mega Seadramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the sea serpent in pale yellow with orange leopard spots, a brown bone-skull helm with a great tusk-blade and green back fins. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage. Built by _megaseadramon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _megaseadramon import make

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "the sea serpent in pale yellow with orange leopard spots, a brown bone-skull helm with a great tusk-blade and green back fins"
build = make("megaseadramonxantibody", look="x")
