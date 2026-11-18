"""Ofanimon: Falldown Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the fallen Ofanimon in dark teal-black armour with a star crest, golden bat wings and red fire swirling round her. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (full armour). Built by _ofanimon.make(look="falldown").
"""
from __future__ import annotations

from _digi import sized
from _ofanimon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "the fallen Ofanimon in dark teal-black armour with a star crest, golden bat wings and red fire swirling round her"
build = make("ofanimonfalldownmode", look="falldown")
