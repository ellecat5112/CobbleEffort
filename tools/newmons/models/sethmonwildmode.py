"""Sethmon Wild Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a hulking red beast-man with a grizzled ape face under a white skull-mask, a green mane and two spiked maces ending in black dog heads.
25 blocks. Built by _sethmon.make(wild=True).

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _sethmon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking red beast-man with a grizzled ape face under a white skull-mask, a green mane and two spiked maces ending in black dog heads"
build = make("sethmonwildmode", wild=True)
