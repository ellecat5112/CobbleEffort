"""Andiramon (Deva) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Andiramon as one of the Twelve Devas: the same rabbit-eared holy beast with a lilac
scarf knotted at its throat and lilac pants. 25 blocks tall.

Front is -z, y is up. 74 units tall; Perfect stage. Built by andiramon.make.
"""
from __future__ import annotations

from andiramon import ANIM, BASE as _B, HEIGHT, HITBOX, K, KIND, SCALE, SHINY as _S, make

LOOK = ("a rabbit-eared Deva: a small pale face, enormous pink-tipped ears, a white hooded mantle, a lilac scarf, long "
        "brown sleeve-arms with clawed cuffs and baggy lilac pants")
BASE = dict(_B, pants=(196, 180, 230), pants_dark=(140, 120, 190))
SHINY = dict(_S, scarf=(240, 200, 90), scarf_dark=(190, 140, 40), pants=(250, 230, 160), pants_dark=(210, 180, 100))
build = make("andiramondeva", BASE, SHINY, deva=True)
