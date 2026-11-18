"""Mirage Gaogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a wolf knight in deep blue armour trimmed gold with star crests, a horned wolf-head helm, huge wolf-jaw gauntlets, a long red cape and a blue tail. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _miragegaogamon.make(burst=False).
"""
from __future__ import annotations

from _digi import sized
from _miragegaogamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a wolf knight in deep blue armour trimmed gold with star crests, a horned wolf-head helm, huge wolf-jaw gauntlets, a long red cape and a blue tail"
build = make("miragegaogamon", burst=False)
