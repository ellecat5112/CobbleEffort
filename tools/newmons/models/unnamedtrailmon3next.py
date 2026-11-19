"""Unnamed Trailmon 3 (Next) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living bullet train from Digimon Next (after a manga panel): a grey ribbed train with a long beak of a nose and pale eyes. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 18
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living bullet train from Digimon Next (after a manga panel): a grey ribbed train with a long beak of a nose and pale eyes"
build = make("unnamedtrailmon3next", "next3")
