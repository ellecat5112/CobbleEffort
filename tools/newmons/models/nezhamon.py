"""Nezhamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a youthful cyborg warrior in gold-and-black plate with a revolver-cylinder faceplate, a streaming red sash, shoulder flames, a fire-tipped spear and great black-and-gold Wind-Fire Wheels on its legs. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _nezhamon.make(crimson=False).
"""
from __future__ import annotations

from _digi import sized
from _nezhamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a youthful cyborg warrior in gold-and-black plate with a revolver-cylinder faceplate, a streaming red sash, shoulder flames, a fire-tipped spear and great black-and-gold Wind-Fire Wheels on its legs"
build = make("nezhamon", crimson=False)
