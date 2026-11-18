"""Red V-dramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a stocky crimson dragon of the Veemon line with a big nose horn, swept horns, a pale V-marked belly and long white
claws. 15 blocks. Built by _vdramon.make(red=True).

Front is -z, y is up. 52 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _vdramon import make

HEIGHT = 52
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stocky crimson dragon with a big nose horn and swept horns, a pale V-marked belly and long white claws"
build = make("redvdramon", red=True)
