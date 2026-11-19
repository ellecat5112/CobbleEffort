"""Skull Knightmon: Cavalier Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a hulking black-and-gold armoured Skull Knightmon with long red drill-lances and a sweeping black cape. 25 blocks. Built by _skullknight.make(mode="cavalier", colour="black").

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _skullknight import make

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking black-and-gold armoured Skull Knightmon with long red drill-lances and a sweeping black cape"
build = make("skullknightmoncavaliermode", mode="cavalier", colour="black")
