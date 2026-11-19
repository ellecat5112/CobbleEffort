"""Skull Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a stocky undead knight in black armour with a silver skull chest, a barred knight helm, red drill cones on its shoulders and a tattered cape. 15 blocks. Built by _skullknight.make(mode="base", colour="black").

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
LOOK = "a stocky undead knight in black armour with a silver skull chest, a barred knight helm, red drill cones on its shoulders and a tattered cape"
build = make("skullknightmon", mode="base", colour="black")
