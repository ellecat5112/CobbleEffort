"""Black Galgomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Galgomon's dark twin: a rabbit-eared dog-gunner with dark green-grey fur, gatling-barrel arms, a
leather belt, baggy green trousers and big clawed feet. 15 blocks tall.

Front is -z, y is up. 62 units tall; Adult stage. Built by _galgomon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _galgomon import make

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("Galgomon's dark twin: a rabbit-eared dog-gunner with dark green-grey fur, gatling-barrel arms, a leather "
        'belt, baggy green trousers and big clawed feet')
build = make("blackgalgomon", "adult", black=True)
