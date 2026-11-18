"""Gazimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gazimon awakened by the X-Antibody: an upright pale-blue gremlin with long jagged ears, a gaping red
maw, red eyes, long black claws and black straps. Child stage, 1 block tall.

Front is -z, y is up. 34 units tall. Built by _gazimon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _gazimon import make

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "an upright pale-blue gremlin with long jagged ears, a gaping red maw and long black claws"
build = make("gazimonxantibody", x=True)
