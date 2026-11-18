"""Ofanimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Ophan angel: a slender woman in sleek teal-green armour, a visored helm with a gold crest, a long white robe-skirt, a golden ring-headed spear and four pairs of golden blade-feather wings. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built covered (full armour). Built by _ofanimon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _ofanimon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "the Ophan angel: a slender woman in sleek teal-green armour, a visored helm with a gold crest, a long white robe-skirt, a golden ring-headed spear and four pairs of golden blade-feather wings"
build = make("ofanimon", look="base")
