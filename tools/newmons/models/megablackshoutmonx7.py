"""Mega Black Shoutmon X7 (a Digimon of the CobbleEffort: Digital crossover; after the game stills on wikimon.net): Black Shoutmon X7 swollen to
colossal size by the Digital World's energy, otherwise unchanged. Built from the Black Shoutmon X7 module by _mega.make; 45 blocks
tall (no level on wikimon: built at the Super Ultimate size, the biggest).
"""
from __future__ import annotations

from _digi import sized
from _mega import make

build, _B = make("blackshoutmonx7", "megablackshoutmonx7")
HEIGHT = _B.HEIGHT
SCALE, HITBOX = sized(45, HEIGHT, 6.0)
KIND = _B.KIND
K = _B.K
ANIM = getattr(_B, "ANIM", None) or {}
LOOK = "a colossal Black Shoutmon X7, swollen to giant size"
