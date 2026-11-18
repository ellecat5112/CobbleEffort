"""Leomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Leomon awakened by the X-Antibody: the lion warrior in dark plate armour with white fur cuffs, a long tattered red cape and a huge two-handed greatsword. 15 blocks tall. Built by _leomon.make(x=True).

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _leomon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a muscular lion-man in dark plate armour with white fur cuffs, a long tattered red cape and a huge two-handed greatsword"
build = make("leomonxantibody", x=True)
