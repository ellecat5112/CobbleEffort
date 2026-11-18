"""Mantaraymon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Mantaraymon awakened by the X-Antibody: a broad navy-armoured manta with silver edges, gold chevrons, a glowing electric orb under its snout and a cyan tail blade.
15 blocks wide. Built by _mantaraymon.make(x=True).

Front is -z, y is up. 20 units tall; Adult stage (Armor).
"""
from __future__ import annotations

from _digi import sized
from _mantaraymon import make

HEIGHT = 20
SCALE, HITBOX = sized(15, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a broad navy-armoured manta with silver edges, gold chevrons, a glowing electric orb under its snout and a cyan tail blade"
build = make("mantaraymonxantibody", x=True)
