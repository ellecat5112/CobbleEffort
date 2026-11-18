"""Rosemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the X queen of flowers in a red suit wound with gold vines, a dark rose crown, a long dark-green cape and a golden thorn whip.
35 blocks. Built by _rosemon.make(look="x").

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _rosemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the X queen of flowers in a red suit wound with gold vines, a dark rose crown, a long dark-green cape and a golden thorn whip"
build = make("rosemonxantibody", look="x")
