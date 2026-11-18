"""Hagurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
living cog: a round dark-steel face set in a golden gear, mismatched red eyes and a jagged mouth-seam, two silver cogs
spinning at its sides. Child stage, 1 block tall.

Front is -z, y is up. 22 units tall. Built by _hagurumon.make().
"""
from __future__ import annotations

from _digi import sized
from _hagurumon import make

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "floater"
K = 4
LOOK = "a round dark-steel face in a golden gear with mismatched red eyes and two spinning silver cogs"
build = make("hagurumon")
