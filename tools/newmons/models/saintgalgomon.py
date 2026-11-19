"""Saint Galgomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Rapidmon evolved: a heavy green armoured mech with missile pods and a rabbit-faced
warhead on its back, gatlings on its arms and spiked steel bands. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Built by _galgomon.make(black=False).
"""
from __future__ import annotations

from _digi import sized
from _galgomon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a heavy green armoured mech with missile pods and a rabbit-faced warhead on its back, gatling arms and spiked steel bands"
build = make("saintgalgomon", "ultimate", black=False)
