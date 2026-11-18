"""Hagurumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Hagurumon awakened by the X-Antibody: its gear ring turned red and gold, two small black cogs above like
ears, golden drill cones on its sides and silver cogs spinning beside them. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall. Built by _hagurumon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _hagurumon import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "floater"
K = 4
LOOK = "a red-and-gold gear with a dark face, cog ears, golden drills and spinning silver cogs"
build = make("hagurumonxantibody", x=True)
