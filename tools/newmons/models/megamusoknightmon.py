"""Mega Muso Knightmon (a Digimon of the CobbleEffort: Digital crossover; after the game stills on wikimon.net): Muso Knightmon swollen to
colossal size by the Digital World's energy, otherwise unchanged. Built from the Muso Knightmon module by _mega.make; 45 blocks
tall (no level on wikimon: built at the Super Ultimate size, the biggest).
"""
from __future__ import annotations

from _digi import sized
from _mega import make

build, _B = make("musoknightmon", "megamusoknightmon")
HEIGHT = _B.HEIGHT
SCALE, HITBOX = sized(45, HEIGHT, 6.0)
KIND = _B.KIND
K = _B.K
ANIM = getattr(_B, "ANIM", None) or {}
LOOK = "a colossal Muso Knightmon, swollen to giant size"
