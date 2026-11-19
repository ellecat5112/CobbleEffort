"""Takutoumon: Wrath Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Takutoumon in its wrath: red armoured claw-feet and gauntlets, flaming horns on its
helm and flame braziers on its shoulders, swinging a long golden trident-spear with a crystal blade. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _takutoumon.make.
"""
from __future__ import annotations

from _digi import sized
from _takutoumon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an armoured guardian god in wrath with flaming horns, red claw-feet and a golden trident-spear"
build = make("takutoumonwrathmode", wrath=True)
