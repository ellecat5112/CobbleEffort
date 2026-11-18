"""Hououmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Hououmon awakened by the X-Antibody: a radiant white-gold phoenix with bright wings, long
silver tail ribbons and crackling red lightning. 35 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage. Built by _hououmon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _hououmon import make

HEIGHT = 46
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = "a radiant white-gold phoenix with bright wings, silver tail ribbons and crackling red lightning"
build = make("hououmonxantibody", x=True)
