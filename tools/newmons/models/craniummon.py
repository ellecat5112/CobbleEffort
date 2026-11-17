"""Craniummon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the Royal Knight in deep violet plate with a skull motif, a glowing tabard, a tall crested helm, a great round shield and a double-ended spear. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _craniummon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the Royal Knight in deep violet plate with a skull motif, a glowing tabard, a tall crested helm, a great round shield and a double-ended spear"

build = make("craniummon", x=False)
