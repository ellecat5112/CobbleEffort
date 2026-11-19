"""Skull Knightmon (White) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a white-cloaked Skull Knightmon wanderer with a long staff. 15 blocks. Built by _skullknight.make(mode="white", colour="black").

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
LOOK = "a white-cloaked Skull Knightmon wanderer with a long staff"
build = make("skullknightmonwhite", mode="white", colour="black")
