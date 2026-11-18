"""Holydramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Holydramon awakened by the X-Antibody: a magenta serpentine dragon with a white
belly and fur, long banded horns and great magenta wings. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage. Built by _holydramon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _holydramon import make

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = "a long magenta serpentine holy dragon with a white belly, banded horns and great magenta wings"
build = make("holydramonxantibody", x=True)
