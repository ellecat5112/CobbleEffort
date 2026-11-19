"""V-dramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a stocky upright blue dragon of the V-mon line: a horned head with a big nose horn and two swept
horns, a pale muzzle and belly marked with a V, thick arms with long white claws, digitigrade legs with clawed feet
and a short heavy tail. 15 blocks.

Front is -z, y is up. Adult stage. Built by _vdramon.make.
"""
from __future__ import annotations

from _digi import sized
from _vdramon import make

HEIGHT = 52
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a stocky blue dragon with a big nose horn and swept horns, a pale V-marked belly and long white claws"
build = make("vdramon", red=False)
