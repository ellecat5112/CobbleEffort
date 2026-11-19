"""Yanmamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a giant dragonfly: an olive-gold segmented body and tail, huge green compound eyes over a fanged
jaw, four long translucent wings and spiny clawed legs. 15 blocks.

Front is -z, y is up. Adult stage. Built on the Sand Yanmamon model, recoloured.
"""
from __future__ import annotations

from _digi import sized
from _variant import clone

_Y = clone("sandyanmamon", "yanmamon",
           base={"grey": (190, 170, 90), "grey_dark": (120, 100, 40), "green": (90, 220, 90)},
           shiny={"grey": (90, 140, 200), "grey_dark": (40, 80, 140)})
HEIGHT = 13
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = _Y.KIND
K = _Y.K
LOOK = "a giant olive-gold dragonfly with huge green compound eyes, a fanged jaw, four translucent wings and spiny legs"
build = _Y.build
