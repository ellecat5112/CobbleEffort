"""Skull Knightmon: Arrow Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Skull Knightmon armed with a golden crossbow-bow. 15 blocks. Built by _skullknight.make(mode="arrow", colour="black").

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
LOOK = "Skull Knightmon armed with a golden crossbow-bow"
build = make("skullknightmonarrowmode", mode="arrow", colour="black")
