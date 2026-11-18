"""Ginkakumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the silver horn oni: a hulking demon in silver plate over black mail, two great horns, a snarling
red-eyed oni mask, a glass gourd in its chest, spiked shoulders and knees, clawed gauntlets and a black cape.
Adult stage, 15 blocks tall.

Front is -z, y is up. 72 units tall. Built by _ginkakumon.make().
"""
from __future__ import annotations

from _digi import sized
from _ginkakumon import make

HEIGHT = 72
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking silver-armoured oni with two great horns, a snarling mask, a glass gourd in its chest and a black cape"
build = make("ginkakumon")
