"""Ginkakumon Promote (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Ginkakumon promoted: the oni's armour turned gleaming gold and wreathed in golden light,
with the glass gourd, great horns and black cape. Adult stage, 15 blocks tall.

Front is -z, y is up. 78 units tall. Built by _ginkakumon.make(promote=True).
"""
from __future__ import annotations

from _digi import sized
from _ginkakumon import make

HEIGHT = 78
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking gold-armoured oni wreathed in golden light, with great horns, a glass gourd and a black cape"
build = make("ginkakumonpromote", promote=True)
