"""Ogudomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the avatar of the Seven Great Demon Lords' sins: a towering black body on four enormous violet-striped legs with red hooked claws, a ring of red eyes and a fanged maw on its chest and the Demon Lords' emblems floating round it. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage (Demon Lord size). Built by _ogudomon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _ogudomon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "the avatar of the Seven Great Demon Lords' sins: a towering black body on four enormous violet-striped legs with red hooked claws, a ring of red eyes and a fanged maw on its chest and the Demon Lords' emblems floating round it"
build = make("ogudomon", x=False)
