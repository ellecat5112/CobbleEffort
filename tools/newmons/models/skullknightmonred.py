"""Skull Knightmon (Red) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a red-armoured Skull Knightmon with a silver skull chest and red drill cones. 15 blocks. Built by _skullknight.make(mode="base", colour="red").

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _skullknight import make

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a red-armoured Skull Knightmon with a silver skull chest and red drill cones"
build = make("skullknightmonred", mode="base", colour="red")
