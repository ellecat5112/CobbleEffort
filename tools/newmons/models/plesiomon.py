"""Plesiomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
great plesiosaur of the deep, white banded with blue-violet, a spiky black mane and orange-red flame fins. 35 blocks.
Built by _plesiomon.make(x=False).

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _plesiomon import make

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a white plesiosaur banded with blue-violet, a long coiling neck, four long flippers, a spiky black mane and flame fins"
build = make("plesiomon", x=False)
