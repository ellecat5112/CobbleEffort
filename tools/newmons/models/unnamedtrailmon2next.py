"""Unnamed Trailmon 2 (Next) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): a living bullet train from Digimon Next (after a manga panel): a sleek white train with a red skirt, swept blade fins and a tail fin. 15 blocks tall.

Front is -z, y is up. Adult stage. Built by _trailmon.make.
"""
from __future__ import annotations

from _digi import sized
from _trailmon import make

HEIGHT = 23
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a living bullet train from Digimon Next (after a manga panel): a sleek white train with a red skirt, swept blade fins and a tail fin"
build = make("unnamedtrailmon2next", "next2")
