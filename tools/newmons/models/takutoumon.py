"""Takutoumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an armoured guardian god in gold and teal plate over blue scale mail, a red tabard,
flame-patterned white trousers and a black cape, raising a glowing cyan pagoda and holding a crystal sword point
down, golden ribbons round it. 35 blocks.

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
LOOK = "an armoured guardian god raising a glowing cyan pagoda, with a crystal sword, red tabard and black cape"
build = make("takutoumon", wrath=False)
