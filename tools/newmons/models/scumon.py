"""Scumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a yellow slime of filth with a pointed swirl top, goggling eyes, a grin of square teeth, a lolling red
tongue, long skeletal arms with black cuffs and claws, and a little pink Chuumon riding on its head. 15 blocks.
Platinum Scumon's body with its own colours.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_S = clone("platinumscumon", "scumon",
           base={"plat": (250, 220, 40), "plat_dark": (200, 150, 20), "steel": (220, 190, 60), "steel_dark": (120, 100, 30)},
           shiny={"plat": (150, 200, 90), "plat_dark": (90, 140, 40)})
HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a yellow slime with a pointed swirl top, goggling eyes, a grin of square teeth, a red tongue, skeletal arms and a Chuumon rider"
build = _S.build
