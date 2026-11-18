"""Knightmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the knight, a bulky silver plate-armoured knight with a visored great helm, a red emblem on its
breastplate, a violet tabard, studded pauldrons and a huge golden studded greatsword. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage. Built by _knightmon.make(wise=False).
"""
from __future__ import annotations

from _digi import sized
from _knightmon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a bulky silver plate-armoured knight with a visored great helm, a violet tabard and a huge golden greatsword"
build = make("knightmon", wise=False)
