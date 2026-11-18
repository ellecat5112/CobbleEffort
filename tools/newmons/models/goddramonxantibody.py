"""Goddramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Goddramon awakened by the X-Antibody: blue armour and robe, a golden serpentine tail,
steel-blue blade-like wings and the lion mane and horned helm. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _goddramon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _goddramon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = "a blue-robed dragon-man with a lion mane, a golden serpentine tail and steel-blue wings"
build = make("goddramonxantibody", x=True)
